import ivy
from _utils import WeightedMedianCalculator
import numpy as np


EPSILON = 10 * np.finfo("double").eps


class Criterion:
    """
    Interface for impurity criteria.

    This object stores methods on how to calculate how good a split is
    using different metrics.
    """

    def __getstate__(self):
        return {}

    def __setstate__(self, d):
        pass

    def init(
        self,
        y,
        sample_weight,
        weighted_n_samples: float,
        sample_indices: list,
        start: int,
        end: int,
    ):
        """
        Placeholder for a method which will initialize the criterion.

        Returns -1 in case of failure to allocate memory (and raise MemoryError)
        or 0 otherwise.

        Parameters
        ----------
        y : ndarray, dtype=DOUBLE_t
            y is a buffer that can store values for n_outputs target variables
            stored as a Cython memoryview.
        sample_weight : ndarray, dtype=DOUBLE_t
            The weight of each sample stored as a Cython memoryview.
        weighted_n_samples : double
            The total weight of the samples being considered
        sample_indices : ndarray, dtype=SIZE_t
            A mask on the samples. Indices of the samples in X and y we want to use,
            where sample_indices[start:end] correspond to the samples in this node.
        start : SIZE_t
            The first sample to be used on this node
        end : SIZE_t
            The last sample used on this node
        """
        pass

    def init_missing(self, n_missing):
        """
        Initialize sum_missing if there are missing values.

        This method assumes that caller placed the missing samples in
        self.sample_indices[-n_missing:]

        Parameters
        ----------
        n_missing: SIZE_t
            Number of missing values for specific feature.
        """
        pass

    def reset(self):
        """
        Reset the criterion at pos=start.

        This method must be implemented by the subclass.
        """
        pass

    def reverse_reset(self):
        """
        Reset the criterion at pos=end.

        This method must be implemented by the subclass.
        """
        pass

    def update(self, new_pos):
        """
        Updated statistics by moving sample_indices[pos:new_pos] to the left child.

        This updates the collected statistics by moving sample_indices[pos:new_pos]
        from the right child to the left child. It must be implemented by
        the subclass.

        Parameters
        ----------
        new_pos : SIZE_t
            New starting index position of the sample_indices in the right child
        """
        pass

    def node_impurity(self):
        """
        Placeholder for calculating the impurity of the node.

        Placeholder for a method which will evaluate the impurity of the
        current node, i.e. the impurity of sample_indices[start:end].
        This is the primary function of the criterion class. The smaller
        the impurity the better.
        """
        pass

    def children_impurity(self, impurity_left, impurity_right):
        """
        Placeholder for calculating the impurity of children.

        Placeholder for a method which evaluates the impurity in
        children nodes, i.e. the impurity of sample_indices[start:pos] + the impurity
        of sample_indices[pos:end].

        Parameters
        ----------
        impurity_left : double pointer
            The memory address where the impurity of the left child should be
            stored.
        impurity_right : double pointer
            The memory address where the impurity of the right child should be
            stored
        """
        pass

    def node_value(self, dest):
        """
        Placeholder for storing the node value.

        Placeholder for a method which will compute the node value
        of sample_indices[start:end] and save the value into dest.

        Parameters
        ----------
        dest : double pointer
            The memory address where the node value should be stored.
        """
        pass

    def proxy_impurity_improvement(self):
        """
        Compute a proxy of the impurity reduction.

        This method is used to speed up the search for the best split.
        It is a proxy quantity such that the split that maximizes this
        value also maximizes the impurity improvement. It neglects all
        constant terms of the impurity decrease for a given split.

        The absolute impurity improvement is only computed by the
        impurity_improvement method once the best split has been found.
        """

        impurity_left = 0.0
        impurity_right = 0.0
        impurity_left, impurity_right = self.children_impurity(
            impurity_left, impurity_right
        )

        return (
            -self.weighted_n_right * impurity_right
            - self.weighted_n_left * impurity_left
        )

    def impurity_improvement(
        self, impurity_parent: float, impurity_left: float, impurity_right: float
    ):
        """
        Compute the improvement in impurity.

        This method computes the improvement in impurity when a split occurs.
        The weighted impurity improvement equation is the following:

        N_t / N * (impurity - N_t_R / N_t * right_impurity
                            - N_t_L / N_t * left_impurity)

        where N is the total number of samples, N_t is the number of samples
        at the current node, N_t_L is the number of samples in the left child,
        and N_t_R is the number of samples in the right child.

        Parameters
        ----------
        impurity_parent : double
            The initial impurity of the parent node before the split

        impurity_left : double
            The impurity of the left child

        impurity_right : double
            The impurity of the right child

        Return
        ------
        double : improvement in impurity after the split occurs
        """
        return (self.weighted_n_node_samples / self.weighted_n_samples) * (
            impurity_parent
            - (self.weighted_n_right / self.weighted_n_node_samples) * impurity_right
            - (self.weighted_n_left / self.weighted_n_node_samples) * impurity_left
        )

    def init_sum_missing(self):
        """Init sum_missing to hold sums for missing values."""
        pass


