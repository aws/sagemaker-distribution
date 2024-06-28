# Verify Tensorflow CUDA
import tensorflow as tf

cuda_available = tf.test.is_built_with_cuda()
if not cuda_available:
    raise Exception("TensorFlow is installed without CUDA support for GPU image build.")
print("TensorFlow is built with CUDA support.")


# Verify Pytorch CUDA
import subprocess

# Run the micromamba list command and capture the output
result = subprocess.run(['micromamba', 'list'], stdout=subprocess.PIPE, text=True)

# Split the output into lines
package_lines = result.stdout.strip().split('\n')

# Find the PyTorch entry
pytorch_entry = None
for line in package_lines:
    dependency_info = line.strip().split()
    if dependency_info and dependency_info[0] == 'pytorch':
        pytorch_entry = line.split()
        break

# If PyTorch is installed, print its information
if pytorch_entry:
    package_name = pytorch_entry[0]
    package_version = pytorch_entry[1]
    package_build = pytorch_entry[2]
    print(f"PyTorch: {package_name} {package_version} {package_build}")
# Raise exception if CUDA is not detected
if 'cuda' not in package_build: 
    raise Exception("Pytorch is installed without CUDA support for GPU image build.")
