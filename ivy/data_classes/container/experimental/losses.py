# global
from typing import Optional, Union, List, Dict

# local
import ivy
from ivy.data_classes.container.base import ContainerBase


class _ContainerWithLossesExperimental(ContainerBase):
    @staticmethod
    def _static_l1_loss(
        input: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        target: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.l1_loss. This method simply wraps the
        function, and so the docstring for ivy.l1_loss also applies to this method with
        minimal changes.

        Parameters
        ----------
        input
            input array or container.
        target
            input array or container containing the targeted values.
        reduction
            ``'mean'``: The output will be averaged.
            ``'sum'``: The output will be summed.
            ``'none'``: No reduction will be applied to the output. Default: ``'mean'``.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If input, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``input``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The L1 loss between the input array and the targeted values.

        Examples
        --------
        With :class:`ivy.Container` inputs:

        >>> x = ivy.Container(a=ivy.array([1, 2, 3]), b=ivy.array([4, 5, 6]))
        >>> y = ivy.Container(a=ivy.array([2, 2, 2]), b=ivy.array([5, 5, 5]))
        >>> z = ivy.Container.static_l1_loss(x, y)
        >>> print(z)
        {
            a: ivy.array(1.),
            b: ivy.array(0.)
        }

        With a mix of :class:`ivy.Array` and :class:`ivy.Container` inputs:

        >>> x = ivy.array([1, 2, 3])
        >>> y = ivy.Container(a=ivy.array([2, 2, 2]), b=ivy.array([5, 5, 5]))
        >>> z = ivy.Container.static_l1_loss(x, y)
        >>> print(z)
        {
            a: ivy.array(1.),
            b: ivy.array(4.)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "l1_loss",
            input,
            target,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def l1_loss(
        self: ivy.Container,
        target: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.l1_loss. This method simply wraps
        the function, and so the docstring for ivy.l1_loss also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input container.
        target
            input array or container containing the targeticted values.
        reduction
            ``'mean'``: The output will be averaged.
            ``'sum'``: The output will be summed.
            ``'none'``: No reduction will be applied to the output. Default: ``'mean'``.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If input, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``input``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The L1 loss between the input array and the targeticted values.

        Examples
        --------
        >>> x = ivy.Container(a=ivy.array([1, 2, 3]), b=ivy.array([4, 5, 6]))
        >>> y = ivy.Container(a=ivy.array([2, 2, 2]), b=ivy.array([5, 5, 5]))
        >>> z = x.l1_loss(y)
        >>> print(z)
        {
            a: ivy.array(1.),
            b: ivy.array(0.)
        }
        """
        return self._static_l1_loss(
            self,
            target,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_log_poisson_loss(
        input: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        target: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        compute_full_loss: bool = False,
        axis: int = -1,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.log_poisson_loss. This method simply
        wraps the function, and so the docstring for ivy.log_poisson_loss also applies
        to this method with minimal changes.

        Parameters
        ----------
        input
            input array or container.
        target
            input array or container containing the targeted values.
        compute_full_loss
            whether to compute the full loss. If false, a constant term is dropped
            in favor of more efficient optimization. Default: ``False``.
        axis
            the axis along which to compute the log-likelihood loss. If axis is ``-1``,
            the log-likelihood loss will be computed along the last dimension.
            Default: ``-1``.
        reduction
            ``'mean'``: The output will be averaged.
            ``'sum'``: The output will be summed.
            ``'none'``: No reduction will be applied to the output. Default: ``'none'``.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If input, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``input``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The L1 loss between the input array and the targeted values.

        Examples
        --------
        With :class:`ivy.Container` inputs:

        >>> x = ivy.Container(a=ivy.array([1, 2, 3]), b=ivy.array([4, 5, 6]))
        >>> y = ivy.Container(a=ivy.array([2, 2, 2]), b=ivy.array([5, 5, 5]))
        >>> z = ivy.Container.static_log_poisson_loss(x, y, reduction='mean')
        >>> print(z)
        {
            a: ivy.array(1.),
            b: ivy.array(0.)
        }

        With a mix of :class:`ivy.Array` and :class:`ivy.Container` inputs:

        >>> x = ivy.array([1, 2, 3])
        >>> y = ivy.Container(a=ivy.array([2, 2, 2]), b=ivy.array([5, 5, 5]))
        >>> z = ivy.Container.static_log_poisson_loss(x, y, reduction='mean')
        >>> print(z)
        {
            a: ivy.array(1.),
            b: ivy.array(4.)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "log_poisson_loss",
            input,
            target,
            compute_full_loss=compute_full_loss,
            axis=axis,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def log_poisson_loss(
        self: ivy.Container,
        target: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        compute_full_loss: bool = False,
        axis: int = -1,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.log_poisson_loss. This method
        simply wraps the function, and so the docstring for ivy.log_poisson_loss also
        applies to this method with minimal changes.

        Parameters
        ----------
        self
            input container.
        target
            input array or container containing the targeticted values.
        compute_full_loss
            whether to compute the full loss. If false, a constant term is dropped
            in favor of more efficient optimization. Default: ``False``.
        axis
            the axis along which to compute the log-likelihood loss. If axis is ``-1``,
            the log-likelihood loss will be computed along the last dimension.
            Default: ``-1``.
        reduction
            ``'mean'``: The output will be averaged.
            ``'sum'``: The output will be summed.
            ``'none'``: No reduction will be applied to the output. Default: ``'none'``.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If input, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``input``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The L1 loss between the input array and the targeticted values.

        Examples
        --------
        >>> x = ivy.Container(a=ivy.array([1, 2, 3]), b=ivy.array([4, 5, 6]))
        >>> y = ivy.Container(a=ivy.array([2, 2, 2]), b=ivy.array([5, 5, 5]))
        >>> z = x.log_poisson_loss(y)
        >>> print(z)
        {
            a: ivy.array(1.),
            b: ivy.array(0.)
        }
        """
        return self._static_log_poisson_loss(
            self,
            target,
            compute_full_loss=compute_full_loss,
            axis=axis,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_smooth_l1_loss(
        input: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        target: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        beta: Optional[Union[float, ivy.Container]] = 1.0,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.smooth_l1_loss. This method simply
        wraps the function, and so the docstring for ivy. smooth_l1_loss also applies to
        this method with minimal changes.

        Parameters
        ----------
        input
            input array or container containing input labels.
        target
            input array or container containing the targeticted labels.
        beta
            a positive float value that sets the smoothness threshold.
            Default: ``1.0``.
        reduction
            ``'none'``: No reduction will be applied to the output.
            ``'mean'``: The output will be averaged.
            ``'sum'``: The output will be summed. Default: ``'mean'``.
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If input, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``input``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The smooth L1 loss between the input array and the targeticted labels.

        Examples
        --------
        With :class:`ivy.Container` inputs:

        >>> x = ivy.Container(a=ivy.array([1, 0, 2]), b=ivy.array([3, 2, 1]))
        >>> y = ivy.Container(a=ivy.array([0.6, 0.2, 0.3]),
        b=ivy.array([0.8, 0.2, 0.2]))
        >>> z = ivy.Container.static_smooth_l1_loss(x, y)
        >>> print(z)
        {
            a: ivy.array(0.9),
            b: ivy.array(0.25)
        }

        With a mix of :class:`ivy.Array` and :class:`ivy.Container` inputs:

        >>> x = ivy.array([1 , 0, 2])
        >>> y = ivy.Container(a=ivy.array([0.6, 0.2, 0.3]),
        b=ivy.array([0.8, 0.2, 0.2]))
        >>> z = ivy.Container.static_smooth_l1_loss(x, y)
        >>> print(z)
        {
            a: ivy.array(0.9),
            b: ivy.array(0.25)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "smooth_l1_loss",
            input,
            target,
            beta=beta,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def smooth_l1_loss(
        self: ivy.Container,
        target: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        beta: Optional[Union[float, ivy.Container]] = 1.0,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.smooth_l1_loss. This method simply
        wraps the function, and so the docstring for ivy. smooth_l1_loss also applies to
        this method with minimal changes.

        Parameters
        ----------
        self
            input container containing input labels.
        target
            input array or container containing the targeticted labels.
        beta
            a positive float value that sets the smoothness threshold.
            Default: ``1.0``.
        reduction
            ``'none'``: No reduction will be applied to the output.
            ``'mean'``: The output will be averaged.
            ``'sum'``: The output will be summed. Default: ``'mean'``.
        key_chains
            The key-chains to apply or not apply the method to. Default is
            ``None``.
        to_apply
            If input, the method will be applied to key_chains, otherwise
            key_chains
            will be skipped. Default is ``input``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output container, for writing the result to.
            It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The smooth L1 loss between the input array and the targeticted labels.

        Examples
        --------
        >>> x = ivy.Container(a=ivy.array([1, 0, 2]), b=ivy.array([3, 2, 1]))
        >>> y = ivy.Container(a=ivy.array([0.6, 0.2, 0.3]),
        b=ivy.array([0.8, 0.2, 0.2]))
        >>> z = x.smooth_l1_loss(y)
        >>> print(z)
        {
            a: ivy.array(0.9),
            b: ivy.array(0.25)
        }
        """
        return self._static_smooth_l1_loss(
            self,
            target,
            beta=beta,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_huber_loss(
        true: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        pred: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        delta: Optional[Union[float, ivy.Container]] = 1.0,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container static method variant of huber_loss. This method simply wraps the
        function, and so the docstring for huber_loss also applies to this method with
        minimal changes.

        Parameters
        ----------
        true
            true array or container containing true labels.
        pred
            true array or container containing the predicted labels.
        delta
            The threshold parameter that determines the point where the loss transitions
            from squared error to absolute error. Default is 1.0.
        reduction : str, optional
            The type of reduction to apply to the loss.
            Possible values are "mean" (default)
            and "sum".
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If true, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``true``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output container, for writing the result to. It must have a shape
            that the true broadcast to.

        Returns
        -------
        ret
            The Huber loss between the true and predicted values.

        Examples
        --------
        With :class:`ivy.Container` trues:

        >>> x = ivy.Container(a=ivy.array([1, 0, 3]), b=ivy.array([0, 0, 2]))
        >>> y = ivy.Container(a=ivy.array([1.5, 0.2, 2.8]), b=ivy.array([0.5, 0.2, 1.9])
        )
        >>> z = ivy.Container.static_huber_loss(x, y, delta=1.0)
        >>> print(z)
        {
            a: ivy.array(0.0575),
            b: ivy.array(0.005)
        }

        With a mix of :class:`ivy.Array` and :class:`ivy.Container` trues:

        >>> x = ivy.array([1, 0, 3])
        >>> y = ivy.Container(a=ivy.array([1.5, 0.2, 2.8]), b=ivy.array([0.5, 0.2, 1.9])
        )
        >>> z = ivy.Container.static_huber_loss(x, y, delta=1.0)
        >>> print(z)
        {
            a: ivy.array(0.0575),
            b: ivy.array(0.005)
        }
        """
        return ContainerBase.cont_multi_map_in_function(
            "huber_loss",
            true,
            pred,
            delta=delta,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def huber_loss(
        self: ivy.Container,
        pred: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        delta: Optional[Union[float, ivy.Container]] = 1.0,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of huber_loss. This method simply wraps
        the function, and so the docstring for huber_loss also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            true container containing true labels.
        pred
            true array or container containing the predicted labels.
        delta
            The threshold parameter that determines the point where the loss transitions
            from squared error to absolute error. Default is 1.0.
        reduction : str, optional
            The type of reduction to apply to the loss.
            Possible values are "mean" (default)
            and "sum".
        key_chains
            The key-chains to apply or not apply the method to. Default is ``None``.
        to_apply
            If true, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is ``true``.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is ``False``.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is ``False``.
        out
            optional output container, for writing the result to. It must have a shape
            that the trues broadcast to.

        Returns
        -------
        ret
            The Huber loss between the true and predicted values.

        Examples
        --------
        >>> x = ivy.Container(a=ivy.array([1, 0, 3]), b=ivy.array([0, 0, 2]))
        >>> y = ivy.Container(a=ivy.array([1.5, 0.2, 2.8]), b=ivy.array([0.5, 0.2, 1.9])
        )
        >>> z = x.huber_loss(y, delta=1.0)
        >>> print(z)
        {
            a: ivy.array(0.0575),
            b: ivy.array(0.005)
        }
        """
        return self._static_huber_loss(
            self,
            pred,
            delta=delta,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_soft_margin_loss(
        input: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        target: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.soft_margin_loss. This method simply
        wraps the function, and so the docstring for ivy.soft_margin_loss also applies
        to this method with minimal changes.

        # Insert the docstring here

        Parameters
        ----------
        input
            input array or container containing input labels.
        target
            input array or container containing the targeticted labels.
        reduction
            the reduction method. Default: "mean".
        key_chains
            The key-chains to apply or not apply the method to. Default is None.
        to_apply
            If input, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is input.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is False.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is False.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The soft margin loss between the given distributions.
        """
        return ContainerBase.cont_multi_map_in_function(
            "soft_margin_loss",
            input,
            target,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def soft_margin_loss(
        self: ivy.Container,
        target: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.soft_margin_loss. This method
        simply wraps the function, and so the docstring for ivy.soft_margin_loss also
        applies to this method with minimal changes.

        # Insert the docstring here

        Parameters
        ----------
        self
            input container containing input labels.
        target
            input array or container containing the targeticted labels.
        reduction
            the reduction method. Default: "mean".
        key_chains
            The key-chains to apply or not apply the method to. Default is None.
        to_apply
            If input, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is input.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is False.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is False.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The soft margin loss between the given distributions.
        """
        return self._static_soft_margin_loss(
            self,
            target,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    @staticmethod
    def _static_kl_div(
        input: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        target: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container static method variant of ivy.kl_div. This method simply wraps the
        function, and so the docstring for ivy.kl_div also applies to this method with
        minimal changes.

        Parameters
        ----------
        input
            input array or container containing input distribution.
        target
            input array or container containing target distribution.
        reduction
            the reduction method. Default: "mean".
        key_chains
            The key-chains to apply or not apply the method to. Default is None.
        to_apply
            If input, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is input.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is False.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is False.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The Kullback-Leibler divergence loss between the given distributions.
        """
        return ContainerBase.cont_multi_map_in_function(
            "kl_div",
            input,
            target,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )

    def kl_div(
        self: ivy.Container,
        target: Union[ivy.Container, ivy.Array, ivy.NativeArray],
        /,
        *,
        reduction: Optional[Union[str, ivy.Container]] = "mean",
        key_chains: Optional[Union[List[str], Dict[str, str], ivy.Container]] = None,
        to_apply: Union[bool, ivy.Container] = True,
        prune_unapplied: Union[bool, ivy.Container] = False,
        map_sequences: Union[bool, ivy.Container] = False,
        out: Optional[ivy.Container] = None,
    ) -> ivy.Container:
        """
        ivy.Container instance method variant of ivy.kl_div. This method simply wraps
        the function, and so the docstring for ivy.kl_div also applies to this method
        with minimal changes.

        Parameters
        ----------
        self
            input container containing input distribution.
        target
            input array or container containing target distribution.
        reduction
            the reduction method. Default: "mean".
        key_chains
            The key-chains to apply or not apply the method to. Default is None.
        to_apply
            If input, the method will be applied to key_chains, otherwise key_chains
            will be skipped. Default is input.
        prune_unapplied
            Whether to prune key_chains for which the function was not applied.
            Default is False.
        map_sequences
            Whether to also map method to sequences (lists, tuples).
            Default is False.
        out
            optional output container, for writing the result to. It must have a shape
            that the inputs broadcast to.

        Returns
        -------
        ret
            The Kullback-Leibler divergence loss between the given distributions.
        """
        return self._static_kl_div(
            self,
            target,
            reduction=reduction,
            key_chains=key_chains,
            to_apply=to_apply,
            prune_unapplied=prune_unapplied,
            map_sequences=map_sequences,
            out=out,
        )
