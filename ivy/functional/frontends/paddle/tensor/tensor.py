# local
import ivy
import ivy.functional.frontends.paddle as paddle_frontend
from ivy.func_wrapper import (
    with_supported_dtypes,
    with_unsupported_dtypes,
)
from ivy.functional.frontends.paddle.func_wrapper import _to_ivy_array


class Tensor:
    def __init__(self, array, dtype=None, place="cpu", stop_gradient=True):
        self._ivy_array = (
            ivy.array(array, dtype=dtype, device=place)
            if not isinstance(array, ivy.Array)
            else array
        )
        self._dtype = dtype
        self._place = place
        self._stop_gradient = stop_gradient

    def __repr__(self):
        return (
            str(self._ivy_array.__repr__())
            .replace("ivy.array", "ivy.frontends.paddle.Tensor")
            .replace("dev", "place")
        )

    # Properties #
    # ---------- #

    @property
    def ivy_array(self):
        return self._ivy_array

    @property
    def place(self):
        return self.ivy_array.device

    @property
    def dtype(self):
        return self._ivy_array.dtype

    @property
    def shape(self):
        return self._ivy_array.shape

    @property
    def ndim(self):
        return self.dim()

    # Setters #
    # --------#

    @ivy_array.setter
    def ivy_array(self, array):
        self._ivy_array = (
            ivy.array(array) if not isinstance(array, ivy.Array) else array
        )

    # Special Methods #
    # -------------------#

    def __getitem__(self, item):
        ivy_args = ivy.nested_map([self, item], _to_ivy_array)
        ret = ivy.get_item(*ivy_args)
        return paddle_frontend.Tensor(ret)

    def __setitem__(self, item, value):
        raise ivy.utils.exceptions.IvyException(
            "ivy.functional.frontends.paddle.Tensor object doesn't support assignment"
        )

    def __iter__(self):
        if self.ndim == 0:
            raise TypeError("iteration over a 0-d tensor not supported")
        for i in range(self.shape[0]):
            yield self[i]

    # Instance Methods #
    # ---------------- #

    def reshape(self, *args, shape=None):
        if args and shape:
            raise TypeError("reshape() got multiple values for argument 'shape'")
        if shape is not None:
            return paddle_frontend.reshape(self._ivy_array, shape)
        if args:
            if isinstance(args[0], (tuple, list)):
                shape = args[0]
                return paddle_frontend.reshape(self._ivy_array, shape)
            else:
                return paddle_frontend.reshape(self._ivy_array, args)
        return paddle_frontend.reshape(self._ivy_array)

    def dim(self):
        return self.ivy_array.ndim

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def abs(self):
        return paddle_frontend.abs(self)

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def acosh(self, name=None):
        return paddle_frontend.Tensor(ivy.acosh(self._ivy_array))

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def ceil(self):
        return paddle_frontend.ceil(self)

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def ceil_(self):
        self.ivy_array = self.ceil().ivy_array
        return self

    @with_unsupported_dtypes({"2.5.1 and below": ("complex", "int8")}, "paddle")
    def numel(self):
        return paddle_frontend.numel(self)

    @with_unsupported_dtypes({"2.5.1 and below": ("float16",)}, "paddle")
    def asinh(self, name=None):
        return paddle_frontend.Tensor(ivy.asinh(self._ivy_array))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def asin(self, name=None):
        return paddle_frontend.Tensor(ivy.asin(self._ivy_array))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def cosh(self, name=None):
        return paddle_frontend.Tensor(ivy.cosh(self._ivy_array))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def log(self, name=None):
        return paddle_frontend.Tensor(ivy.log(self._ivy_array))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def sin(self, name=None):
        return paddle_frontend.Tensor(ivy.sin(self._ivy_array))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def sinh(self, name=None):
        return paddle_frontend.Tensor(ivy.sinh(self._ivy_array))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def lerp(self, y, weight, name=None):
        return paddle_frontend.lerp(self, y, weight)

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def lerp_(self, y, weight, name=None):
        self.ivy_array = paddle_frontend.lerp(self, y, weight).ivy_array
        return self

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def argmax(self, axis=None, keepdim=False, dtype=None, name=None):
        return paddle_frontend.Tensor(
            ivy.argmax(self._ivy_array, axis=axis, keepdims=keepdim, dtype=dtype)
        )

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "uint16")}, "paddle")
    def unsqueeze(self, axis=None, name=None):
        return paddle_frontend.Tensor(ivy.expand_dims(self._ivy_array, axis=axis))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def sqrt(self, name=None):
        return paddle_frontend.Tensor(ivy.sqrt(self._ivy_array))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def sqrt_(self, name=None):
        self.ivy_array = self.sqrt().ivy_array
        return self

    @with_unsupported_dtypes({"2.5.1 and below": ("bfloat16", "uint16")}, "paddle")
    def zero_(self):
        self.ivy_array = paddle_frontend.Tensor(
            ivy.zeros_like(self._ivy_array)
        ).ivy_array
        return self

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def cos(self, name=None):
        return paddle_frontend.Tensor(ivy.cos(self._ivy_array))

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def exp(self, name=None):
        return paddle_frontend.Tensor(ivy.exp(self._ivy_array))

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def exp_(self, name=None):
        self.ivy_array = self.exp().ivy_array
        return self

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def erf(self, name=None):
        return paddle_frontend.Tensor(ivy.erf(self._ivy_array))

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def subtract(self, y, name=None):
        return paddle_frontend.Tensor(ivy.subtract(self._ivy_array, _to_ivy_array(y)))

    @with_unsupported_dtypes(
        {"2.5.1 and below": ("float16", "uint8", "int8", "bool")}, "paddle"
    )
    def subtract_(self, y, name=None):
        self.ivy_array = self.subtract(y).ivy_array
        return self

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def log10(self, name=None):
        return paddle_frontend.Tensor(ivy.log10(self._ivy_array))

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def argsort(self, axis=-1, descending=False, name=None):
        return paddle_frontend.Tensor(
            ivy.argsort(self._ivy_array, axis=axis, descending=descending)
        )

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def floor(self, name=None):
        return paddle_frontend.Tensor(ivy.floor(self._ivy_array))

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def floor_(self):
        self.ivy_array = self.floor().ivy_array
        return self

    @with_supported_dtypes(
        {"2.5.1 and below": ("float32", "float64", "int32", "int64")}, "paddle"
    )
    def clip(self, min=None, max=None, name=None):
        ivy.utils.assertions.check_all_or_any_fn(
            min,
            max,
            fn=ivy.exists,
            type="any",
            limit=[1, 2],
            message="at most one of min or max can be None",
        )
        if min is None:
            ret = ivy.minimum(self._ivy_array, max)
        elif max is None:
            ret = ivy.maximum(self._ivy_array, min)
        else:
            ret = ivy.clip(self._ivy_array, min, max)
        return paddle_frontend.Tensor(ret)

    @with_supported_dtypes(
        {"2.5.1 and below": ("float32", "float64", "int32", "int64")}, "paddle"
    )
    def clip_(self, min=None, max=None, name=None):
        ivy.utils.assertions.check_all_or_any_fn(
            min,
            max,
            fn=ivy.exists,
            type="any",
            limit=[1, 2],
            message="at most one of min or max can be None",
        )
        if min is None:
            self._ivy_array = ivy.minimum(self._ivy_array, max)
        elif max is None:
            self._ivy_array = ivy.maximum(self._ivy_array, min)
        else:
            self._ivy_array = ivy.clip(self._ivy_array, min, max)
        return self

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def tanh(self, name=None):
        return paddle_frontend.Tensor(ivy.tanh(self._ivy_array))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def add_(self, y, name=None):
        self.ivy_array = paddle_frontend.Tensor(
            ivy.add(self._ivy_array, _to_ivy_array(y))
        ).ivy_array
        return self

    @with_supported_dtypes(
        {"2.5.1 and below": ("float16", "float32", "float64", "int32", "int64")},
        "paddle",
    )
    def isinf(self, name=None):
        return paddle_frontend.Tensor(ivy.isinf(self._ivy_array))

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "uint16")}, "paddle")
    def unsqueeze_(self, axis=None, name=None):
        self.ivy_array = paddle_frontend.Tensor(
            ivy.expand_dims(self._ivy_array, axis=axis)
        ).ivy_array
        return self

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def square(self, name=None):
        return paddle_frontend.Tensor(ivy.square(self._ivy_array))

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def remainder_(self, y, name=None):
        self.ivy_array = paddle_frontend.Tensor(
            ivy.remainder(self._ivy_array, _to_ivy_array(y))
        ).ivy_array
        return self

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def cholesky(self, upper=False, name=None):
        return paddle_frontend.Tensor(ivy.cholesky(self._ivy_array, upper=upper))

    @with_unsupported_dtypes(
        {"2.5.1 and below": ("float16", "uint16", "int16")}, "paddle"
    )
    def squeeze_(self, axis=None, name=None):
        if isinstance(axis, int) and self.ndim > 0:
            if self.shape[axis] > 1:
                return self
        if len(self.shape) == 0:
            return self
        self.ivy_array = paddle_frontend.Tensor(
            ivy.squeeze(self._ivy_array, axis=axis)
        ).ivy_array
        return self

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def multiply(self, y, name=None):
        return paddle_frontend.multiply(self, y)

    @with_supported_dtypes(
        {"2.5.1 and below": ("float16", "float32", "float64", "int32", "int64")},
        "paddle",
    )
    def isfinite(self, name=None):
        return paddle_frontend.Tensor(ivy.isfinite(self._ivy_array))

    @with_supported_dtypes({"2.4.2 and below": ("float16", "bfloat16")}, "paddle")
    def all(self, axis=None, keepdim=False, dtype=None, name=None):
        return paddle_frontend.Tensor(
            ivy.all(self.ivy_array, axis=axis, keepdims=keepdim, dtype=dtype)
        )

    @with_supported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def allclose(self, other, rtol=1e-05, atol=1e-08, equal_nan=False, name=None):
        return paddle_frontend.Tensor(
            ivy.allclose(
                self._ivy_array, other, rtol=rtol, atol=atol, equal_nan=equal_nan
            )
        )

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def sort(self, axis=-1, descending=False, name=None):
        return paddle_frontend.Tensor(
            ivy.sort(self._ivy_array, axis=axis, descending=descending)
        )

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def log1p(self, name=None):
        return ivy.log1p(self._ivy_array)

    @with_supported_dtypes(
        {
            "2.4.2 and below": (
                "bool",
                "uint8",
                "int8",
                "int16",
                "int32",
                "int64",
            )
        },
        "paddle",
    )
    def bitwise_and(self, y, out=None, name=None):
        return paddle_frontend.bitwise_and(self, y)

    @with_supported_dtypes(
        {
            "2.5.1 and below": (
                "bool",
                "int8",
                "int16",
                "int32",
                "int64",
                "float32",
                "float64",
            )
        },
        "paddle",
    )
    def logical_or(self, y, out=None, name=None):
        return paddle_frontend.logical_or(self, y, out=out)

    @with_supported_dtypes(
        {"2.5.1 and below": ("bool", "uint8", "int8", "int16", "int32", "int64")},
        "paddle",
    )
    def bitwise_xor(self, y, out=None, name=None):
        return paddle_frontend.bitwise_xor(self, y)

    @with_supported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def any(self, axis=None, keepdim=False, name=None):
        return paddle_frontend.Tensor(
            ivy.any(self._ivy_array, axis=axis, keepdims=keepdim)
        )

    @with_unsupported_dtypes({"2.5.1 and below": "bfloat16"}, "paddle")
    def astype(self, dtype):
        return paddle_frontend.Tensor(ivy.astype(self._ivy_array, dtype))

    @with_supported_dtypes(
        {"2.5.1 and below": ("bool", "uint8", "int8", "int16", "int32", "int64")},
        "paddle",
    )
    def bitwise_not(self, out=None, name=None):
        return paddle_frontend.Tensor(ivy.bitwise_invert(self._ivy_array, out=out))

    @with_supported_dtypes(
        {
            "2.5.1 and below": (
                "bool",
                "int8",
                "int16",
                "int32",
                "int64",
            )
        },
        "paddle",
    )
    def bitwise_or(self, y, out=None, name=None):
        return paddle_frontend.bitwise_or(self, y, out=out)

    @with_supported_dtypes(
        {
            "2.5.1 and below": (
                "bool",
                "int8",
                "int16",
                "int32",
                "int64",
                "float32",
                "float64",
            )
        },
        "paddle",
    )
    def logical_xor(self, y, out=None, name=None):
        return paddle_frontend.logical_xor(self, y, out=out)

    @with_supported_dtypes(
        {"2.5.1 and below": ("float16", "float32", "float64", "int32", "int64")},
        "paddle",
    )
    def isnan(self, name=None):
        return paddle_frontend.isnan(self)

    @with_unsupported_dtypes(
        {
            "2.5.1 and below": (
                "bool",
                "uint8",
                "int8",
                "int16",
                "complex64",
                "complex128",
            )
        },
        "paddle",
    )
    def greater_than(self, y, name=None):
        return paddle_frontend.greater_than(self, y)

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def rsqrt(self, name=None):
        return paddle_frontend.Tensor(ivy.reciprocal(ivy.sqrt(self._ivy_array)))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def rsqrt_(self, name=None):
        self.ivy_array = self.rsqrt().ivy_array
        return self

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def reciprocal(self, name=None):
        return paddle_frontend.reciprocal(self)

    @with_supported_dtypes(
        {
            "2.5.1 and below": (
                "bool",
                "int8",
                "int16",
                "int32",
                "int64",
                "float32",
                "float64",
            )
        },
        "paddle",
    )
    def logical_and(self, y, out=None, name=None):
        return paddle_frontend.logical_and(self, y, out=out)

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def divide(self, y, name=None):
        return paddle_frontend.divide(self, y)

    @with_unsupported_dtypes(
        {
            "2.5.1 and below": (
                "bool",
                "uint8",
                "int8",
                "int16",
                "complex64",
                "complex128",
            )
        },
        "paddle",
    )
    def less_than(self, y, name=None):
        return paddle_frontend.less_than(self, y)

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def cumprod(self, dim=None, dtype=None, name=None):
        return paddle_frontend.Tensor(
            ivy.cumprod(self._ivy_array, axis=dim, dtype=dtype)
        )

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def cumsum(self, axis=None, dtype=None, name=None):
        return paddle_frontend.Tensor(
            ivy.cumsum(self._ivy_array, axis=axis, dtype=dtype)
        )

    @with_supported_dtypes(
        {"2.5.1 and below": ("complex64", "complex128", "float32", "float64")},
        "paddle",
    )
    def angle(self, name=None):
        return paddle_frontend.Tensor(ivy.angle(self._ivy_array))

    @with_unsupported_dtypes(
        {
            "2.5.1 and below": (
                "uint8",
                "int8",
                "int16",
                "complex64",
                "complex128",
            )
        },
        "paddle",
    )
    def equal(self, y, name=None):
        return paddle_frontend.equal(self, y)

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def rad2deg(self, name=None):
        return paddle_frontend.Tensor(ivy.rad2deg(self._ivy_array))

    @with_unsupported_dtypes(
        {
            "2.5.1 and below": (
                "uint8",
                "int8",
                "int16",
                "float16",
                "complex64",
                "complex128",
            )
        },
        "paddle",
    )
    def equal_all(self, y, name=None):
        return paddle_frontend.Tensor(
            ivy.array_equal(self._ivy_array, _to_ivy_array(y))
        )

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def maximum(self, other, name=None):
        return ivy.maximum(self._ivy_array, other)

    @with_unsupported_dtypes({"2.5.1 and below": "bfloat16"}, "paddle")
    def fmax(self, y, name=None):
        return paddle_frontend.Tensor(ivy.fmax(self._ivy_array, _to_ivy_array(y)))

    @with_unsupported_dtypes({"2.5.1 and below": "bfloat16"}, "paddle")
    def fmin(self, y, name=None):
        return paddle_frontend.Tensor(ivy.fmin(self._ivy_array, _to_ivy_array(y)))

    @with_supported_dtypes(
        {"2.5.1 and below": ("float32", "float64", "int32", "int64")}, "paddle"
    )
    def minimum(self, y, name=None):
        return paddle_frontend.Tensor(ivy.minimum(self._ivy_array, _to_ivy_array(y)))

    @with_supported_dtypes(
        {"2.5.1 and below": ("float32", "float64", "int32", "int64")}, "paddle"
    )
    def max(self, axis=None, keepdim=False, name=None):
        return paddle_frontend.Tensor(
            ivy.max(self._ivy_array, axis=axis, keepdims=keepdim)
        )

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def deg2rad(self, name=None):
        return paddle_frontend.Tensor(ivy.deg2rad(self._ivy_array))

    @with_supported_dtypes(
        {"2.5.1 and below": ("float32", "float64", "int32", "int64", "bool")}, "paddle"
    )
    def rot90(self, k=1, axes=(0, 1), name=None):
        return paddle_frontend.Tensor(ivy.rot90(self._ivy_array, k=k, axes=axes))

    @with_supported_dtypes(
        {"2.5.1 and below": ("complex64", "complex128")},
        "paddle",
    )
    def imag(self, name=None):
        return paddle_frontend.imag(self)

    def is_tensor(self):
        return paddle_frontend.is_tensor(self._ivy_array)

    @with_supported_dtypes(
        {
            "2.5.1 and below": (
                "float32",
                "float64",
            )
        },
        "paddle",
    )
    def isclose(self, y, rtol=1e-05, atol=1e-08, equal_nan=False, name=None):
        return paddle_frontend.isclose(
            self, y, rtol=rtol, atol=atol, equal_nan=equal_nan
        )

    @with_supported_dtypes({"2.5.1 and below": ("int32", "int64")}, "paddle")
    def floor_divide(self, y, name=None):
        return paddle_frontend.Tensor(
            ivy.floor_divide(self._ivy_array, _to_ivy_array(y))
        )

    # cond
    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def cond(self, p=None, name=None):
        return paddle_frontend.cond(self, p=p, name=name)

    @with_unsupported_dtypes({"2.4.2 and below": ("int16", "float16")}, "paddle")
    def conj(self, name=None):
        return paddle_frontend.Tensor(ivy.conj(self._ivy_array))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def log2(self, name=None):
        return paddle_frontend.Tensor(ivy.log2(self._ivy_array))

    @with_unsupported_dtypes(
        {"2.4.2 and below": ("float32", "float64", "int32", "int64")}, "paddle"
    )
    def neg(self, name=None):
        return paddle_frontend.neg(self)

    @with_supported_dtypes(
        {
            "2.5.1 and below": (
                "bool",
                "int8",
                "int16",
                "int32",
                "int64",
                "float32",
                "float64",
            )
        },
        "paddle",
    )
    def logical_not(self, out=None, name=None):
        return paddle_frontend.Tensor(ivy.logical_not(self.ivy_array))

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def sign(self, name=None):
        return ivy.sign(self._ivy_array)

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def var(self, axis=None, unbiased=True, keepdim=False, name=None):
        return paddle_frontend.Tensor(
            ivy.var(
                self._ivy_array, axis=axis, correction=int(unbiased), keepdims=keepdim
            )
        )

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def sgn(self, name=None):
        return paddle_frontend.Tensor(ivy.sign(self._ivy_array, np_variant=True))

    def tolist(self):
        return paddle_frontend.Tensor(ivy.to_list(self._ivy_array))

    @with_supported_dtypes(
        {"2.5.1 and below": ("float32", "float64", "int32", "int64")},
        "paddle",
    )
    def min(self, axis=None, keepdim=False, name=None):
        return ivy.min(self._ivy_array, axis=axis, keepdims=keepdim)

    @with_supported_dtypes(
        {"2.5.1 and below": ("int32", "int64", "float32", "float64")}, "paddle"
    )
    def pow(self, y, name=None):
        return paddle_frontend.Tensor(ivy.pow(self._ivy_array, _to_ivy_array(y)))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def atan(self, name=None):
        return ivy.atan(self._ivy_array)

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def atanh(self, name=None):
        return ivy.atanh(self._ivy_array)

    @with_unsupported_dtypes({"2.4.2 and below": ("float32", "float64")}, "paddle")
    def std(self, axis=None, unbiased=True, keepdim=False, name=None):
        return paddle_frontend.Tensor(
            ivy.std(self._ivy_array, axis=axis, keepdims=keepdim)
        )

    @with_supported_dtypes(
        {"2.5.1 and below": ("int32", "int64", "float32", "float64")}, "paddle"
    )
    def trunc(self, name=None):
        return paddle_frontend.Tensor(ivy.trunc(self._ivy_array))

    @with_supported_dtypes({"2.5.1 and below": ("float32", "float64")}, "paddle")
    def stanh(self, scale_a=0.67, scale_b=1.7159, name=None):
        return paddle_frontend.stanh(self, scale_a=scale_a, scale_b=scale_b)

    @with_supported_dtypes(
        {"2.5.1 and below": ("int32", "int64", "float32", "float64")}, "paddle"
    )
    def trace(self, offset=0, axis1=0, axis2=1, name=None):
        return paddle_frontend.Tensor(
            ivy.trace(self._ivy_array, offset=offset, axis1=axis1, axis2=axis2)
        )

    @with_supported_dtypes(
        {"2.5.1 and below": ("float32", "float64", "int16", "int32", "int64", "uint8")},
        "paddle",
    )
    def argmin(self, axis=None, keepdim=False, dtype=None, name=None):
        return paddle_frontend.argmin(
            self._ivy_array, axis=axis, keepdim=keepdim, dtype=dtype
        )

    @with_supported_dtypes(
        {"2.5.1 and below": ("float32", "float64", "int32", "int64")},
        "paddle",
    )
    def topk(self, k, axis=None, largest=True, sorted=True, name=None):
        return ivy.top_k(self._ivy_array, k, axis=axis, largest=largest, sorted=sorted)

    @with_unsupported_dtypes({"2.5.1 and below": ("float16", "bfloat16")}, "paddle")
    def remainder(self, y, name=None):
        return ivy.remainder(self._ivy_array, y)

    def is_floating_point(self):
        return paddle_frontend.is_floating_point(self._ivy_array)
