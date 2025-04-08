ARG SAGEMAKER_DISTRIBUTION_IMAGE
FROM $SAGEMAKER_DISTRIBUTION_IMAGE

ARG MAMBA_DOCKERFILE_ACTIVATE=1

ENV AWS_REGION='us-west-2'
ENV DataZoneUserId=2222
ENV DataZoneUserName=mary
ENV DataZoneUserEmail=mary@maxdome.com
ENV DataZoneDomainId=dzd_d3xxovcphmcpzk
ENV DataZoneProjectId=50d2vxs0avlj80
ENV DataZoneProjectRepositoryName=maxdome-50d2vxs0avlj80-dev

COPY --chown=$MAMBA_USER:$MAMBA_USER scripts/run_sagemaker_workflows_tests.sh .
RUN chmod +x run_sagemaker_workflows_tests.sh
CMD ["./run_sagemaker_workflows_tests.sh"]
