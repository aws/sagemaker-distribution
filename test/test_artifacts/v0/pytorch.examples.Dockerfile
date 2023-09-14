ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN sudo apt-get update && \
    sudo apt-get install -y git && \
    git clone --recursive https://github.com/pytorch/examples && \
    :

WORKDIR "examples"

# There is a line in run_python_examples.sh which looks like: BASE_DIR=`pwd`"/"`dirname $0`
# When we run the shell script through /usr/local/bin/_entrypoint.sh, that line above doesn't work correctly. In our
# case, we properly set `pwd` to the directory that contains all the examples, so we just modify the script to change
# the previous line to look like: BASE_DIR=`pwd`
RUN sed -i 's/^BASE_DIR=.*pwd.*dirname.*/BASE_DIR=`pwd`/' run_python_examples.sh
RUN ./run_python_examples.sh install_deps

# We skip `imagenet` because it requires a lot of resources and so aren't a good fit for us.
CMD ["./run_python_examples.sh", "dcgan,fast_neural_style,distributed,mnist,mnist_forward_forward,mnist_hogwild,mnist_rnn,regression,reinforcement_learning,siamese_network,super_resolution,time_sequence_prediction,vae,word_language_model,fx"]
