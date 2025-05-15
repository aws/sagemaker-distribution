ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN micromamba install -y --freeze-installed -c conda-forge pytest

RUN python -c "import sagemaker_data_explorer"
RUN jupyter labextension list &>  >(grep --color=never @amzn/sagemaker-data-explorer-jl-plugin) | grep  enabled

RUN jupyter labextension list &> >(grep --color=never @amzn/sagemaker-connection-magics-jlextension) | grep enabled

RUN python -c "import sagemaker_ui_doc_manager_jl_plugin"
RUN jupyter labextension list &>  >(grep --color=never @amzn/sagemaker-ui-doc-manager-jl-plugin) | grep  enabled


RUN jupyter labextension list &>  >(grep --color=never sagemaker_sparkmonitor) | grep  enabled
