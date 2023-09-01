from collections import namedtuple
from typing import (
    Optional,
    Union,
    Sequence,
    Tuple,
    NamedTuple,
    List,
    Any,
    Literal,
    Callable,
)
from numbers import Number


from .. import backend_version
from ivy.func_wrapper import with_unsupported_device_and_dtypes, with_supported_dtypes
import paddle
import ivy
import ivy.functional.backends.paddle as paddle_backend
from ivy.func_wrapper import with_supported_device_and_dtypes
from ...tensorflow.experimental.manipulation import _to_tf_padding

# Code from cephes for i0

_i0A = [
    -4.41534164647933937950e-18,
    3.33079451882223809783e-17,
    -2.43127984654795469359e-16,
    1.71539128555513303061e-15,
    -1.16853328779934516808e-14,
    7.67618549860493561688e-14,
    -4.85644678311192946090e-13,
    2.95505266312963983461e-12,
    -1.72682629144155570723e-11,
    9.67580903537323691224e-11,
    -5.18979560163526290666e-10,
    2.65982372468238665035e-9,
    -1.30002500998624804212e-8,
    6.04699502254191894932e-8,
    -2.67079385394061173391e-7,
    1.11738753912010371815e-6,
    -4.41673835845875056359e-6,
    1.64484480707288970893e-5,
    -5.75419501008210370398e-5,
    1.88502885095841655729e-4,
    -5.76375574538582365885e-4,
    1.63947561694133579842e-3,
    -4.32430999505057594430e-3,
    1.05464603945949983183e-2,
    -2.37374148058994688156e-2,
    4.93052842396707084878e-2,
    -9.49010970480476444210e-2,
    1.71620901522208775349e-1,
    -3.04682672343198398683e-1,
    6.76795274409476084995e-1,
]

_i0B = [
    -7.23318048787475395456e-18,
    -4.83050448594418207126e-18,
    4.46562142029675999901e-17,
    3.46122286769746109310e-17,
    -2.82762398051658348494e-16,
    -3.42548561967721913462e-16,
    1.77256013305652638360e-15,
    3.81168066935262242075e-15,
    -9.55484669882830764870e-15,
    -4.15056934728722208663e-14,
    1.54008621752140982691e-14,
    3.85277838274214270114e-13,
    7.18012445138366623367e-13,
    -1.79417853150680611778e-12,
    -1.32158118404477131188e-11,
    -3.14991652796324136454e-11,
    1.18891471078464383424e-11,
    4.94060238822496958910e-10,
    3.39623202570838634515e-9,
    2.26666899049817806459e-8,
    2.04891858946906374183e-7,
    2.89137052083475648297e-6,
    6.88975834691682398426e-5,
    3.36911647825569408990e-3,
    8.04490411014108831608e-1,
]


