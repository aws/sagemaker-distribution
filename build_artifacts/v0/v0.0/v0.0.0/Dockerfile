ARG TAG_FOR_BASE_MICROMAMBA_IMAGE
FROM mambaorg/micromamba:$TAG_FOR_BASE_MICROMAMBA_IMAGE

ARG CUDA_MAJOR_MINOR_VERSION=''
ARG ENV_IN_FILENAME
ARG ARG_BASED_ENV_IN_FILENAME

ARG NB_USER="sagemaker-user"
ARG NB_UID=1000
ARG NB_GID=100

USER root
RUN usermod "--login=${NB_USER}" "--home=/home/${NB_USER}" --move-home "-u ${NB_UID}" "${MAMBA_USER}" && \
    groupmod "--new-name=${NB_USER}" --non-unique "-g ${NB_GID}" "${MAMBA_USER}" && \
    # Update the expected value of MAMBA_USER for the
    # _entrypoint.sh consistency check.
    echo "${NB_USER}" > "/etc/arg_mamba_user" && \
    :
ENV MAMBA_USER=$NB_USER

RUN apt-get update && \
    apt-get install -y --no-install-recommends sudo gettext-base && \
    # We just install tzdata below but leave default time zone as UTC. This helps packages like Pandas to function correctly.
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata && \
    chmod g+w /etc/passwd && \
    echo "${NB_USER}    ALL=(ALL)    NOPASSWD:    ALL" >> /etc/sudoers && \
    # Note that we do NOT run `rm -rf /var/lib/apt/lists/*` here. If we did, anyone building on top of our images will
    # not be able to run any `apt-get install` commands and that would hamper customizability of the images.
    :
RUN echo "source /usr/local/bin/_activate_current_env.sh" | tee --append /etc/profile

USER $MAMBA_USER
COPY --chown=$MAMBA_USER:$MAMBA_USER *.in /tmp/

# Make sure that $ENV_IN_FILENAME has a newline at the end before the `tee` command runs. Otherwise, nasty things
# will happen.
RUN if [[ -z $ARG_BASED_ENV_IN_FILENAME ]] ; \
    then echo 'No ARG_BASED_ENV_IN_FILENAME passed' ; \
    else envsubst < /tmp/$ARG_BASED_ENV_IN_FILENAME | tee --append /tmp/$ENV_IN_FILENAME ; \
    fi

ARG CONDA_OVERRIDE_CUDA=$CUDA_MAJOR_MINOR_VERSION
RUN micromamba install -y --name base --file /tmp/$ENV_IN_FILENAME && \
    micromamba clean --all --yes --force-pkgs-dirs && \
    rm -rf /tmp/*.in

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN sudo ln -s $(which python3) /usr/bin/python

WORKDIR "/home/${NB_USER}"
ENV SHELL=/bin/bash
