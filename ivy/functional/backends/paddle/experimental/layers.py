# global
from typing import Optional, Union, Tuple, List, Literal, Sequence, Callable
import paddle
from ivy.functional.ivy.layers import (
    _depth_max_pooling_helper,
    _validate_max_pool_params,
)
from ivy.utils.exceptions import IvyNotImplementedException, IvyValueError
from ivy.func_wrapper import (
    with_supported_device_and_dtypes,
    with_unsupported_dtypes,
    with_supported_dtypes,
)
from .. import backend_version

# local


def _determine_depth_max_pooling(x, kernel, strides, dims, data_format="channel_first"):
    # Determine depth pooling
    kernel, strides, depth_pooling = _depth_max_pooling_helper(
        x.shape, kernel, strides, dims=dims, data_format=data_format
    )
    if depth_pooling:
        x = paddle.transpose(x, (0, 2, 1, *range(3, dims + 2)))
    return x, kernel, strides, depth_pooling


@with_supported_device_and_dtypes(
    {
        "2.5.1 and below": {
            "cpu": ("float32", "float64"),
            "gpu": ("bfloat16", "float16", "float32", "float64"),
        }
    },
    backend_version,
)
def max_pool1d(
    x: paddle.Tensor,
    kernel: Union[int, Tuple[int, ...]],
    strides: Union[int, Tuple[int, ...]],
    padding: Union[str, int, Tuple[int], List[Tuple[int, int]]],
    /,
    *,
    data_format: str = "NWC",
    dilation: Union[int, Tuple[int]] = 1,
    ceil_mode: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    dims = 1
    kernel, strides, padding, dilation = _validate_max_pool_params(
        kernel, strides, padding, dilation, ceil_mode, dims=dims
    )

    if data_format == "NWC":
        x = paddle.transpose(x, perm=(0, 2, 1))
        kernel = [kernel[i] for i in [0, 2, 1]] if len(kernel) == (dims + 2) else kernel
        strides = (
            [strides[i] for i in [0, 2, 1]] if len(strides) == (dims + 2) else strides
        )
        padding = (
            [padding[i] for i in [0, 2, 1]]
            if isinstance(padding, list) and len(padding) == (dims + 2)
            else padding
        )

    # Determine depthwise pooling
    x, kernel, strides, depth_pooling = _determine_depth_max_pooling(
        x, kernel, strides, dims, data_format="channel_first"
    )

    # TODO: Add support for pooling with dilation in the paddle backend.
    # It's currently not natively supported in the fromework.
    if max(dilation) > 1:
        raise NotImplementedError(
            "Max pooling with dilation is currently not supported in the 'paddle'"
            " backend"
        )

    padding = (
        [item for sublist in padding for item in sublist]
        if not isinstance(padding, str)
        else padding
    )  # to work directly with paddle's max_pool1d function
    res = paddle.nn.functional.max_pool1d(
        x, kernel, strides, padding=padding, ceil_mode=ceil_mode
    )

    if depth_pooling:
        res = paddle.transpose(res, perm=(0, 2, 1))
    if data_format == "NWC":
        res = paddle.transpose(res, perm=(0, 2, 1))
    return res


@with_supported_device_and_dtypes(
    {
        "2.5.1 and below": {
            "cpu": ("float32", "float64"),
            "gpu": ("bfloat16", "float16", "float32", "float64"),
        }
    },
    backend_version,
)
def max_pool2d(
    x: paddle.Tensor,
    kernel: Union[int, Tuple[int, ...]],
    strides: Union[int, Tuple[int, ...]],
    padding: Union[str, int, Tuple[int], List[Tuple[int, int]]],
    /,
    *,
    data_format: str = "NHWC",
    dilation: Union[int, Tuple[int, ...]] = 1,
    ceil_mode: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    dims = 2
    kernel, strides, padding, dilation = _validate_max_pool_params(
        kernel, strides, padding, dilation, ceil_mode, dims=dims
    )

    if data_format == "NHWC":
        x = paddle.transpose(x, perm=[0, 3, 1, 2])
        kernel = (
            [kernel[i] for i in [0, 3, 1, 2]] if len(kernel) == (dims + 2) else kernel
        )
        strides = (
            [strides[i] for i in [0, 3, 1, 2]]
            if len(strides) == (dims + 2)
            else strides
        )
        padding = (
            [padding[i] for i in [0, 3, 1, 2]]
            if isinstance(padding, list) and len(padding) == (dims + 2)
            else padding
        )

    # Determine depthwise pooling
    x, kernel, strides, depth_pooling = _determine_depth_max_pooling(
        x, kernel, strides, dims, data_format="channel_first"
    )

    # TODO: Add support for pooling with dilation in the paddle backend.
    # It's currently not natively supported in the fromework.
    if max(dilation) > 1:
        raise NotImplementedError(
            "Max pooling with dilation is currently not supported in the 'paddle'"
            " backend"
        )

    padding = (
        [item for sublist in padding for item in sublist]
        if not isinstance(padding, str)
        else padding
    )  # paddle's expected format
    res = paddle.nn.functional.max_pool2d(
        x, kernel, strides, padding=padding, ceil_mode=ceil_mode
    )

    if depth_pooling:
        res = paddle.transpose(res, perm=[0, 2, 1, 3])
    if data_format == "NHWC":
        res = paddle.transpose(res, perm=[0, 2, 3, 1])
    return res


@with_supported_device_and_dtypes(
    {
        "2.5.1 and below": {
            "cpu": ("float32", "float64"),
            "gpu": ("bfloat16", "float16", "float32", "float64"),
        }
    },
    backend_version,
)
def max_pool3d(
    x: paddle.Tensor,
    kernel: Union[int, Tuple[int, ...]],
    strides: Union[int, Tuple[int, ...]],
    padding: Union[str, int, Tuple[int], List[Tuple[int, int]]],
    /,
    *,
    data_format: str = "NDHWC",
    dilation: Union[int, Tuple[int, ...]] = 1,
    ceil_mode: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    dims = 3
    kernel, strides, padding, dilation = _validate_max_pool_params(
        kernel, strides, padding, dilation, ceil_mode, dims=dims
    )

    if data_format == "NDHWC":
        x = paddle.transpose(x, perm=(0, 4, 1, 2, 3))
        kernel = (
            [kernel[i] for i in [0, 4, 1, 2, 3]]
            if len(kernel) == (dims + 2)
            else kernel
        )
        strides = (
            [strides[i] for i in [0, 4, 1, 2, 3]]
            if len(strides) == (dims + 2)
            else strides
        )
        padding = (
            [padding[i] for i in [0, 4, 1, 2, 3]]
            if isinstance(padding, list) and len(padding) == (dims + 2)
            else padding
        )

    # Determine depthwise pooling
    x, kernel, strides, depth_pooling = _determine_depth_max_pooling(
        x, kernel, strides, dims, data_format="channel_first"
    )

    # TODO: Add support for pooling with dilation in the paddle backend.
    # It's currently not natively supported in the fromework.
    if max(dilation) > 1:
        raise NotImplementedError(
            "Max pooling with dilation is currently not supported in the 'paddle'"
            " backend"
        )

    padding = (
        [item for sublist in padding for item in sublist]
        if not isinstance(padding, str)
        else padding
    )  # paddle's expected format
    res = paddle.nn.functional.max_pool3d(
        x, kernel, strides, padding=padding, ceil_mode=ceil_mode
    )

    if depth_pooling:
        res = paddle.transpose(res, perm=[0, 2, 1, 3, 4])
    if data_format == "NDHWC":
        res = paddle.transpose(res, perm=[0, 2, 3, 4, 1])
    return res


def avg_pool1d(
    x: paddle.Tensor,
    kernel: Union[int, Tuple[int]],
    strides: Union[int, Tuple[int]],
    padding: str,
    /,
    *,
    data_format: str = "NWC",
    count_include_pad: bool = False,
    ceil_mode: bool = False,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def avg_pool2d(
    x: paddle.Tensor,
    kernel: Union[int, Tuple[int], Tuple[int, int]],
    strides: Union[int, Tuple[int], Tuple[int, int]],
    padding: str,
    /,
    *,
    data_format: str = "NHWC",
    count_include_pad: bool = False,
    ceil_mode: bool = False,
    divisor_override: Optional[int] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def avg_pool3d(
    x: paddle.Tensor,
    kernel: Union[int, Tuple[int], Tuple[int, int, int]],
    strides: Union[int, Tuple[int], Tuple[int, int, int]],
    padding: str,
    /,
    *,
    data_format: str = "NDHWC",
    count_include_pad: bool = False,
    ceil_mode: bool = False,
    divisor_override: Optional[int] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def dct(
    x: paddle.Tensor,
    /,
    *,
    type: Optional[Literal[1, 2, 3, 4]] = 2,
    n: Optional[int] = None,
    axis: Optional[int] = -1,
    norm: Optional[Literal["ortho"]] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def fft(
    x: paddle.Tensor,
    dim: int,
    /,
    *,
    norm: Optional[str] = "backward",
    n: Union[int, Tuple[int]] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if not isinstance(dim, int):
        raise IvyValueError(f"Expecting <class 'int'> instead of {type(dim)}")

    if n is None:
        n = x.shape[dim]

    if dim < -x.ndim or dim >= x.ndim:
        raise IvyValueError(
            f"Invalid dim {dim}, expecting a value ranging from {-x.ndim} to {x.ndim-1}"
        )

    if not isinstance(n, int):
        raise TypeError(f"Expecting int type for 'n', instead of {type(n)}")

    if n <= 1:
        raise IvyValueError(f"Invalid number of data points {n}, expecting more than 1")

    valid_norm_modes = ["backward", "ortho", "forward"]
    if norm not in valid_norm_modes:
        raise IvyValueError(
            f"Unrecognized normalization mode {norm}, expecting one of"
            f" {valid_norm_modes}"
        )

    if x.dtype in [paddle.int64, paddle.float64, paddle.complex128]:
        x = x.cast(paddle.complex128)
    else:
        x = x.cast(paddle.complex64)

    return paddle.fft.fft(x, n, dim, norm=norm)


@with_supported_device_and_dtypes(
    {
        "2.5.1 and below": {
            "cpu": ("bfloat16", "float32", "float64"),
            "gpu": ("bfloat16", "float16", "float32", "float64"),
        }
    },
    backend_version,
)
def dropout1d(
    x: paddle.Tensor,
    prob: float,
    /,
    *,
    training: bool = True,
    data_format: str = "NWC",
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    axis = data_format.index("C") - 3 + x.ndim
    return paddle.nn.functional.dropout(x, p=prob, axis=axis, training=training)


@with_supported_device_and_dtypes(
    {
        "2.5.1 and below": {
            "cpu": ("bfloat16", "float32", "float64"),
            "gpu": ("bfloat16", "float16", "float32", "float64"),
        }
    },
    backend_version,
)
def dropout2d(
    x: paddle.Tensor,
    prob: float,
    /,
    *,
    training: bool = True,
    data_format: str = "NHWC",
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    axis = data_format.index("C") - 4 + x.ndim
    return paddle.nn.functional.dropout(x, p=prob, axis=axis, training=training)


@with_supported_device_and_dtypes(
    {
        "2.5.1 and below": {
            "cpu": ("bfloat16", "float32", "float64"),
            "gpu": ("bfloat16", "float16", "float32", "float64"),
        }
    },
    backend_version,
)
def dropout3d(
    x: paddle.Tensor,
    prob: float,
    /,
    *,
    training: bool = True,
    data_format: str = "NDHWC",
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    axis = data_format.index("C") - 5 + x.ndim
    return paddle.nn.functional.dropout(x, p=prob, axis=axis, training=training)


def ifft(
    x: paddle.Tensor,
    dim: int,
    *,
    norm: Optional[str] = "backward",
    n: Union[int, Tuple[int]] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def embedding(
    weights: paddle.Tensor,
    indices: paddle.Tensor,
    /,
    *,
    max_norm: Optional[int] = None,
    out=None,
) -> paddle.Tensor:
    raise IvyNotImplementedException()


def interpolate(
    x: paddle.Tensor,
    size: Union[Sequence[int], int],
    /,
    *,
    mode: Optional[Literal["linear", "bilinear", "trilinear"]] = "linear",
    scale_factor: Optional[Union[Sequence[int], int]] = None,
    recompute_scale_factor: Optional[bool] = None,
    align_corners: Optional[bool] = None,
    antialias: Optional[bool] = False,
    out: Optional[paddle.Tensor] = None,
):
    raise IvyNotImplementedException()


def adaptive_max_pool2d(
    input: paddle.Tensor, output_size: Union[Sequence[int], int]
) -> paddle.Tensor:
    squeeze = input.ndim == 3
    x = paddle.unsqueeze(input, axis=0) if squeeze else input
    ret = paddle.nn.functional.adaptive_max_pool2d(x, output_size)
    return paddle.squeeze(ret, axis=0) if squeeze else ret


def ifftn(
    x: paddle.Tensor,
    s: Optional[Union[int, Tuple[int]]] = None,
    axes: Optional[Union[int, Tuple[int]]] = None,
    *,
    norm: Optional[str] = "backward",
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    return paddle.fft.ifftn(x, s, axes, norm)


@with_unsupported_dtypes(
    {"2.5.1 and below": ("bfloat16", "float16", "complex64", "complex128", "bool")},
    backend_version,
)
def rfftn(
    x: paddle.Tensor,
    s: Optional[Union[int, Tuple[int]]] = None,
    axes: Optional[Union[int, Tuple[int]]] = None,
    *,
    norm: Optional[str] = "backward",
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    result = paddle.fft.rfftn(x, s, axes, norm)
    return result.astype("complex128")


@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "complex64",
            "complex128",
        )
    },
    backend_version,
)
def fft2(
    x: paddle.Tensor,
    *,
    dim: Optional[Union[int, Tuple[int]]] = None,
    norm: Optional[str] = "backward",
    s: Optional[Union[int, Tuple[int]]] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    res = paddle.fft.fft2(x, s, dim, norm)
    return res.astype("complex128")


# stft
@with_supported_dtypes(
    {
        "2.5.1 and below": (
            "complex64",
            "complex128",
        )
    },
    backend_version,
)
def stft(
    signals: paddle.Tensor,
    frame_length: int,
    frame_step: int,
    /,
    *,
    fft_length: Optional[int] = None,
    window_fn: Optional[Callable] = None,
    pad_end: Optional[bool] = False,
    name: Optional[str] = None,
    out: Optional[paddle.Tensor] = None,
) -> paddle.Tensor:
    if not isinstance(frame_length, int):
        raise IvyValueError(f"Expecting <class 'int'> instead of {type(frame_length)}")

    if frame_length < 1:
        raise IvyValueError(
            f"Invalid data points {frame_length}, expecting frame_length larger than or"
            " equal to 1"
        )

    if not isinstance(frame_step, int):
        raise IvyValueError(f"Expecting <class 'int'> instead of {type(frame_step)}")

    if frame_step < 1:
        raise IvyValueError(
            f"Invalid data points {frame_length}, expecting frame_length larger than or"
            " equal to 1"
        )

    if fft_length is not None:
        if not isinstance(fft_length, int):
            raise IvyValueError(
                f"Expecting <class 'int'> instead of {type(fft_length)}"
            )

        if fft_length < 1:
            raise IvyValueError(
                f"Invalid data points {frame_length}, expecting frame_length larger"
                " than or equal to 1"
            )

    input_dtype = signals.dtype
    if input_dtype == paddle.float32:
        dtype = "complex64"
    elif input_dtype == paddle.float64:
        dtype = "complex128"

    def stft_1D(signals, frame_length, frame_step, fft_length, pad_end):
        if fft_length is None:
            fft_length = 1
            while fft_length < frame_length:
                fft_length *= 2

        num_samples = signals.shape[-1]

        if pad_end:
            num_samples = signals.shape[-1]
            num_frames = -(-num_samples // frame_step)
            pad_length = max(
                0, frame_length + frame_step * (num_frames - 1) - num_samples
            )

            signals = paddle.nn.functional.pad(signals, (0, pad_length))
        else:
            num_frames = 1 + (num_samples - frame_length) // frame_step

        stft_result = []

        if window_fn is None:
            window = 1
        else:
            window = window_fn(frame_length)

        for i in range(num_frames):
            start = i * frame_step
            end = start + frame_length
            frame = signals[..., start:end]
            windowed_frame = frame * window
            pad_length = fft_length - frame_length
            windowed_frame = paddle.nn.functional.pad(windowed_frame, (0, pad_length))
            windowed_frame = paddle.to_tensor(windowed_frame)

            fft_frame = fft(windowed_frame, -1)
            slit = int((fft_length // 2 + 1))
            stft_result.append(fft_frame[..., 0:slit])

        stft = paddle.to_tensor(stft_result)
        return stft

    def stft_helper(nested_list, frame_length, frame_step, fft_length):
        nested_list = nested_list
        if len(nested_list.shape) > 1:
            return [
                stft_helper(sublist, frame_length, frame_step, fft_length)
                for sublist in nested_list
            ]
        else:
            return stft_1D(nested_list, frame_length, frame_step, fft_length, pad_end)

    to_return = stft_helper(signals, frame_length, frame_step, fft_length)
    result = paddle.to_tensor(to_return)
    return result.astype(dtype)