class FriedmanMSE:
    def __init__(self, n_outputs):
        self.n_outputs = n_outputs

    def proxy_impurity_improvement(self):
        total_sum_left = 0.0
        total_sum_right = 0.0

        for k in range(self.n_outputs):
            total_sum_left += self.sum_left[k]
            total_sum_right += self.sum_right[k]

        diff = (
            self.weighted_n_right * total_sum_left
            - self.weighted_n_left * total_sum_right
        )

        return diff * diff / (self.weighted_n_left * self.weighted_n_right)

    def impurity_improvement(self, impurity_parent, impurity_left, impurity_right):
        total_sum_left = 0.0
        total_sum_right = 0.0

        for k in range(self.n_outputs):
            total_sum_left += self.sum_left[k]
            total_sum_right += self.sum_right[k]

        diff = (
            self.weighted_n_right * total_sum_left
            - self.weighted_n_left * total_sum_right
        ) / self.n_outputs

        return (
            diff
            * diff
            / (
                self.weighted_n_left
                * self.weighted_n_right
                * self.weighted_n_node_samples
            )
        )


class Poisson:
    def __init__(self, n_outputs):
        self.n_outputs = n_outputs

    def node_impurity(self):
        return self.poisson_loss(
            self.start, self.end, self.sum_total, self.weighted_n_node_samples
        )

    def proxy_impurity_improvement(self):
        proxy_impurity_left = 0.0
        proxy_impurity_right = 0.0

        for k in range(self.n_outputs):
            if (self.sum_left[k] <= EPSILON) or (self.sum_right[k] <= EPSILON):
                return -ivy.inf
            else:
                y_mean_left = self.sum_left[k] / self.weighted_n_left
                y_mean_right = self.sum_right[k] / self.weighted_n_right
                proxy_impurity_left -= self.sum_left[k] * ivy.log(y_mean_left)
                proxy_impurity_right -= self.sum_right[k] * ivy.log(y_mean_right)

        return -proxy_impurity_left - proxy_impurity_right

    def children_impurity(self, impurity_left, impurity_right):
        start = self.start
        pos = self.pos
        end = self.end

        impurity_left[0] = self.poisson_loss(
            start, pos, self.sum_left, self.weighted_n_left
        )
        impurity_right[0] = self.poisson_loss(
            pos, end, self.sum_right, self.weighted_n_right
        )

    def poisson_loss(self, start, end, y_sum, weight_sum):
        y_mean = 0.0
        poisson_loss = 0.0
        w = 1.0

        for k in range(self.n_outputs):
            if y_sum[k] <= EPSILON:
                return ivy.inf

            y_mean = y_sum[k] / weight_sum

            for p in range(start, end):
                i = self.sample_indices[p]

                if self.sample_weight is not None:
                    w = self.sample_weight[i]

                poisson_loss += w * self.y[i, k] * ivy.log(self.y[i, k] / y_mean)

        return poisson_loss / (weight_sum * self.n_outputs)


