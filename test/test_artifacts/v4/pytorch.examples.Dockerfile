ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN git clone --recursive https://github.com/pytorch/examples

# During automation some tests fails with `libcuda.so: cannot open shared object file: No such file or directory`
# But libcuda.so.1 exists. Adding this resolves, but also adding `2>/dev/null` to ignore if not needed.
RUN sudo ln -s /usr/lib/x86_64-linux-gnu/libcuda.so.1 /usr/lib/x86_64-linux-gnu/libcuda.so 2>/dev/null

RUN micromamba install --freeze-installed -y conda-forge::uv

WORKDIR "examples"

CMD ./run_python_examples.sh
