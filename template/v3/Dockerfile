ARG TAG_FOR_BASE_MICROMAMBA_IMAGE
FROM mambaorg/micromamba:$TAG_FOR_BASE_MICROMAMBA_IMAGE

ARG CUDA_MAJOR_MINOR_VERSION=''
ARG ENV_IN_FILENAME
ARG PINNED_ENV_IN_FILENAME
ARG ARG_BASED_ENV_IN_FILENAME
ARG IMAGE_VERSION
LABEL "org.amazon.sagemaker-distribution.image.version"=$IMAGE_VERSION

ARG AMZN_BASE="/opt/amazon/sagemaker"
ARG DB_ROOT_DIR="/opt/db"
ARG DIRECTORY_TREE_STAGE_DIR="${AMZN_BASE}/dir-staging"

ARG NB_USER="sagemaker-user"
ARG NB_UID=1000
ARG NB_GID=100

# https://www.openssl.org/source/
ARG FIPS_VALIDATED_SSL=3.0.8
ARG MIN_REQUIRED_MICROMAMBA_VERSION=1.5.11

ENV SAGEMAKER_LOGGING_DIR="/var/log/sagemaker/"
ENV STUDIO_LOGGING_DIR="/var/log/studio/"
ENV EDITOR="nano"
ENV IMAGE_VERSION=$IMAGE_VERSION
ENV PINNED_MICROMAMBA_MINOR_VERSION="1.5.*"
ENV SAGEMAKER_RECOVERY_MODE_HOME=/tmp/sagemaker-recovery-mode-home

USER root
# Upgrade micromamba to the latest patch version in the pinned minor version range, if applicable
RUN CURRENT_MICROMAMBA_VERSION=$(micromamba --version) && \
    echo "Current micromamba version: $CURRENT_MICROMAMBA_VERSION" && \
    if [[ "$CURRENT_MICROMAMBA_VERSION" == $PINNED_MICROMAMBA_MINOR_VERSION ]]; then \
        echo "Upgrading micromamba to the latest $PINNED_MICROMAMBA_MINOR_VERSION version..." && \
        micromamba self-update -c conda-forge --version "$MIN_REQUIRED_MICROMAMBA_VERSION" && \
        micromamba clean --all --yes --force-pkgs-dirs; \
    else \
        echo "Micromamba is already at version $CURRENT_MICROMAMBA_VERSION (outside $PINNED_MICROMAMBA_MINOR_VERSION). No upgrade performed."; \
    fi

RUN usermod "--login=${NB_USER}" "--home=/home/${NB_USER}" --move-home "-u ${NB_UID}" "${MAMBA_USER}" && \
    groupmod "--new-name=${NB_USER}" --non-unique "-g ${NB_GID}" "${MAMBA_USER}" && \
    # Update the expected value of MAMBA_USER for the
    # _entrypoint.sh consistency check.
    echo "${NB_USER}" > "/etc/arg_mamba_user" && \
    :
ENV MAMBA_USER=$NB_USER
ENV USER=$NB_USER

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends sudo gettext-base wget curl unzip git rsync build-essential openssh-client nano cron less mandoc jq ca-certificates gnupg && \
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
    : && \
    # Install Q CLI
    curl --proto '=https' --tlsv1.2 -sSf "https://desktop-release.q.us-east-1.amazonaws.com/1.12.7/q-x86_64-linux.zip" -o "q.zip" && \
    unzip q.zip && \
    Q_INSTALL_GLOBAL=true ./q/install.sh --no-confirm && \
    rm -rf q q.zip && \
    : && \
    echo "source /usr/local/bin/_activate_current_env.sh" | tee --append /etc/profile && \
# CodeEditor - create server, user data dirs
    mkdir -p /opt/amazon/sagemaker/sagemaker-code-editor-server-data /opt/amazon/sagemaker/sagemaker-code-editor-user-data \
    && chown $MAMBA_USER:$MAMBA_USER /opt/amazon/sagemaker/sagemaker-code-editor-server-data /opt/amazon/sagemaker/sagemaker-code-editor-user-data && \