class ClassificationCriterion(Criterion):
    def __init__(self, n_outputs, n_classes):
        self.start = 0
        self.pos = 0
        self.end = 0
        self.missing_go_to_left = 0

        self.n_outputs = n_outputs
        self.n_samples = 0
        self.n_node_samples = 0
        self.weighted_n_node_samples = 0.0
        self.weighted_n_left = 0.0
        self.weighted_n_right = 0.0
        self.weighted_n_missing = 0.0

        self.n_classes = ivy.empty(n_outputs, dtype=ivy.intp)

        max_n_classes = 0

        # For each target, set the number of unique classes in that target,
        # and also compute the maximal stride of all targets
        for k in range(n_outputs):
            self.n_classes[k] = n_classes[k]

            if n_classes[k] > max_n_classes:
                max_n_classes = n_classes[k]

        self.max_n_classes = max_n_classes

        # Count labels for each output
        self.sum_total = ivy.zeros((n_outputs, max_n_classes), dtype=ivy.float64)
        self.sum_left = ivy.zeros((n_outputs, max_n_classes), dtype=ivy.float64)
        self.sum_right = ivy.zeros((n_outputs, max_n_classes), dtype=ivy.float64)

    def init(self, y, sample_weight, weighted_n_samples, sample_indices, start, end):
        self.y = y
        self.sample_weight = sample_weight
        self.sample_indices = sample_indices
        self.start = start
        self.end = end
        self.n_node_samples = end - start
        self.weighted_n_samples = weighted_n_samples
        self.weighted_n_node_samples = 0.0

        for k in range(self.n_outputs):
            self.sum_total[k, :] = 0.0

        for p in range(start, end):
            i = sample_indices[p]
            w = 1.0

            if sample_weight is not None:
                w = sample_weight[i]

            for k in range(self.n_outputs):
                c = int(self.y[i, k])
                self.sum_total[k, c] += w

            self.weighted_n_node_samples += w

        self.reset()
        return 0

    def init_sum_missing(self):
        self.sum_missing = ivy.zeros(
            (self.n_outputs, self.max_n_classes), dtype=ivy.float64
        )

    def init_missing(self, n_missing):
        w = 1.0

        self.n_missing = n_missing
        if n_missing == 0:
            return

        self.sum_missing[:, :] = 0.0
        self.weighted_n_missing = 0.0

        for p in range(self.end - n_missing, self.end):
            i = self.sample_indices[p]
            if self.sample_weight is not None:
                w = self.sample_weight[i]

            for k in range(self.n_outputs):
                c = int(self.y[i, k])
                self.sum_missing[k, c] += w

            self.weighted_n_missing += w

    def reset(self):
        self.pos = self.start
        _move_sums_classification(
            self,
            self.sum_left,
            self.sum_right,
            self.weighted_n_left,
            self.weighted_n_right,
            self.missing_go_to_left,
        )
        return 0

    def reverse_reset(self):
        self.pos = self.end
        _move_sums_classification(
            self,
            self.sum_right,
            self.sum_left,
            self.weighted_n_right,
            self.weighted_n_left,
            not self.missing_go_to_left,
        )
        return 0

    def update(self, new_pos):
        pos = self.pos

        end_non_missing = self.end - self.n_missing

        sample_indices = self.sample_indices
        sample_weight = self.sample_weight

        for k in range(self.n_outputs):
            for c in range(self.max_n_classes):
                self.sum_left[k, c] = 0.0
                self.sum_right[k, c] = 0.0

        if (new_pos - pos) <= (end_non_missing - new_pos):
            for p in range(pos, new_pos):
                i = sample_indices[p]

                w = 1.0

                if sample_weight is not None:
                    w = sample_weight[i]

                for k in range(self.n_outputs):
                    c = int(self.y[i, k])
                    self.sum_left[k, c] += w

                self.weighted_n_left += w

        else:
            self.reverse_reset()

            for p in range(end_non_missing - 1, new_pos - 1, -1):
                i = sample_indices[p]

                w = 1.0

                if sample_weight is not None:
                    w = sample_weight[i]

                for k in range(self.n_outputs):
                    c = int(self.y[i, k])
                    self.sum_left[k, c] -= w

                self.weighted_n_left -= w

        self.weighted_n_right = self.weighted_n_node_samples - self.weighted_n_left

        for k in range(self.n_outputs):
            for c in range(self.max_n_classes):
                self.sum_right[k, c] = self.sum_total[k, c] - self.sum_left[k, c]

        self.pos = new_pos
        return 0

    def node_impurity(self):
        pass

    def children_impurity(self, impurity_left, impurity_right):
        pass

    def node_value(self, dest):
        for k in range(self.n_outputs):
            dest[:] = self.sum_total[k, :]
            dest += self.max_n_classes


