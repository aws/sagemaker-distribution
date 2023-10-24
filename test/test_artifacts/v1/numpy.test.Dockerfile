ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Inorder to test numpy, we need pytest and hypothesis to be installed.
RUN micromamba install -y --freeze-installed conda-forge::pytest conda-forge::hypothesis conda-forge::meson
# Some unit tests in numpy requires gcc to be installed.
RUN sudo apt-get update && sudo apt-get install -y gcc
# Check https://numpy.org/doc/stable/reference/testing.html
# numpy.test() returns True if tests succeed else False.
# We need to flip the result so that we exit with status code as 0 if all the tests succeeded.
CMD ["python", "-c", "import numpy,sys; tests_succeeded = numpy.test(); sys.exit(not tests_succeeded)"]