def moveaxis(
    a: paddle.Tensor,
    source: Union[int, Sequence[int]],
    destination: Union[int, Sequence[int]],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if isinstance(source, tuple):
        source = list(source)
    if isinstance(destination, tuple):
        source = list(destination)
    if a.dtype in [paddle.int8, paddle.int16, paddle.uint8]:
        return paddle.moveaxis(a.cast("float32"), source, destination).cast(a.dtype)
    return paddle.moveaxis(a, source, destination)


@with_supported_dtypes(
    {"2.5.1 and below": ("float16", "float32", "float64", "int32", "int64")},
    backend_version,
)
def pad(
    input: paddle.Tensor,
    pad_width: Union[Sequence[Sequence[int]], paddle.Tensor, int],
    /,
    *,
    mode: Union[
        Literal[
            "constant",
            "edge",
            "reflect",
            "wrap",
        ],
        Callable,
    ] = "constant",
    stat_length: Union[Sequence[paddle.Tensor], int] = 1,
    constant_values: Number = 0,
    end_values: Number = 0,
    reflect_type: Literal["even", "odd"] = "even",
    **kwargs: Optional[Any],
) -> paddle.Tensor:
    constant_values = (
        float(constant_values)
        if not isinstance(constant_values, float)
        else constant_values
    )
    pad_width = _to_paddle_padding(pad_width, input.ndim)
    mode = "replicate" if mode == "edge" else "circular" if mode == "wrap" else mode
    data_format = "NCL" if input.ndim == 1 else "NCHW" if input.ndim == 2 else "NCDHW"
    return (
        paddle.nn.functional.pad(
            input.unsqueeze(0).unsqueeze(0),
            pad_width,
            mode=mode,
            value=constant_values,
            data_format=data_format,
        )
        .squeeze(0)
        .squeeze(0)
    )


pad.partial_mixed_handler = lambda *args, mode="constant", constant_values=0, reflect_type="even", **kwargs: _check_paddle_pad(
    mode, reflect_type, args[1], args[0].shape, constant_values, 3
)


def _check_paddle_pad(
    mode, reflect_type, pad_width, input_shape, constant_values, ndim_limit
):
    pad_width = _to_tf_padding(pad_width, len(input_shape))
    return isinstance(constant_values, Number) and (
        mode == "constant"
        or (
            (
                (
                    mode == "reflect"
                    and reflect_type == "even"
                    and all(
                        pad_width[i][0] < s and pad_width[i][1] < s
                        for i, s in enumerate(input_shape)
                    )
                )
                or mode in ["edge", "wrap"]
            )
            and len(input_shape) <= ndim_limit
        )
    )


def _to_paddle_padding(pad_width, ndim):
    if isinstance(pad_width, Number):
        pad_width = [pad_width] * (2 * ndim)
    else:
        if len(pad_width) == 2 and isinstance(pad_width[0], Number) and ndim != 1:
            pad_width = pad_width * ndim
        pad_width = [item for sublist in pad_width for item in sublist[::-1]][::-1]
    return pad_width


@with_unsupported_device_and_dtypes(
    {
        "2.5.1 and below": {
            "cpu": (
                "int8",
                "int16",
                "uint8",
                "float16",
                "complex64",
                "complex128",
                "bool",
            )
        }
    },
    backend_version,
)
def heaviside(
    x1: paddle.Tensor,
    x2: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.heaviside(x1, x2)


def flipud(
    m: paddle.Tensor,
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if m.dtype in [paddle.int8, paddle.int16, paddle.uint8, paddle.float16]:
        return paddle.flip(m.cast("float32"), axis=0).cast(m.dtype)
    return paddle.flip(m, axis=0)


@with_unsupported_device_and_dtypes(
    {"2.5.1 and below": {"cpu": ("int16", "float16")}},
    backend_version,
)
def vstack(
    arrays: Sequence[paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    with ivy.ArrayMode(False):
        if arrays[0].ndim >= 2:
            return ivy.concat(arrays, axis=0)
        else:
            return ivy.stack(arrays, axis=0)


def hstack(
    arrays: Sequence[paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    with ivy.ArrayMode(False):
        if arrays[0].ndim >= 2:
            return ivy.concat(arrays, axis=1)
        else:
            return ivy.concat(arrays, axis=0)


@with_supported_device_and_dtypes(
    {
        "2.5.1 and above": {
            "cpu": (
                "bool",
                "int32",
                "int64",
                "float32",
                "float64",
            ),
            "gpu": ("float16",),
        },
    },
    backend_version,
)
def rot90(
    m: paddle.Tensor,
    /,
    *,
    copy: Optional[bool] = None,
    k: Optional[int] = 1,
    axes: Optional[Tuple[int, int]] = (0, 1),
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if (k % 4) and m.dtype in [paddle.int8, paddle.int16, paddle.uint8, paddle.float16]:
        return paddle.rot90(m.cast("float32"), k=k, axes=axes).cast(m.dtype)
    return paddle.rot90(m, k=k, axes=axes)


@with_unsupported_device_and_dtypes(
    {"2.5.1 and below": {"cpu": ("complex64", "complex128")}},
    backend_version,
)
def top_k(
    x: paddle.Tensor,
    k: int,
    /,
    *,
    axis: int = -1,
    largest: Optional[bool] = True,
    sorted: bool = True,
    out: Optional[Tuple[paddle.Tensor, paddle.Tensor]] = None,
) -> Tuple[paddle.Tensor, paddle.Tensor]:
    k = min(k, x.shape[axis])
    topk_res = NamedTuple(
        "top_k", [("values", paddle.Tensor), ("indices", paddle.Tensor)]
    )
    with ivy.ArrayMode(False):
        indices = ivy.argsort(x, axis=axis, descending=largest)
        indices = paddle.index_select(indices, paddle.arange(end=k), axis)
        if not sorted:
            indices = paddle.sort(indices, axis=axis)
        val = ivy.take_along_axis(x, indices, axis)
        return topk_res(val, indices)


def fliplr(
    m: paddle.Tensor,
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if m.dtype in [paddle.int8, paddle.int16, paddle.uint8, paddle.float16]:
        return paddle.flip(m.cast("float32"), axis=1).cast(m.dtype)
    return paddle.flip(m, axis=1)


def i0(
    x: paddle.Tensor,
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    def _i0_1(x):
        return paddle_backend.multiply(
            paddle_backend.exp(x),
            _chbevl(paddle_backend.subtract(paddle_backend.divide(x, 2.0), 2.0), _i0A),
        )

    def _i0_2(x):
        return paddle_backend.divide(
            paddle_backend.multiply(
                paddle_backend.exp(x),
                _chbevl(
                    paddle_backend.subtract(paddle_backend.divide(32.0, x), 2.0), _i0B
                ),
            ),
            paddle_backend.sqrt(x),
        )

    def _chbevl(x, vals):
        b0 = vals[0]
        b1 = 0.0

        for i in range(1, len(vals)):
            b2 = b1
            b1 = b0
            b0 = paddle_backend.add(
                paddle_backend.subtract(paddle_backend.multiply(x, b1), b2), vals[i]
            )
        return paddle_backend.multiply(0.5, paddle_backend.subtract(b0, b2))

    x = paddle_backend.abs(x)
    return paddle_backend.where(paddle_backend.less_equal(x, 8.0), _i0_1(x), _i0_2(x))


def flatten(
    x: paddle.Tensor,
    /,
    *,
    copy: Optional[bool] = None,
    start_dim: Optional[int] = 0,
    end_dim: Optional[int] = -1,
    order: Optional[str] = "C",
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    ivy.utils.assertions.check_elem_in_list(order, ["C", "F"])
    if x.ndim == 0:
        return x

    def _flatten(x, start_dim, end_dim):
        if x.dtype in [
            paddle.float16,
            paddle.complex64,
            paddle.complex128,
            paddle.bool,
        ]:
            if paddle.is_complex(x):
                return paddle.complex(
                    paddle.flatten(x.real(), start_axis=start_dim, stop_axis=end_dim),
                    paddle.flatten(x.imag(), start_axis=start_dim, stop_axis=end_dim),
                )
            return paddle.flatten(
                x.cast("float32"), start_axis=start_dim, stop_axis=end_dim
            ).cast(x.dtype)
        return paddle.flatten(x, start_axis=start_dim, stop_axis=end_dim)

    if order == "F":
        with ivy.ArrayMode(False):
            x = ivy.permute_dims(x, list(reversed(range(x.ndim))))
            ret = _flatten(x, start_dim, end_dim)
            return ivy.permute_dims(ret, list(reversed(range(ret.ndim))))
    return _flatten(x, start_dim, end_dim)


def vsplit(
    ary: paddle.Tensor,
    indices_or_sections: Union[int, Sequence[int], paddle.Tensor],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[paddle.Tensor]:
    if ary.ndim < 2:
        raise ivy.exceptions.IvyError(
            "vsplit only works on arrays of 2 or more dimensions"
        )
    return ivy.split(ary, copy=copy, num_or_size_splits=indices_or_sections, axis=0)


def dsplit(
    ary: paddle.Tensor,
    indices_or_sections: Union[int, Sequence[int], paddle.Tensor],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[paddle.Tensor]:
    if ary.ndim < 3:
        raise ivy.exceptions.IvyError(
            "dsplit only works on arrays of 3 or more dimensions"
        )
    return ivy.split(ary, num_or_size_splits=indices_or_sections, axis=2)


def atleast_1d(
    *arys: paddle.Tensor, copy: Optional[bool] = None
) -> List[paddle.Tensor]:
    res = []
    for ary in arys:
        ary = ivy.array(ary, copy=copy).data
        if ary.ndim < 1:
            with ivy.ArrayMode(False):
                res.append(ivy.expand_dims(ary, axis=0))
        else:
            res.append(ary)
    if len(res) == 1:
        return res[0]
    return res


def dstack(
    arrays: Sequence[paddle.Tensor],
    /,
    *,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    with ivy.ArrayMode(False):
        arrays = ivy.atleast_2d(*arrays)
        if not isinstance(arrays, list):
            arrays = [arrays]
        if arrays[0].ndim < 3:
            return ivy.stack(arrays, axis=-1)
        else:
            return ivy.concat(arrays, axis=2)


def atleast_2d(
    *arys: paddle.Tensor, copy: Optional[bool] = None
) -> List[paddle.Tensor]:
    res = []
    for ary in arys:
        ary = ivy.array(ary, copy=copy).data
        if ary.ndim < 2:
            with ivy.ArrayMode(False):
                res.append(ivy.expand_dims(ary, axis=list(range(2 - ary.ndim))))
        else:
            res.append(ary)
    if len(res) == 1:
        return res[0]
    return res


@with_unsupported_device_and_dtypes(
    {"2.5.1 and below": {"cpu": ("float16",)}},
    backend_version,
)
def atleast_3d(
    *arys: Union[paddle.Tensor, bool, Number], copy: Optional[bool] = None
) -> List[paddle.Tensor]:
    res = []
    for ary in arys:
        ary = ivy.array(ary, copy=copy).data
        if ary.ndim == 0:
            result = ary.reshape((1, 1, 1))
        elif ary.ndim == 1:
            result = ary[None, :, None]
        elif ary.ndim == 2:
            result = ary[:, :, None]
        else:
            result = ary
        res.append(result)
    if len(res) == 1:
        return res[0]
    else:
        return res


@with_unsupported_device_and_dtypes(
    {"2.5.1 and below": {"cpu": ("int8",)}},
    backend_version,
)
@with_supported_device_and_dtypes(
    {"2.5.1 and below": {"cpu": ("int32", "int64", "float32", "float64")}},
    backend_version,
)
def take_along_axis(
    arr: paddle.Tensor,
    indices: paddle.Tensor,
    axis: int,
    /,
    *,
    mode: str = "fill",
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if arr.ndim != indices.ndim:
        raise ivy.utils.exceptions.IvyException(
            "arr and indices must have the same number of dimensions;"
            + f" got {arr.ndim} vs {indices.ndim}"
        )
    indices = indices.cast("int64")
    if mode not in ["clip", "fill", "drop"]:
        raise ValueError(
            f"Invalid mode '{mode}'. Valid modes are 'clip', 'fill', 'drop'."
        )
    arr_shape = arr.shape
    if axis < 0:
        axis += arr.ndim
    if mode == "clip":
        max_index = arr.shape[axis] - 1
        with ivy.ArrayMode(False):
            indices = ivy.clip(indices, 0, max_index)
    elif mode in ("fill", "drop"):
        if "float" in str(arr.dtype) or "complex" in str(arr.dtype):
            fill_value = float("nan")
        elif "uint" in str(arr.dtype):
            fill_value = paddle.iinfo(arr.dtype).max
        elif "int" in str(arr.dtype):
            fill_value = -paddle.iinfo(arr.dtype).max - 1
        else:
            raise TypeError(
                f"Invalid dtype '{arr.dtype}'. Valid dtypes are 'float', 'complex',"
                " 'uint', 'int'."
            )

        with ivy.ArrayMode(False):
            indices = ivy.where(
                (indices < 0) | (indices >= arr.shape[axis]), -1, indices
            )
            arr_shape = list(arr_shape)
            arr_shape[axis] = 1
            fill_arr = ivy.full(arr_shape, fill_value, dtype=arr.dtype)
            arr = ivy.concat([arr, fill_arr], axis=axis)
            indices = ivy.where(indices < 0, arr.shape[axis] + indices, indices)

    if arr.dtype in [
        paddle.int8,
        paddle.int16,
        paddle.uint8,
        paddle.float16,
        paddle.complex64,
        paddle.complex128,
        paddle.bool,
    ]:
        if paddle.is_complex(arr):
            return paddle.complex(
                paddle.take_along_axis(arr.real(), indices, axis),
                paddle.take_along_axis(arr.imag(), indices, axis),
            )
        return paddle.take_along_axis(arr.cast("float32"), indices, axis).cast(
            arr.dtype
        )
    return paddle.take_along_axis(arr, indices, axis)


def hsplit(
    ary: paddle.Tensor,
    indices_or_sections: Union[int, Tuple[int, ...]],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[paddle.Tensor]:
    if ary.ndim == 1:
        return ivy.split(ary, num_or_size_splits=indices_or_sections, axis=0)
    return ivy.split(ary, num_or_size_splits=indices_or_sections, axis=1)


def broadcast_shapes(*shapes: Union[List[int], List[Tuple]]) -> Tuple[int]:
    def _broadcast_shape(s1, s2):
        len_1 = len(s1)
        len_2 = len(s2)
        if len_1 == 0:
            return () if len_2 == 0 else s2
        elif len_1 != 0 and len_2 == 0:
            return s1
        else:
            return paddle.broadcast_shape(s1, s2)

    if len(shapes) == 0:
        raise ValueError("shapes=[] must be non-empty")
    elif len(shapes) == 1:
        return shapes[0]
    result = _broadcast_shape(shapes[0], shapes[1])
    for i in range(2, len(shapes)):
        result = _broadcast_shape(result, shapes[i])
    # paddle outputs -1 if the output dimension is 0
    result = [0 if dim == -1 else dim for dim in result]
    return tuple(result)


def expand(
    x: paddle.Tensor,
    shape: Union[List[int], List[Tuple]],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle_backend.broadcast_to(x, shape)


def concat_from_sequence(
    input_sequence: Union[Tuple[paddle.Tensor], List[paddle.Tensor]],
    /,
    *,
    new_axis: int = 0,
    axis: int = 0,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    with ivy.ArrayMode(False):
        if new_axis == 0:
            return ivy.concat(input_sequence, axis=axis)
        elif new_axis == 1:
            return ivy.stack(input_sequence, axis=axis)


@with_unsupported_device_and_dtypes(
    {"2.5.1 and below": {"cpu": ("int8", "int16", "uint8")}}, backend_version
)
def unique_consecutive(
    x: paddle.Tensor,
    /,
    *,
    axis: Optional[int] = None,
) -> Tuple[paddle.Tensor, paddle.Tensor, paddle.Tensor]:
    Results = namedtuple(
        "Results",
        ["output", "inverse_indices", "counts"],
    )
    x_shape = None
    if axis is None:
        x_shape = x.shape
        x = x.flatten()
        axis = -1
    if axis < 0:
        axis += x.ndim
    split_indices = paddle.flatten(
        paddle.where(
            ivy.current_backend().any(
                paddle.abs(paddle.diff(x, axis=axis)) > 1e-50,
                axis=tuple(i for i in paddle.arange(x.ndim) if i != axis),
            )
        )[0]
        + 1,
    )
    if len(split_indices) > 0:
        split_sizes = (
            [split_indices[0]]
            + [
                split_indices[i] - split_indices[i - 1]
                for i in range(1, len(split_indices))
            ]
            + [x.shape[axis] - split_indices[-1]]
        )
        sub_arrays = paddle.split(
            x,
            split_sizes,
            axis=axis,
        )
    else:
        sub_arrays = [x]
    output = paddle.concat(
        [
            ivy.current_backend().unique_all(sub_array, axis=axis)[0]
            for sub_array in sub_arrays
        ],
        axis=axis,
    )
    counts = paddle.to_tensor([sub_array.shape[axis] for sub_array in sub_arrays])
    inverse_indices = paddle.repeat_interleave(paddle.arange(len(counts)), counts)
    if x_shape:
        inverse_indices = paddle.reshape(inverse_indices, x_shape)
    return Results(
        output.astype(x.dtype),
        inverse_indices,
        counts,
    )


@with_unsupported_device_and_dtypes(
    {"2.5.1 and below": {"cpu": ("int8", "int16", "uint8", "float16")}}, backend_version
)
def fill_diagonal(
    a: paddle.Tensor,
    v: Union[int, float],
    /,
    *,
    wrap: bool = False,
) -> paddle.Tensor:
    shape = a.shape
    max_end = paddle.prod(paddle.to_tensor(shape))
    end = max_end
    if len(shape) == 2:
        step = shape[1] + 1
        if not wrap:
            end = shape[1] * shape[1]
    else:
        step = 1 + (paddle.cumprod(paddle.to_tensor(shape[:-1]), dim=0)).sum()
    end = max_end if end > max_end else end
    a = paddle.reshape(a, (-1,))
    w = paddle.zeros(a.shape, dtype=bool)
    ins = paddle.arange(0, max_end)
    steps = paddle.arange(0, end, step)

    for i in steps:
        i = ins == i
        w = paddle.logical_or(w, i)
    v = paddle.to_tensor(v, dtype=a.dtype)
    a = paddle.where(w, v, a)
    a = paddle.reshape(a, shape)
    return a