class RegressionCriterion(Criterion):
    """
    Abstract regression criterion for regression problems.

    This handles cases where the target is a continuous value and is
    evaluated by computing the variance of the target values left and
    right of the split point.
    """

    def __init__(self, n_outputs, n_samples):
        """
        Initialize parameters for this criterion.

        Parameters
        ----------
        n_outputs : int
            The number of targets to be predicted

        n_samples : int
            The total number of samples to fit on
        """
        self.start = 0
        self.pos = 0
        self.end = 0
        self.n_outputs = n_outputs
        self.n_samples = n_samples
        self.n_node_samples = 0
        self.weighted_n_node_samples = 0.0
        self.weighted_n_left = 0.0
        self.weighted_n_right = 0.0
        self.weighted_n_missing = 0.0
        self.sq_sum_total = 0.0
        self.sum_total = ivy.zeros(n_outputs, dtype=ivy.float64)
        self.sum_left = ivy.zeros(n_outputs, dtype=ivy.float64)
        self.sum_right = ivy.zeros(n_outputs, dtype=ivy.float64)

    def init(self, y, sample_weight, weighted_n_samples, sample_indices, start, end):
        """
        Initialize the criterion.

        This initializes the criterion at node sample_indices[start:end]
        and children sample_indices[start:start] and
        sample_indices[start:end].
        """
        self.y = y
        self.sample_weight = sample_weight
        self.sample_indices = sample_indices
        self.start = start
        self.end = end
        self.n_node_samples = end - start
        self.weighted_n_samples = weighted_n_samples
        self.weighted_n_node_samples = 0.0
        self.sq_sum_total = 0.0
        self.sum_total.fill(0.0)

        for p in range(start, end):
            i = sample_indices[p]
            w = sample_weight[i] if sample_weight is not None else 1.0
            for k in range(self.n_outputs):
                y_ik = self.y[i, k]
                w_y_ik = w * y_ik
                self.sum_total[k] += w_y_ik
                self.sq_sum_total += w_y_ik * y_ik

            self.weighted_n_node_samples += w

        self.reset()
        return 0

    def init_sum_missing(self):
        """Initialize sum_missing to hold sums for missing values."""
        self.sum_missing = ivy.zeros(self.n_outputs, dtype=ivy.float64)

    def init_missing(self, n_missing):
        """Initialize sum_missing if there are missing values."""
        self.n_missing = n_missing
        if n_missing == 0:
            return

        self.sum_missing.fill(0.0)
        self.weighted_n_missing = 0.0

        for p in range(self.end - n_missing, self.end):
            i = self.sample_indices[p]
            w = self.sample_weight[i] if self.sample_weight is not None else 1.0

            for k in range(self.n_outputs):
                y_ik = self.y[i, k]
                w_y_ik = w * y_ik
                self.sum_missing[k] += w_y_ik

            self.weighted_n_missing += w

    def reset(self):
        """Reset the criterion at pos=start."""
        self.pos = self.start
        self._move_sums_regression(
            self.sum_left,
            self.sum_right,
            self.weighted_n_left,
            self.weighted_n_right,
            self.missing_go_to_left,
        )
        return 0

    def reverse_reset(self):
        """Reset the criterion at pos=end."""
        self.pos = self.end
        self._move_sums_regression(
            self.sum_right,
            self.sum_left,
            self.weighted_n_right,
            self.weighted_n_left,
            not self.missing_go_to_left,
        )
        return 0

    def update(self, new_pos):
        """Update statistics by moving sample_indices[pos:new_pos] to the left."""
        sample_weight = self.sample_weight
        sample_indices = self.sample_indices
        pos = self.pos

        end_non_missing = self.end - self.n_missing

        for k in range(self.n_outputs):
            self.sum_left[k] = 0.0

        w = 1.0

        if (new_pos - pos) <= (end_non_missing - new_pos):
            for p in range(pos, new_pos):
                i = sample_indices[p]
                w = sample_weight[i] if sample_weight is not None else 1.0
                for k in range(self.n_outputs):
                    self.sum_left[k] += w * self.y[i, k]
                self.weighted_n_left += w
        else:
            self.reverse_reset()
            for p in range(end_non_missing - 1, new_pos - 1, -1):
                i = sample_indices[p]
                w = sample_weight[i] if sample_weight is not None else 1.0
                for k in range(self.n_outputs):
                    self.sum_left[k] -= w * self.y[i, k]
                self.weighted_n_left -= w

        self.weighted_n_right = self.weighted_n_node_samples - self.weighted_n_left

        for k in range(self.n_outputs):
            self.sum_right[k] = self.sum_total[k] - self.sum_left[k]

        self.pos = new_pos
        return 0

    def node_impurity(self):
        pass

    def children_impurity(self):
        pass

    def node_value(self, dest):
        for k in range(self.n_outputs):
            dest[k] = self.sum_total[k] / self.weighted_n_node_samples

    def _move_sums_regression(
        self, sum_1, sum_2, weighted_n_1, weighted_n_2, put_missing_in_1
    ):
        """
        Distribute sum_total and sum_missing into sum_1 and sum_2.

        If there are missing values and:
        - put_missing_in_1 is True, then missing values go to sum_1.
        - put_missing_in_1 is False, then missing values go to sum_2.
        """
        has_missing = self.n_missing != 0

        if has_missing and put_missing_in_1:
            for k in range(self.n_outputs):
                sum_1[k] = self.sum_missing[k]

            weighted_n_1[0] = self.weighted_n_missing
            weighted_n_2[0] = self.weighted_n_node_samples - self.weighted_n_missing
        else:
            for k in range(self.n_outputs):
                sum_1[k] = 0.0

            weighted_n_1[0] = 0.0
            weighted_n_2[0] = self.weighted_n_node_samples

        for k in range(self.n_outputs):
            sum_2[k] = self.sum_total[k] - sum_1[k]


