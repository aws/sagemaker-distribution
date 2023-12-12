ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Inorder to test scipy, we need pytest and hypothesis to be installed.
RUN micromamba install -y --freeze-installed -c conda-forge pytest hypothesis scipy-tests
# Check https://github.com/numpy/numpy/blob/main/doc/TESTS.rst
# Note: Testing guidelines are same for numpy and scipy.
# scipy.test() returns True if tests succeed else False.
# We need to flip the result so that we exit with status code as 0 if all the tests succeeded.
CMD ["python", "-c", "import scipy,sys; tests_succeeded = scipy.test(); sys.exit(not tests_succeeded)"]
