ARG TAG_FOR_BASE_MICROMAMBA_IMAGE
FROM mambaorg/micromamba:$TAG_FOR_BASE_MICROMAMBA_IMAGE

ARG CUDA_MAJOR_MINOR_VERSION=''
ARG ENV_IN_FILENAME
ARG ARG_BASED_ENV_IN_FILENAME

ARG AMZN_BASE="/opt/amazon/sagemaker"
ARG DIRECTORY_TREE_STAGE_DIR="${AMZN_BASE}/dir-staging"

ARG NB_USER="sagemaker-user"
ARG NB_UID=1000
ARG NB_GID=100

ENV SAGEMAKER_LOGGING_DIR="/var/log/sagemaker/"
ENV STUDIO_LOGGING_DIR="/var/log/studio/"

USER root
RUN usermod "--login=${NB_USER}" "--home=/home/${NB_USER}" --move-home "-u ${NB_UID}" "${MAMBA_USER}" && \
    groupmod "--new-name=${NB_USER}" --non-unique "-g ${NB_GID}" "${MAMBA_USER}" && \
    # Update the expected value of MAMBA_USER for the
    # _entrypoint.sh consistency check.
    echo "${NB_USER}" > "/etc/arg_mamba_user" && \
    :
ENV MAMBA_USER=$NB_USER
ENV USER=$NB_USER

RUN apt-get update && \
    apt-get install -y --no-install-recommends sudo gettext-base wget curl unzip git rsync build-essential openssh-client nano && \
    # We just install tzdata below but leave default time zone as UTC. This helps packages like Pandas to function correctly.
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata krb5-user libkrb5-dev libsasl2-dev libsasl2-modules && \
    chmod g+w /etc/passwd && \
    echo "ALL    ALL=(ALL)    NOPASSWD:    ALL" >> /etc/sudoers && \
    touch /etc/krb5.conf.lock && chown ${NB_USER}:${MAMBA_USER} /etc/krb5.conf* && \
    # Note that we do NOT run `rm -rf /var/lib/apt/lists/*` here. If we did, anyone building on top of our images will
    # not be able to run any `apt-get install` commands and that would hamper customizability of the images.
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    sudo ./aws/install && \
    rm -rf aws awscliv2.zip && \
    :
RUN echo "source /usr/local/bin/_activate_current_env.sh" | tee --append /etc/profile

USER $MAMBA_USER
COPY --chown=$MAMBA_USER:$MAMBA_USER $ENV_IN_FILENAME *.in /tmp/

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

# Install glue kernels, and move to shared directory
# Also patching base kernel so Studio background code doesn't start session silently
RUN install-glue-kernels && \
    SITE_PACKAGES=$(pip show aws-glue-sessions | grep Location | awk '{print $2}') && \
    jupyter-kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_pyspark --user && \
    jupyter-kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_spark --user && \
    mv /home/sagemaker-user/.local/share/jupyter/kernels/glue_pyspark /opt/conda/share/jupyter/kernels && \
    mv /home/sagemaker-user/.local/share/jupyter/kernels/glue_spark /opt/conda/share/jupyter/kernels && \
    sed -i '/if not store_history and (/i\        if "sm_analytics_runtime_check" in code:\n            return await self._complete_cell()\n' \
    "$SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_kernel_base/BaseKernel.py"


# Patch glue kernels to use kernel wrapper
COPY patch_glue_pyspark.json /opt/conda/share/jupyter/kernels/glue_pyspark/kernel.json
COPY patch_glue_spark.json /opt/conda/share/jupyter/kernels/glue_spark/kernel.json

USER root
RUN HOME_DIR="/home/${NB_USER}/licenses" \
    && mkdir -p ${HOME_DIR} \
    && curl -o ${HOME_DIR}/oss_compliance.zip https://aws-dlinfra-utilities.s3.amazonaws.com/oss_compliance.zip \
    && unzip ${HOME_DIR}/oss_compliance.zip -d ${HOME_DIR}/ \
    && cp ${HOME_DIR}/oss_compliance/test/testOSSCompliance /usr/local/bin/testOSSCompliance \
    && chmod +x /usr/local/bin/testOSSCompliance \
    && chmod +x ${HOME_DIR}/oss_compliance/generate_oss_compliance.sh \
    && ${HOME_DIR}/oss_compliance/generate_oss_compliance.sh ${HOME_DIR} python \
    && rm -rf ${HOME_DIR}/oss_compliance*

# Merge in OS directory tree contents.
RUN mkdir -p ${DIRECTORY_TREE_STAGE_DIR}
COPY dirs/ ${DIRECTORY_TREE_STAGE_DIR}/
RUN rsync -a ${DIRECTORY_TREE_STAGE_DIR}/ / && \
    rm -rf ${DIRECTORY_TREE_STAGE_DIR}

# Create logging directories for supervisor
RUN mkdir -p $SAGEMAKER_LOGGING_DIR && \
    chmod a+rw $SAGEMAKER_LOGGING_DIR && \
    mkdir -p ${STUDIO_LOGGING_DIR} && \
    chown ${NB_USER}:${MAMBA_USER} ${STUDIO_LOGGING_DIR}

# Create supervisord runtime directory
RUN mkdir -p /var/run/supervisord && \
    chmod a+rw /var/run/supervisord

USER $MAMBA_USER
ENV PATH="/opt/conda/bin:/opt/conda/condabin:$PATH"
WORKDIR "/home/${NB_USER}"

# Install Kerberos.
# Make sure no dependency is added/updated
RUN pip install "krb5>=0.5.1,<0.6" && \
    pip show krb5 | grep Require | xargs -i sh -c '[ $(echo {} | cut -d: -f2 | wc -w) -eq 0 ] '

# https://stackoverflow.com/questions/122327
RUN SYSTEM_PYTHON_PATH=$(python3 -c "from __future__ import print_function;import sysconfig; print(sysconfig.get_paths().get('purelib'))") && \
    # Remove SparkRKernel as it's not supported \
    jupyter-kernelspec remove -f -y sparkrkernel && \
    # Patch Sparkmagic lib to support Custom Certificates \
    # https://github.com/jupyter-incubator/sparkmagic/pull/435/files \
    cp -a ${SYSTEM_PYTHON_PATH}/sagemaker_studio_analytics_extension/patches/configuration.py ${SYSTEM_PYTHON_PATH}/sparkmagic/utils/ && \
    cp -a ${SYSTEM_PYTHON_PATH}/sagemaker_studio_analytics_extension/patches/reliablehttpclient.py ${SYSTEM_PYTHON_PATH}/sparkmagic/livyclientlib/reliablehttpclient.py && \
    sed -i 's=  "python"=  "/opt/conda/bin/python"=g'  /opt/conda/share/jupyter/kernels/pysparkkernel/kernel.json /opt/conda/share/jupyter/kernels/sparkkernel/kernel.json && \
    sed -i 's="Spark"="SparkMagic Spark"=g'  /opt/conda/share/jupyter/kernels/sparkkernel/kernel.json && \
    sed -i 's="PySpark"="SparkMagic PySpark"=g'  /opt/conda/share/jupyter/kernels/pysparkkernel/kernel.json

ENV SHELL=/bin/bash