class Gini(ClassificationCriterion):
    def node_impurity(self):
        gini = 0.0
        for k in range(self.n_outputs):
            sq_count = 0.0
            for c in range(self.n_classes[k]):
                count_k = self.sum_total[k, c]
                sq_count += count_k * count_k
            gini += 1.0 - sq_count / (
                self.weighted_n_node_samples * self.weighted_n_node_samples
            )
        return gini / self.n_outputs

    def children_impurity(self):
        gini_left = 0.0
        gini_right = 0.0
        for k in range(self.n_outputs):
            sq_count_left = 0.0
            sq_count_right = 0.0
            for c in range(self.n_classes[k]):
                count_k_left = self.sum_left[k, c]
                sq_count_left += count_k_left * count_k_left
                count_k_right = self.sum_right[k, c]
                sq_count_right += count_k_right * count_k_right
            gini_left += 1.0 - sq_count_left / (
                self.weighted_n_left * self.weighted_n_left
            )
            gini_right += 1.0 - sq_count_right / (
                self.weighted_n_right * self.weighted_n_right
            )
        return gini_left / self.n_outputs, gini_right / self.n_outputs


class Entropy(ClassificationCriterion):
    """
    Cross Entropy impurity criterion for classification.

    This handles cases where the target is a classification taking values
    0, 1, ... K-2, K-1. If node m represents a region Rm with Nm observations,
    then let

        count_k = 1 / Nm * sum_{x_i in Rm} I(yi = k)

    be the proportion of class k observations in node m.

    The cross-entropy is then defined as

        cross-entropy = -sum_{k=0}^{K-1} count_k * log(count_k)
    """

    def node_impurity(self):
        """
        Evaluate the impurity of the current node.

        Evaluate the cross-entropy criterion as impurity of the current
        node, i.e., the impurity of sample_indices[start:end]. The
        smaller the impurity the better.
        """
        entropy = 0.0

        for k in range(self.n_outputs):
            for c in range(self.n_classes[k]):
                count_k = self.sum_total[k, c]
                if count_k > 0.0:
                    count_k /= self.weighted_n_node_samples
                    entropy -= count_k * ivy.log(count_k)

        return entropy / self.n_outputs

    def children_impurity(self):
        """
        Evaluate the impurity in children nodes.

        i.e., the impurity of the left child (sample_indices[start:pos]) and the
        impurity of the right child (sample_indices[pos:end]).

        Returns
        -------
        impurity_left : float
            The impurity of the left child
        impurity_right : float
            The impurity of the right child
        """
        entropy_left = 0.0
        entropy_right = 0.0

        for k in range(self.n_outputs):
            for c in range(self.n_classes[k]):
                count_k_left = self.sum_left[k, c]
                count_k_right = self.sum_right[k, c]

                if count_k_left > 0.0:
                    count_k_left /= self.weighted_n_left
                    entropy_left -= count_k_left * ivy.log(count_k_left)

                if count_k_right > 0.0:
                    count_k_right /= self.weighted_n_right
                    entropy_right -= count_k_right * ivy.log(count_k_right)

        return entropy_left / self.n_outputs, entropy_right / self.n_outputs


