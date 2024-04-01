ARG COSMOS_IMAGE
FROM $COSMOS_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN micromamba install -y --freeze-installed -c conda-forge pytest

RUN sudo apt-get update && \
    sudo apt-get install -y git && \
    git clone --recursive  https://github.com/aws/git-remote-codecommit.git && \
    :
WORKDIR "git-remote-codecommit"
COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_git_remote_codecommit_test.sh .
RUN chmod +x run_git_remote_codecommit_test.sh
CMD ["./run_git_remote_codecommit_test.sh"]