# create dir to store user data files
    mkdir -p /opt/amazon/sagemaker/user-data \
    && chown $MAMBA_USER:$MAMBA_USER /opt/amazon/sagemaker/user-data && \
# Merge in OS directory tree contents.
    mkdir -p ${DIRECTORY_TREE_STAGE_DIR}
COPY dirs/ ${DIRECTORY_TREE_STAGE_DIR}/
RUN rsync -a ${DIRECTORY_TREE_STAGE_DIR}/ / && \
    rm -rf ${DIRECTORY_TREE_STAGE_DIR} && \
# CodeEditor - download the extensions
    mkdir -p /etc/code-editor/extensions && \
    while IFS= read -r url || [ -n "$url" ]; do \
        echo "Downloading extension from ${url}..." && \
        wget --no-check-certificate -P /etc/code-editor/extensions "${url}"; \
    done < /etc/code-editor/extensions.txt

USER $MAMBA_USER
COPY --chown=$MAMBA_USER:$MAMBA_USER $ENV_IN_FILENAME *.in /tmp/
COPY --chown=$MAMBA_USER:$MAMBA_USER $PINNED_ENV_IN_FILENAME *.in /tmp/

ARG MAMBA_DOCKERFILE_ACTIVATE=1
ARG CONDA_OVERRIDE_CUDA=$CUDA_MAJOR_MINOR_VERSION