class MSE(RegressionCriterion):
    """
    Mean squared error impurity criterion.

    MSE = var_left + var_right
    """

    def node_impurity(self):
        impurity = self.sq_sum_total / self.weighted_n_node_samples
        for k in range(self.n_outputs):
            impurity -= (self.sum_total[k] / self.weighted_n_node_samples) ** 2.0
        return impurity / self.n_outputs

    def proxy_impurity_improvement(self):
        proxy_impurity_left = 0.0
        proxy_impurity_right = 0.0
        for k in range(self.n_outputs):
            proxy_impurity_left += self.sum_left[k] * self.sum_left[k]
            proxy_impurity_right += self.sum_right[k] * self.sum_right[k]
        return (
            proxy_impurity_left / self.weighted_n_left
            + proxy_impurity_right / self.weighted_n_right
        )

    def children_impurity(self):
        sample_weight = self.sample_weight
        sample_indices = self.sample_indices
        pos = self.pos
        start = self.start

        sq_sum_left = 0.0
        sq_sum_right = self.sq_sum_total

        for p in range(start, pos):
            i = sample_indices[p]

            if sample_weight is not None:
                w = sample_weight[i]
            else:
                w = 1.0

            for k in range(self.n_outputs):
                sq_sum_left += w * self.y[i, k] * self.y[i, k]

        sq_sum_right = self.sq_sum_total - sq_sum_left

        impurity_left = sq_sum_left / self.weighted_n_left
        impurity_right = sq_sum_right / self.weighted_n_right

        for k in range(self.n_outputs):
            impurity_left -= (self.sum_left[k] / self.weighted_n_left) ** 2.0
            impurity_right -= (self.sum_right[k] / self.weighted_n_right) ** 2.0

        impurity_left /= self.n_outputs
        impurity_right /= self.n_outputs

        return impurity_left, impurity_right

    def node_value(self, dest):
        for k in range(self.n_outputs):
            dest[k] = self.sum_total[k] / self.weighted_n_node_samples


class MAE(RegressionCriterion):
    """
    Mean absolute error impurity criterion.

    MAE = (1 / n) * (sum_i |y_i - f_i|), where y_i is the true
    value and f_i is the predicted value.
    """

    def __init__(self, n_outputs, n_samples):
        super().__init__(n_outputs, n_samples)
        self.left_child = ivy.empty(n_outputs, dtype=object)
        self.right_child = ivy.empty(n_outputs, dtype=object)
        for k in range(n_outputs):
            self.left_child[k] = WeightedMedianCalculator(n_samples)
            self.right_child[k] = WeightedMedianCalculator(n_samples)

    def init(self, y, sample_weight, weighted_n_samples, sample_indices, start, end):
        super().init(y, sample_weight, weighted_n_samples, sample_indices, start, end)

        left_child = self.left_child
        right_child = self.right_child

        for k in range(self.n_outputs):
            left_child[k].reset()
            right_child[k].reset()

        for p in range(start, end):
            i = sample_indices[p]
            w = sample_weight[i] if sample_weight is not None else 1.0
            for k in range(self.n_outputs):
                right_child[k].push(self.y[i, k], w)

        for k in range(self.n_outputs):
            self.node_medians[k] = right_child[k].get_median()

    def init_missing(self, n_missing):
        if n_missing != 0:
            raise ValueError("Missing values are not supported for MAE.")

    def reset(self):
        super().reset()
        left_child = self.left_child
        right_child = self.right_child

        self.weighted_n_left = 0.0
        self.weighted_n_right = self.weighted_n_node_samples

        for k in range(self.n_outputs):
            for i in range(left_child[k].size()):
                value, weight = left_child[k].pop()
                right_child[k].push(value, weight)

    def reverse_reset(self):
        super().reverse_reset()
        left_child = self.left_child
        right_child = self.right_child

        self.weighted_n_right = 0.0
        self.weighted_n_left = self.weighted_n_node_samples

        for k in range(self.n_outputs):
            for i in range(right_child[k].size()):
                value, weight = right_child[k].pop()
                left_child[k].push(value, weight)

    def update(self, new_pos):
        super().update(new_pos)
        sample_weight = self.sample_weight
        sample_indices = self.sample_indices

        left_child = self.left_child
        right_child = self.right_child

        pos = self.pos
        end = self.end

        for k in range(self.n_outputs):
            for p in range(pos, end):
                i = sample_indices[p]
                w = sample_weight[i] if sample_weight is not None else 1.0
                left_child[k].remove(self.y[i, k], w)
                right_child[k].push(self.y[i, k], w)

        self.weighted_n_right = self.weighted_n_node_samples - self.weighted_n_left

    def node_value(self, dest):
        for k in range(self.n_outputs):
            dest[k] = self.node_medians[k]

    def node_impurity(self):
        sample_weight = self.sample_weight
        sample_indices = self.sample_indices
        impurity = 0.0

        for k in range(self.n_outputs):
            for p in range(self.start, self.end):
                i = sample_indices[p]

                if sample_weight is not None:
                    w = sample_weight[i]
                else:
                    w = 1.0

                impurity += abs(self.y[i, k] - self.node_medians[k]) * w

        return impurity / (self.weighted_n_node_samples * self.n_outputs)

    def children_impurity(self):
        sample_weight = self.sample_weight
        sample_indices = self.sample_indices

        start = self.start
        pos = self.pos
        end = self.end

        impurity_left = 0.0
        impurity_right = 0.0

        for k in range(self.n_outputs):
            for p in range(start, pos):
                i = sample_indices[p]

                if sample_weight is not None:
                    w = sample_weight[i]
                else:
                    w = 1.0

                impurity_left += abs(self.y[i, k] - self.node_medians[k]) * w

            impurity_left /= self.weighted_n_left * self.n_outputs

            for p in range(pos, end):
                i = sample_indices[p]

                if sample_weight is not None:
                    w = sample_weight[i]
                else:
                    w = 1.0

                impurity_right += abs(self.y[i, k] - self.node_medians[k]) * w

            impurity_right /= self.weighted_n_right * self.n_outputs

        return impurity_left, impurity_right


