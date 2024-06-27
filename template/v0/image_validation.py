import tensorflow as tf

cuda_available = tf.test.is_built_with_cuda()
if not cuda_available:
    raise Exception("TensorFlow is installed without CUDA support for GPU image build.")
print("TensorFlow is built with CUDA support.")
