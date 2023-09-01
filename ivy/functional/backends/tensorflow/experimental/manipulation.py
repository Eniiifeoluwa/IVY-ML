# global
from collections import namedtuple
from typing import (
    Union,
    Optional,
    Sequence,
    Tuple,
    NamedTuple,
    List,
    Literal,
    Callable,
    Any,
)
from numbers import Number
import tensorflow as tf

# local
from ivy.func_wrapper import with_unsupported_dtypes
from .. import backend_version
import ivy


def moveaxis(
    a: Union[tf.Tensor, tf.Variable],
    source: Union[int, Sequence[int]],
    destination: Union[int, Sequence[int]],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    return tf.experimental.numpy.moveaxis(a, source, destination)


@with_unsupported_dtypes({"2.13.0 and below": ("bfloat16",)}, backend_version)
def heaviside(
    x1: Union[tf.Tensor, tf.Variable],
    x2: Union[tf.Tensor, tf.Variable],
    /,
    *,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    return tf.cast(tf.experimental.numpy.heaviside(x1, x2), x1.dtype)


def flipud(
    m: Union[tf.Tensor, tf.Variable],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    return tf.experimental.numpy.flipud(m)


def vstack(
    arrays: Union[Sequence[tf.Tensor], Sequence[tf.Variable]],
    /,
    *,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    return tf.experimental.numpy.vstack(arrays)


def hstack(
    arrays: Union[Sequence[tf.Tensor], Sequence[tf.Variable]],
    /,
    *,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    return tf.experimental.numpy.hstack(arrays)


def rot90(
    m: Union[tf.Tensor, tf.Variable],
    /,
    *,
    copy: Optional[bool] = None,
    k: int = 1,
    axes: Tuple[int, int] = (0, 1),
    out: Union[tf.Tensor, tf.Variable] = None,
) -> Union[tf.Tensor, tf.Variable]:
    return tf.experimental.numpy.rot90(m, k, axes)


@with_unsupported_dtypes({"2.13.0 and below": ("unsigned", "complex")}, backend_version)
def top_k(
    x: tf.Tensor,
    k: int,
    /,
    *,
    axis: int = -1,
    largest: bool = True,
    sorted: bool = True,
    out: Optional[Tuple[tf.Tensor, tf.Tensor]] = None,
) -> Tuple[tf.Tensor, tf.Tensor]:
    k = min(k, x.shape[axis])
    if not largest:
        indices = tf.experimental.numpy.argsort(x, axis=axis)
        indices = tf.experimental.numpy.take(
            indices, tf.experimental.numpy.arange(k), axis=axis
        )
        indices = tf.dtypes.cast(indices, tf.int32)
    else:
        indices = tf.experimental.numpy.argsort(-x, axis=axis)
        indices = tf.experimental.numpy.take(
            indices, tf.experimental.numpy.arange(k), axis=axis
        )
        indices = tf.dtypes.cast(indices, tf.int32)
    if not sorted:
        indices = tf.sort(indices, axis=axis)
    topk_res = NamedTuple("top_k", [("values", tf.Tensor), ("indices", tf.Tensor)])
    val = tf.experimental.numpy.take_along_axis(x, indices, axis=axis)
    indices = tf.dtypes.cast(indices, tf.int64)
    return topk_res(val, indices)


def fliplr(
    m: Union[tf.Tensor, tf.Variable],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    return tf.experimental.numpy.fliplr(m)


@with_unsupported_dtypes({"2.13.0 and below": ("bfloat16",)}, backend_version)
def i0(
    x: Union[tf.Tensor, tf.Variable],
    /,
    *,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    return tf.math.bessel_i0(x, name=None)


def vsplit(
    ary: Union[tf.Tensor, tf.Variable],
    indices_or_sections: Union[int, Sequence[int], tf.Tensor, tf.Variable],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[Union[tf.Tensor, tf.Variable]]:
    if len(ary.shape) < 2:
        raise ivy.utils.exceptions.IvyError(
            "vsplit only works on arrays of 2 or more dimensions"
        )
    return ivy.split(ary, num_or_size_splits=indices_or_sections, axis=0)


def dsplit(
    ary: Union[tf.Tensor, tf.Variable],
    indices_or_sections: Union[int, Sequence[int], tf.Tensor, tf.Variable],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[Union[tf.Tensor, tf.Variable]]:
    if len(ary.shape) < 3:
        raise ivy.utils.exceptions.IvyError(
            "dsplit only works on arrays of 3 or more dimensions"
        )
    return ivy.split(ary, num_or_size_splits=indices_or_sections, axis=2)


def atleast_1d(
    *arys: Union[tf.Tensor, tf.Variable, bool, Number],
    copy: Optional[bool] = None,
) -> List[Union[tf.Tensor, tf.Variable]]:
    return tf.experimental.numpy.atleast_1d(*arys)


def dstack(
    arrays: Union[Sequence[tf.Tensor], Sequence[tf.Variable]],
    /,
    *,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    return tf.experimental.numpy.dstack(arrays)


def atleast_2d(
    *arys: Union[tf.Tensor, tf.Variable],
    copy: Optional[bool] = None,
) -> List[Union[tf.Tensor, tf.Variable]]:
    return tf.experimental.numpy.atleast_2d(*arys)


def atleast_3d(
    *arys: Union[tf.Tensor, tf.Variable, bool, Number],
    copy: Optional[bool] = None,
) -> List[Union[tf.Tensor, tf.Variable]]:
    return tf.experimental.numpy.atleast_3d(*arys)


def take_along_axis(
    arr: Union[tf.Tensor, tf.Variable],
    indices: Union[tf.Tensor, tf.Variable],
    axis: int,
    /,
    *,
    mode: str = "fill",
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    if len(arr.shape) != len(indices.shape):
        raise ivy.utils.exceptions.IvyException(
            "arr and indices must have the same number of dimensions;"
            + f" got {len(arr.shape)} vs {len(indices.shape)}"
        )
    indices = tf.dtypes.cast(indices, tf.int32)
    if mode not in ["clip", "fill", "drop"]:
        raise ValueError(
            f"Invalid mode '{mode}'. Valid modes are 'clip', 'fill', 'drop'."
        )
    arr_shape = arr.shape
    if axis < 0:
        axis += len(arr.shape)
    if mode == "clip":
        max_index = arr.shape[axis] - 1
        indices = tf.clip_by_value(indices, 0, max_index)
    elif mode in ("fill", "drop"):
        if "float" in str(arr.dtype) or "complex" in str(arr.dtype):
            fill_value = tf.constant(float("nan"), dtype=arr.dtype)
        elif "uint" in str(arr.dtype):
            fill_value = tf.constant(arr.dtype.max, dtype=arr.dtype)
        elif "int" in str(arr.dtype):
            fill_value = tf.constant(-arr.dtype.max - 1, dtype=arr.dtype)
        else:
            raise TypeError(
                f"Invalid dtype '{arr.dtype}'. Valid dtypes are 'float', 'complex',"
                " 'uint', 'int'."
            )
        indices = tf.where((indices < 0) | (indices >= arr.shape[axis]), -1, indices)
        arr_shape = list(arr_shape)
        arr_shape[axis] = 1
        fill_arr = tf.fill(arr_shape, fill_value)
        arr = tf.concat([arr, fill_arr], axis=axis)
    return tf.experimental.numpy.take_along_axis(arr, indices, axis)


def hsplit(
    ary: Union[tf.Tensor, tf.Variable],
    indices_or_sections: Union[int, Tuple[int, ...]],
    /,
    *,
    copy: Optional[bool] = None,
) -> List[Union[tf.Tensor, tf.Variable]]:
    if len(ary.shape) == 1:
        return ivy.split(ary, num_or_size_splits=indices_or_sections, axis=0)
    return ivy.split(ary, num_or_size_splits=indices_or_sections, axis=1)


def broadcast_shapes(
    *shapes: Union[List[int], List[Tuple]],
) -> Tuple[int, ...]:
    if len(shapes) > 1:
        desired_shape = tf.broadcast_dynamic_shape(shapes[0], shapes[1])
        if len(shapes) > 2:
            for i in range(2, len(shapes)):
                desired_shape = tf.broadcast_dynamic_shape(desired_shape, shapes[i])
    else:
        return [shapes[0]]
    return tuple(desired_shape.numpy().tolist())


def pad(
    input: Union[tf.Tensor, tf.Variable],
    pad_width: Union[Sequence[Sequence[int]], Union[tf.Tensor, tf.Variable], int],
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
    stat_length: Union[Sequence[Union[tf.Tensor, tf.Variable]], int] = 1,
    constant_values: Number = 0,
    end_values: Number = 0,
    reflect_type: Literal["even", "odd"] = "even",
    **kwargs: Optional[Any],
) -> Union[tf.Tensor, tf.Variable]:
    pad_width = _to_tf_padding(pad_width, len(input.shape))
    if not isinstance(pad_width, (tf.Variable, tf.Tensor)):
        pad_width = tf.constant(pad_width)
    return tf.pad(
        input,
        pad_width,
        mode=mode,
        constant_values=constant_values,
    )


pad.partial_mixed_handler = lambda *args, mode="constant", constant_values=0, reflect_type="even", **kwargs: _check_tf_pad(
    args[0].shape, args[1], mode, constant_values, reflect_type
)


def _check_tf_pad(input_shape, pad_width, mode, constant_values, reflect_type):
    pad_width = _to_tf_padding(pad_width, len(input_shape))
    return isinstance(constant_values, Number) and (
        mode == "constant"
        or (
            reflect_type == "even"
            and (
                (
                    mode == "reflect"
                    and all(
                        pad_width[i][0] < s and pad_width[i][1] < s
                        for i, s in enumerate(input_shape)
                    )
                )
                or (
                    mode == "symmetric"
                    and all(
                        pad_width[i][0] <= s and pad_width[i][1] <= s
                        for i, s in enumerate(input_shape)
                    )
                )
            )
        )
    )


def _to_tf_padding(pad_width, ndim):
    if isinstance(pad_width, Number):
        pad_width = [[pad_width] * 2] * ndim
    elif len(pad_width) == 2 and isinstance(pad_width[0], Number):
        pad_width = pad_width * ndim
    return pad_width


def expand(
    x: Union[tf.Tensor, tf.Variable],
    shape: Union[List[int], List[Tuple]],
    /,
    *,
    copy: Optional[bool] = None,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    shape = list(shape)
    for i, dim in enumerate(shape):
        if dim < 0:
            shape[i] = x.shape.num_elements() / tf.reduce_prod(
                [s for s in shape if s > 0]
            )
    return tf.broadcast_to(x, shape)


def concat_from_sequence(
    input_sequence: Union[Tuple[tf.Tensor], List[tf.Tensor]],
    /,
    *,
    new_axis: int = 0,
    axis: int = 0,
    out: Optional[Union[tf.Tensor, tf.Variable]] = None,
) -> Union[tf.Tensor, tf.Variable]:
    is_tuple = type(input_sequence) is tuple
    if is_tuple:
        input_sequence = list(input_sequence)
    highest_dtype = input_sequence[0].dtype
    for i in input_sequence:
        highest_dtype = ivy.as_native_dtype(ivy.promote_types(highest_dtype, i.dtype))

    if new_axis == 0:
        ret = tf.concat(input_sequence, axis=axis)
        return ret
    elif new_axis == 1:
        ret = tf.stack(input_sequence, axis=axis)
        return ret


def unique_consecutive(
    x: Union[tf.Tensor, tf.Variable],
    /,
    *,
    axis: Optional[int] = None,
) -> Tuple[
    Union[tf.Tensor, tf.Variable],
    Union[tf.Tensor, tf.Variable],
    Union[tf.Tensor, tf.Variable],
]:
    Results = namedtuple(
        "Results",
        ["output", "inverse_indices", "counts"],
    )
    x_shape = None
    if axis is None:
        x_shape = x.shape
        x = tf.reshape(x, -1)
        axis = -1
    ndim = len(x.shape)
    if axis < 0:
        axis += ndim
    splits = (
        tf.where(
            tf.math.reduce_any(
                tf.experimental.numpy.diff(x, axis=axis) != 0,
                axis=tuple(i for i in tf.range(ndim) if i != axis),
            )
        )
        + 1
    )
    if tf.size(splits) > 0:
        sub_arrays = tf.experimental.numpy.split(x, tf.reshape(splits, -1), axis=axis)
    else:
        sub_arrays = [x]
    output = tf.concat(
        [
            tf.raw_ops.UniqueV2(x=sub_array, axis=tf.constant([axis]))[0]
            for sub_array in sub_arrays
        ],
        axis=axis,
    )
    counts = tf.convert_to_tensor([sub_array.shape[axis] for sub_array in sub_arrays])
    inverse_indices = tf.repeat(tf.range(len(counts)), counts)
    if x_shape:
        inverse_indices = tf.reshape(inverse_indices, x_shape)
    return Results(
        tf.cast(output, x.dtype),
        tf.cast(inverse_indices, tf.int64),
        tf.cast(counts, tf.int64),
    )


def fill_diagonal(
    a: tf.Tensor,
    v: Union[int, float],
    /,
    *,
    wrap: bool = False,
):
    shape = tf.shape(a)
    max_end = tf.math.reduce_prod(shape)
    end = max_end
    if len(shape) == 2:
        step = shape[1] + 1
        if not wrap:
            end = shape[1] * shape[1]
    else:
        step = 1 + tf.reduce_sum(tf.math.cumprod(shape[:-1]))
    a = tf.reshape(a, (-1,))
    end = min(end, max_end)
    indices = [[i] for i in range(0, end, step)]
    ups = tf.convert_to_tensor([v] * len(indices), dtype=a.dtype)
    a = tf.tensor_scatter_nd_update(a, indices, ups)
    a = tf.reshape(a, shape)
    return a
