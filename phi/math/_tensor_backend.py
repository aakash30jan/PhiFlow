from functools import partial

from ._shape import BATCH_DIM, CHANNEL_DIM, SPATIAL_DIM
from ..backend.backend import Backend
from ..backend.dynamic_backend import DYNAMIC_BACKEND as math
from ._tensors import AbstractTensor, tensor, broadcastable_native_tensors, NativeTensor, CollapsedTensor, TensorStack


class TensorBackend(Backend):

    def __init__(self):
        Backend.__init__(self, 'Tensor', precision=None)
    
    def is_tensor(self, x, only_native=False):
        if only_native:
            return isinstance(x, AbstractTensor)
        else:
            return True

    def as_tensor(self, x, convert_external=True):
        if convert_external:
            return tensor(x)
        else:
            return x

    def copy(self, tensor, only_mutable=False):
        raise NotImplementedError()

    def transpose(self, tensor, axes):
        return CollapsedTensor(tensor, tensor.shape[axes])

    def equal(self, x, y):
        return x == y

    def random_uniform(self, shape):
        raise NotImplementedError()

    def random_normal(self, shape):
        raise NotImplementedError()

    def stack(self, values, axis=0):
        if axis == 0:
            dim_type = BATCH_DIM
        elif axis == -1 or axis == len(values):
            dim_type = CHANNEL_DIM
        else:
            raise NotImplementedError()
        return TensorStack(values, 'stack', dim_type)

    def concat(self, values, axis):
        tensors = broadcastable_native_tensors(values)
        concatenated = math.concat(tensors, axis)
        return NativeTensor(concatenated, values[0].shape)

    def pad(self, value, pad_width, mode='constant', constant_values=0):
        assert isinstance(value, AbstractTensor)
        if isinstance(pad_width, dict):  # name -> (lower, upper) or both
            if isinstance(value, NativeTensor):
                native = value.tensor
                ordered_pad_widths = value.shape.order(pad_width, default=0)
                ordered_mode = value.shape.order(mode, default='constant')
                ordered_constant_values = value.shape.order(constant_values, default=0)
                result_tensor = math.pad(native, ordered_pad_widths, ordered_mode, ordered_constant_values)
                new_shape = value.shape.with_sizes(math.staticshape(result_tensor))
                return NativeTensor(result_tensor, new_shape)
        raise NotImplementedError()

    def resample(self, inputs, sample_coords, interpolation='linear', boundary='constant', constant_values=0):
        raise NotImplementedError()

    def reshape(self, value, shape):
        raise NotImplementedError()

    def sum(self, value, axis=None, keepdims=False):
        if isinstance(value, AbstractTensor):
            raise NotImplementedError()
        else:
            assert axis == 0
            shape, tensors = broadcastable_native_tensors(*value)
            result_tensor = math.sum(tensors, axis=0, keepdims=False)
            return NativeTensor(result_tensor, shape)

    def prod(self, value, axis=None):
        raise NotImplementedError()

    def divide_no_nan(self, x, y):
        raise NotImplementedError()

    def where(self, condition, x=None, y=None):
        raise NotImplementedError()

    def mean(self, value, axis=None, keepdims=False):
        raise NotImplementedError()

    def py_func(self, func, inputs, Tout, shape_out, stateful=True, name=None, grad=None):
        raise NotImplementedError()

    def range(self, start, limit=None, delta=1, dtype=None):
        raise NotImplementedError()

    def zeros_like(self, tensor):
        raise NotImplementedError()

    def ones_like(self, tensor):
        raise NotImplementedError()

    def dot(self, a, b, axes):
        raise NotImplementedError()

    def matmul(self, A, b):
        raise NotImplementedError()

    def einsum(self, equation, *tensors):
        raise NotImplementedError()

    def while_loop(self, cond, body, loop_vars, shape_invariants=None, parallel_iterations=10, back_prop=True, swap_memory=False, name=None, maximum_iterations=None):
        raise NotImplementedError()

    def abs(self, x):
        raise NotImplementedError()

    def sign(self, x):
        raise NotImplementedError()

    def round(self, x):
        raise NotImplementedError()

    def ceil(self, x):
        raise NotImplementedError()

    def floor(self, x):
        raise NotImplementedError()

    def max(self, x, axis=None, keepdims=False):
        raise NotImplementedError()

    def min(self, x, axis=None, keepdims=False):
        raise NotImplementedError()

    def maximum(self, a, b):
        a_, b_ = tensor(a, b)
        return a_._op2(b_, math.maximum)

    def minimum(self, a, b):
        a_, b_ = tensor(a, b)
        return a_._op2(b_, math.minimum)

    def clip(self, x, minimum, maximum):
        new_shape, (x_, min_, max_) = broadcastable_native_tensors(tensor(x, minimum, maximum))
        assert new_shape == x.shape, 'Not implemented'
        result_tensor = math.clip(x_, min_, max_)
        return NativeTensor(result_tensor, new_shape)

    def with_custom_gradient(self, function, inputs, gradient, input_index=0, output_index=None, name_base='custom_gradient_func'):
        raise NotImplementedError()

    def sqrt(self, x):
        return tensor(x)._op1(math.sqrt)

    def exp(self, x):
        return tensor(x)._op1(math.exp)

    def conv(self, tensor, kernel, padding='same'):
        raise NotImplementedError()

    def expand_dims(self, a, axis=0, number=1):
        raise NotImplementedError()

    def shape(self, tensor):
        return tensor.shape.sizes

    def staticshape(self, tensor):
        return tensor.shape.sizes

    def to_float(self, x, float64=False):
        return tensor(x)._op1(partial(math.to_float, float64=float64))

    def to_int(self, x, int64=False):
        return tensor(x)._op1(partial(math.to_int, int64=int64))

    def to_complex(self, x):
        return tensor(x)._op1(math.to_complex)

    def gather(self, values, indices):
        raise NotImplementedError()

    def gather_nd(self, values, indices, batch_dims=0):
        raise NotImplementedError()

    def unstack(self, tensor, axis=0, keepdims=False):
        assert isinstance(tensor, AbstractTensor)
        return tensor.unstack(tensor.shape.names[axis])

    def std(self, x, axis=None, keepdims=False):
        raise NotImplementedError()

    def boolean_mask(self, x, mask):
        raise NotImplementedError()

    def isfinite(self, x):
        raise NotImplementedError()

    def scatter(self, points, indices, values, shape, duplicates_handling='undefined'):
        raise NotImplementedError()

    def any(self, boolean_tensor, axis=None, keepdims=False):
        raise NotImplementedError()

    def all(self, boolean_tensor, axis=None, keepdims=False):
        raise NotImplementedError()

    def fft(self, x):
        raise NotImplementedError()

    def ifft(self, k):
        raise NotImplementedError()

    def imag(self, complex):
        raise NotImplementedError()

    def real(self, complex):
        raise NotImplementedError()

    def cast(self, x, dtype):
        raise NotImplementedError()

    def sin(self, x):
        raise NotImplementedError()

    def cos(self, x):
        raise NotImplementedError()

    def dtype(self, array):
        raise NotImplementedError()

    def tile(self, value, multiples):
        raise NotImplementedError()

    def sparse_tensor(self, indices, values, shape):
        raise NotImplementedError()