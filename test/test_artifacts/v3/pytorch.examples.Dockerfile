ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN git clone --recursive https://github.com/pytorch/examples

# During automation some tests fails with `libcuda.so: cannot open shared object file: No such file or directory`
# But libcuda.so.1 exists. Adding this resolves, but also adding `2>/dev/null` to ignore if not needed.
RUN sudo ln -s /usr/lib/x86_64-linux-gnu/libcuda.so.1 /usr/lib/x86_64-linux-gnu/libcuda.so 2>/dev/null

WORKDIR "examples"

RUN ./run_python_examples.sh install_deps

# We skip `imagenet` because it requires a lot of resources and so aren't a good fit for us.
CMD ["./run_python_examples.sh", "dcgan,fast_neural_style,distributed,mnist,mnist_forward_forward,mnist_hogwild,mnist_rnn,regression,reinforcement_learning,siamese_network,super_resolution,time_sequence_prediction,vae,word_language_model,fx"]