# Make sure that $ENV_IN_FILENAME and $PINNED_ENV_IN_FILENAME has a newline at the end before the `tee` command runs.
# Otherwise, nasty things will happen.
RUN if [[ -z $ARG_BASED_ENV_IN_FILENAME ]] ; \
    then echo 'No ARG_BASED_ENV_IN_FILENAME passed' ; \
    else envsubst < /tmp/$ARG_BASED_ENV_IN_FILENAME | tee --append /tmp/$ENV_IN_FILENAME ; \
    fi && \
    # Enforce dependencies are all installed from conda-forge
    micromamba install -y --name base --file /tmp/$ENV_IN_FILENAME --file /tmp/$PINNED_ENV_IN_FILENAME && \
    mkdir -p $SAGEMAKER_RECOVERY_MODE_HOME && \
    chown $MAMBA_USER:$MAMBA_USER $SAGEMAKER_RECOVERY_MODE_HOME && \
    SUPERVISOR_VERSION=$(grep "^conda-forge::supervisor\[" /tmp/$ENV_IN_FILENAME) && \
    JUPYTERLAB_VERSION=$(grep "^conda-forge::jupyterlab\[" /tmp/$ENV_IN_FILENAME) && \
    SAGEMAKER_JUPYTERLAB_VERSION=$(grep "^conda-forge::sagemaker-jupyterlab-extension" /tmp/$ENV_IN_FILENAME) && \
    echo "Installing in sagemaker-recovery-mode micromamba environment: $JUPYTERLAB_VERSION $SAGEMAKER_JUPYTERLAB_VERSION" && \
    micromamba create --prefix /opt/conda/envs/sagemaker-recovery-mode && \
    micromamba install --prefix /opt/conda/envs/sagemaker-recovery-mode -y $JUPYTERLAB_VERSION $SAGEMAKER_JUPYTERLAB_VERSION $SUPERVISOR_VERSION && \
    micromamba clean --all --yes --force-pkgs-dirs && \
    rm -rf /tmp/*.in && \
    sudo ln -s $(which python3) /usr/bin/python && \
    # Update npm version
    npm i -g npm && \
    # Enforce to use `conda-forge` as only channel, by removing `defaults`
    conda config --remove channels defaults && \
    micromamba config append channels conda-forge --env && \
    # Configure CodeEditor - Install extensions and set preferences
    extensionloc=/opt/amazon/sagemaker/sagemaker-code-editor-server-data/extensions && mkdir -p "${extensionloc}" \
    # Loop through all vsix files in /etc/code-editor/extensions and install them
    && for ext in /etc/code-editor/extensions/*.vsix; do \
        echo "Installing extension ${ext}..."; \
        sagemaker-code-editor --install-extension "${ext}" --extensions-dir "${extensionloc}" --server-data-dir /opt/amazon/sagemaker/sagemaker-code-editor-server-data --user-data-dir /opt/amazon/sagemaker/sagemaker-code-editor-user-data; \
       done \
    # Copy the settings
    && cp /etc/code-editor/code_editor_machine_settings.json /opt/amazon/sagemaker/sagemaker-code-editor-server-data/data/Machine/settings.json && \
    cp /etc/code-editor/code_editor_user_settings.json /opt/amazon/sagemaker/sagemaker-code-editor-server-data/data/User/settings.json && \
    # Install glue kernels, and move to shared directory
    # Also patching base kernel so Studio background code doesn't start session silently
    install-glue-kernels && \
    SITE_PACKAGES=$(pip show aws-glue-sessions | grep Location | awk '{print $2}') && \
    jupyter-kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_pyspark --user && \
    jupyter-kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_spark --user && \
    mv /home/sagemaker-user/.local/share/jupyter/kernels/glue_pyspark /opt/conda/share/jupyter/kernels && \
    mv /home/sagemaker-user/.local/share/jupyter/kernels/glue_spark /opt/conda/share/jupyter/kernels && \
    sed -i '/if not store_history and (/i\        if "sm_analytics_runtime_check" in code:\n            return await self._complete_cell()\n' \
    "$SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_kernel_base/BaseKernel.py" && \
    # Install FIPS Provider for OpenSSL, on top of existing OpenSSL installation
    # v3.0.8 is latest FIPS validated provider, so this is the one we install
    # But we need to run tests against the installed version.
    # see https://github.com/openssl/openssl/blob/master/README-FIPS.md https://www.openssl.org/source/
    INSTALLED_SSL=$(micromamba list | grep openssl | tr -s ' ' | cut -d ' ' -f 3 | head -n 1) && \
    # download source code for installed, and FIPS validated openssl versions
    curl -L https://github.com/openssl/openssl/releases/download/openssl-$FIPS_VALIDATED_SSL/openssl-$FIPS_VALIDATED_SSL.tar.gz > openssl-$FIPS_VALIDATED_SSL.tar.gz &&  \
    curl -L https://github.com/openssl/openssl/releases/download/openssl-$INSTALLED_SSL/openssl-$INSTALLED_SSL.tar.gz > openssl-$INSTALLED_SSL.tar.gz &&  \
    tar -xf openssl-$FIPS_VALIDATED_SSL.tar.gz && tar -xf openssl-$INSTALLED_SSL.tar.gz && cd openssl-$FIPS_VALIDATED_SSL && \
    # Configure both versions to enable FIPS and build
    ./Configure enable-fips --prefix=/opt/conda --openssldir=/opt/conda/ssl && make && \
    cd ../openssl-$INSTALLED_SSL && \
    ./Configure enable-fips --prefix=/opt/conda --openssldir=/opt/conda/ssl && make && \
    # Copy validated provider to installed version for testing
    cp ../openssl-$FIPS_VALIDATED_SSL/providers/fips.so providers/. && \
    cp ../openssl-$FIPS_VALIDATED_SSL/providers/fipsmodule.cnf providers/. && \
    make tests && cd ../openssl-$FIPS_VALIDATED_SSL && \
    # After tests pass, install FIPS provider and remove source code
    make install_fips && cd .. && rm -rf ./openssl-* && \
# Create new config file with fips-enabled. Then user can override OPENSSL_CONF to enable FIPS
# e.g. export OPENSSL_CONF=/opt/conda/ssl/openssl-fips.cnf
    cp /opt/conda/ssl/openssl.cnf /opt/conda/ssl/openssl-fips.cnf && \
    sed -i "s:# .include fipsmodule.cnf:.include /opt/conda/ssl/fipsmodule.cnf:" /opt/conda/ssl/openssl-fips.cnf && \
    sed -i 's:# fips = fips_sect:fips = fips_sect:' /opt/conda/ssl/openssl-fips.cnf && \
# Install Kerberos.
# Make sure no dependency is added/updated
    pip install "krb5>=0.5.1,<0.6" && \
    pip show krb5 | grep Require | xargs -i sh -c '[ $(echo {} | cut -d: -f2 | wc -w) -eq 0 ] ' && \
# https://stackoverflow.com/questions/122327
    SYSTEM_PYTHON_PATH=$(python3 -c "from __future__ import print_function;import sysconfig; print(sysconfig.get_paths().get('purelib'))") && \
    # Remove SparkRKernel as it's not supported \
    jupyter-kernelspec remove -f -y sparkrkernel && \
    # Patch Sparkmagic lib to support Custom Certificates \
    # https://github.com/jupyter-incubator/sparkmagic/pull/435/files \
    cp -a ${SYSTEM_PYTHON_PATH}/sagemaker_studio_analytics_extension/patches/configuration.py ${SYSTEM_PYTHON_PATH}/sparkmagic/utils/ && \
    cp -a ${SYSTEM_PYTHON_PATH}/sagemaker_studio_analytics_extension/patches/reliablehttpclient.py ${SYSTEM_PYTHON_PATH}/sparkmagic/livyclientlib/reliablehttpclient.py && \
    sed -i 's=  "python"=  "/opt/conda/bin/python"=g'  /opt/conda/share/jupyter/kernels/pysparkkernel/kernel.json /opt/conda/share/jupyter/kernels/sparkkernel/kernel.json && \
    sed -i 's="Spark"="SparkMagic Spark"=g'  /opt/conda/share/jupyter/kernels/sparkkernel/kernel.json && \
    sed -i 's="PySpark"="SparkMagic PySpark"=g'  /opt/conda/share/jupyter/kernels/pysparkkernel/kernel.json && \
    # Configure RTC - disable jupyter_collaboration by default
    jupyter labextension disable @jupyter/collaboration-extension && \
    # Disable docprovider-extension for v3 and above images
    jupyter labextension disable @jupyter/docprovider-extension

# Patch glue kernels to use kernel wrapper
COPY patch_glue_pyspark.json /opt/conda/share/jupyter/kernels/glue_pyspark/kernel.json
COPY patch_glue_spark.json /opt/conda/share/jupyter/kernels/glue_spark/kernel.json

USER root

# Create logging directories for supervisor
RUN mkdir -p $SAGEMAKER_LOGGING_DIR && \
    chmod a+rw $SAGEMAKER_LOGGING_DIR && \
    mkdir -p ${STUDIO_LOGGING_DIR} && \
    chown ${NB_USER}:${MAMBA_USER} ${STUDIO_LOGGING_DIR} && \
    # Create sagemaker pysdk admin default config directory
    mkdir -p /etc/xdg/sagemaker && \
    chmod a+rw /etc/xdg/sagemaker && \
    # Clean up CodeEditor artifacts
    rm -rf /etc/code-editor && \
    # Create supervisord runtime directory
    mkdir -p /var/run/supervisord && \
    chmod a+rw /var/run/supervisord && \
    # Create root directory for DB
    # Create logging directories for supervisor
    mkdir -p $DB_ROOT_DIR && \
    chmod a+rw $DB_ROOT_DIR && \
    HOME_DIR="/home/${NB_USER}/licenses" \
    && mkdir -p ${HOME_DIR} \
    && curl -o ${HOME_DIR}/oss_compliance.zip https://aws-dlinfra-utilities.s3.amazonaws.com/oss_compliance.zip \
    && unzip ${HOME_DIR}/oss_compliance.zip -d ${HOME_DIR}/ \
    && cp ${HOME_DIR}/oss_compliance/test/testOSSCompliance /usr/local/bin/testOSSCompliance \
    && chmod +x /usr/local/bin/testOSSCompliance \
    && chmod +x ${HOME_DIR}/oss_compliance/generate_oss_compliance.sh \
    && ${HOME_DIR}/oss_compliance/generate_oss_compliance.sh ${HOME_DIR} python \
    && rm -rf ${HOME_DIR}/oss_compliance*

# Explicitly disable BuildKit for SM Studio Docker functionality
ENV DOCKER_BUILDKIT=0
ENV PATH="/etc/sagemaker-inference-server:/opt/conda/bin:/opt/conda/condabin:$PATH"
WORKDIR "/home/${NB_USER}"
ENV SHELL=/bin/bash
ENV OPENSSL_MODULES=/opt/conda/lib64/ossl-modules/
USER $MAMBA_USER