# --- Helpers --- #
# --------------- #


def _move_sums_classification(
    criterion, sum_1, sum_2, weighted_n_1, weighted_n_2, put_missing_in_1
):
    """
    Distribute sum_total and sum_missing into sum_1 and sum_2.

    If there are missing values and:
    - put_missing_in_1 is True, then missing values go to sum_1. Specifically:
        sum_1 = sum_missing
        sum_2 = sum_total - sum_missing

    - put_missing_in_1 is False, then missing values go to sum_2. Specifically:
        sum_1 = 0
        sum_2 = sum_total
    """
    for k in range(criterion.n_outputs):
        if criterion.n_missing != 0 and put_missing_in_1:
            sum_1[k, :] = criterion.sum_missing[k, :]
            sum_2[k, :] = criterion.sum_total[k, :] - criterion.sum_missing[k, :]
            weighted_n_1[0] = criterion.weighted_n_missing
            weighted_n_2[0] = (
                criterion.weighted_n_node_samples - criterion.weighted_n_missing
            )
        else:
            sum_1[k, :] = 0.0  # Set all elements in sum_1 to 0
            sum_2[k, :] = criterion.sum_total[k, :]
            weighted_n_1[0] = 0.0
            weighted_n_2[0] = criterion.weighted_n_node_samples


def _move_sums_regression(
    criterion, sum_1, sum_2, weighted_n_1, weighted_n_2, put_missing_in_1
):
    """
    Distribute sum_total and sum_missing into sum_1 and sum_2.

    If there are missing values and:
    - put_missing_in_1 is True, then missing values go to sum_1. Specifically:
        sum_1 = sum_missing
        sum_2 = sum_total - sum_missing

    - put_missing_in_1 is False, then missing values go to sum_2. Specifically:
        sum_1 = 0
        sum_2 = sum_total
    """
    if criterion.n_missing != 0 and put_missing_in_1:
        sum_1[:] = criterion.sum_missing[:]
        sum_2[:] = criterion.sum_total[:] - criterion.sum_missing[:]
        weighted_n_1[0] = criterion.weighted_n_missing
        weighted_n_2[0] = (
            criterion.weighted_n_node_samples - criterion.weighted_n_missing
        )
    else:
        sum_1[:] = 0.0  # Set all elements in sum_1 to 0
        sum_2[:] = criterion.sum_total[:]
        weighted_n_1[0] = 0.0
        weighted_n_2[0] = criterion.weighted_n_node_samples
