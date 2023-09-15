from typing import Optional, Union, Literal

# global
import torch
import torch.nn

# local
import ivy
from ivy.func_wrapper import with_unsupported_dtypes
from . import backend_version


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, backend_version)
def logit(
    x: torch.Tensor,
    /,
    *,
    eps: Optional[float] = None,
    complex_mode: Literal["split", "magnitude", "jax"] = "jax",
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    return torch.logit(x, eps=eps, out=out)


@with_unsupported_dtypes({"2.0.1 and below": ("complex", "float16")}, backend_version)
def thresholded_relu(
    x: torch.Tensor,
    /,
    *,
    threshold: Optional[Union[int, float]] = None,
    out: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    return torch.threshold(x, threshold=threshold, value=0)


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, backend_version)
def relu6(
    x: torch.Tensor, /, *, complex_mode="jax", out: Optional[torch.Tensor] = None
) -> torch.Tensor:
    return torch.nn.functional.relu6(x)


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, backend_version)
def logsigmoid(
    input: torch.Tensor, /, *, complex_mode="jax", out: Optional[torch.Tensor] = None
) -> torch.Tensor:
    if torch.is_complex(input):
        return torch.log(torch.sigmoid(input))
    return torch.nn.functional.logsigmoid(input)


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, backend_version)
def selu(x: torch.Tensor, /, *, out: Optional[torch.Tensor] = None) -> torch.Tensor:
    ret = torch.nn.functional.selu(x)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret).astype(x.dtype)
    return ivy.astype(ret, x.dtype)


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, backend_version)
def silu(x: torch.Tensor, /, *, out: Optional[torch.Tensor] = None) -> torch.Tensor:
    return torch.nn.functional.silu(x)


@with_unsupported_dtypes({"2.0.1 and below": ("float16",)}, backend_version)
def elu(
    x: torch.Tensor, /, *, alpha: float = 1.0, out: Optional[torch.Tensor] = None
) -> torch.Tensor:
    ret = torch.nn.functional.elu(x, alpha)
    if ivy.exists(out):
        return ivy.inplace_update(out, ret).astype(x.dtype)
    return ivy.astype(ret, x.dtype)
