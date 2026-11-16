ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN git clone --recursive https://github.com/pytorch/examples

# During automation some tests fails with `libcuda.so: cannot open shared object file: No such file or directory`
# But libcuda.so.1 exists. Adding this resolves, but also adding `2>/dev/null` to ignore if not needed.
RUN sudo ln -s /usr/lib/x86_64-linux-gnu/libcuda.so.1 /usr/lib/x86_64-linux-gnu/libcuda.so 2>/dev/null

RUN micromamba install --freeze-installed -y conda-forge::uv
# uv ignores the conda "base" environment, so point `uv pip`/`uv run` at the image's python explicitly.
ENV UV_SYSTEM_PYTHON=1
# Same list as run_all() minus mnist_hogwild (pins torchvision==0.20.0) and time_sequence_prediction (pins torch<2.6):
# with UV_SYSTEM_PYTHON their requirements would replace the image's own torch.
ENV EXAMPLES=dcgan,fast_neural_style,imagenet,mnist,mnist_forward_forward,mnist_rnn,regression,reinforcement_learning,siamese_network,vae,word_language_model,fx,gcn,gat

WORKDIR "examples"

CMD ./run_python_examples.sh
