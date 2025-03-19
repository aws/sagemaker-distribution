ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN micromamba install -y --freeze-installed -c conda-forge pytest

RUN python -c "import sagemaker_data_explorer"
RUN jupyter labextension list &>  >(grep --color=never @amzn/sagemaker-data-explorer-jl-plugin) | grep  enabled

RUN jupyter labextension list &> >(grep --color=never @amzn/sagemaker-connection-magics-jlextension) | grep enabled

RUN python -c "import sagemaker_ui_doc_manager_jl_plugin"
RUN jupyter labextension list &>  >(grep --color=never @amzn/sagemaker-ui-doc-manager-jl-plugin) | grep  enabled

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_sagemaker_studio_dataengineering_extensions_test.sh .
RUN chmod +x run_sagemaker_studio_dataengineering_extensions_test.sh
CMD ["./run_sagemaker_studio_dataengineering_extensions_test.sh"]