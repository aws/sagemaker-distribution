#!/bin/bash

# We need to checkout the version of sagemaker-python-sdk that is installed in the mamba environment.

pysdk_version=$(micromamba list | grep sagemaker-python-sdk | tr -s ' ' | cut -d ' ' -f 3)
# Checkout the corresponding sagemaker-python-sdk version
git checkout tags/v$pysdk_version

# Install test dependencies of sagemaker-python-sdk
# Using pip as some of the packages are not available on conda-forge
pip install --use-deprecated=legacy-resolver -r requirements/extras/test_requirements.txt

# Run the unit tests, ignoring tests which require AWS Configuration
# TODO: Re-evaluate the ignored tests since we are setting the AWS_DEFAULT_REGION as part of the Dockerfile.
# Test cases are being skipped where S3 Operations are being executed, accessing local container server.
pytest tests/unit --ignore tests/unit/sagemaker/feature_store/ --ignore tests/unit/sagemaker/jumpstart/ --ignore tests/unit/sagemaker/workflow/ \
    --ignore tests/unit/sagemaker/async_inference --ignore tests/unit/test_model_card.py --ignore tests/unit/test_model_card.py --ignore tests/unit/test_processing.py \
    --ignore tests/unit/test_tensorboard.py --ignore tests/unit/sagemaker/async_inference --ignore tests/unit/sagemaker/experiments --ignore tests/unit/sagemaker/local \
    --ignore tests/unit/sagemaker/monitor/test_data_capture_config.py --ignore tests/unit/sagemaker/experiments --ignore tests/unit/sagemaker/remote_function \
    --ignore tests/unit/sagemaker/model/test_deploy.py --ignore tests/unit/sagemaker/image_uris/jumpstart/test_common.py \
    --deselect tests/unit/sagemaker/serve/builder/test_djl_builder.py::test_tune_for_djl_local_container_deep_ping_ex \
    --deselect tests/unit/sagemaker/serve/builder/test_djl_builder.py::test_tune_for_djl_local_container_invoke_ex \
    --deselect tests/unit/sagemaker/serve/builder/test_djl_builder.py::test_tune_for_djl_local_container_load_ex \
    --deselect tests/unit/sagemaker/serve/builder/test_djl_builder.py::test_tune_for_djl_local_container_oom_ex \
    --deselect tests/unit/sagemaker/serve/builder/test_model_builder.py::TestModelBuilder::test_build_negative_path_when_schema_builder_not_present \
    --deselect tests/unit/sagemaker/serve/builder/test_model_builder.py::TestModelBuilder::test_build_task_override_with_invalid_task_provided \
    --deselect tests/unit/sagemaker/serve/builder/test_model_builder.py::TestModelBuilder::test_model_server_override_djl_with_model \
    --deselect tests/unit/sagemaker/serve/builder/test_model_builder.py::TestModelBuilder::test_model_server_override_tei_with_model \
    --deselect tests/unit/sagemaker/serve/builder/test_model_builder.py::TestModelBuilder::test_model_server_override_tensor_with_model \
    --deselect tests/unit/sagemaker/serve/builder/test_model_builder.py::TestModelBuilder::test_model_server_override_tgi_with_model \
    --deselect tests/unit/sagemaker/serve/builder/test_model_builder.py::TestModelBuilder::test_model_server_override_torchserve_with_model \
    --deselect tests/unit/sagemaker/serve/builder/test_model_builder.py::TestModelBuilder::test_model_server_override_transformers_with_model \
    --deselect tests/unit/sagemaker/serve/builder/test_model_builder.py::TestModelBuilder::test_model_server_override_triton_with_model \
    --deselect tests/unit/sagemaker/serve/builder/test_tei_builder.py::TestTEIBuilder::test_build_deploy_for_tei_local_container_and_remote_container \
    --deselect tests/unit/sagemaker/serve/builder/test_tei_builder.py::TestTEIBuilder::test_image_uri_override \
    --deselect tests/unit/sagemaker/serve/builder/test_transformers_builder.py::TestTransformersBuilder::test_build_deploy_for_transformers_local_container_and_remote_container \
    --deselect tests/unit/sagemaker/serve/builder/test_transformers_builder.py::TestTransformersBuilder::test_failure_hf_md \
    --deselect tests/unit/sagemaker/serve/builder/test_transformers_builder.py::TestTransformersBuilder::test_image_uri_override \
    --deselect tests/unit/sagemaker/serve/detector/test_image_detector.py::TestImageDetector::test_detect_latest_downcast_xgb \
    --deselect tests/unit/sagemaker/serve/model_server/tei/test_server.py::TeiServerTests::test_start_invoke_destroy_local_tei_server \
    --deselect tests/unit/sagemaker/serve/model_server/triton/test_server.py::TritonServerTests::test_start_invoke_destroy_local_triton_server_cpu \
    --deselect tests/unit/sagemaker/serve/model_server/triton/test_server.py::TritonServerTests::test_start_invoke_destroy_local_triton_server_gpu \
    --deselect tests/unit/test_estimator.py::test_insert_invalid_source_code_args \
    --deselect tests/unit/sagemaker/model_uris/jumpstart/test_common.py::test_jumpstart_common_model_uri \
    --deselect tests/unit/sagemaker/monitor/test_model_monitoring.py::test_model_quality_monitor_update_failure \
    --deselect tests/unit/sagemaker/script_uris/jumpstart/test_common.py::test_jumpstart_common_script_uri \
    --deselect tests/unit/sagemaker/serve/builder/test_djl_builder.py::TestDjlBuilder::test_tune_for_djl_local_container_deep_ping_ex \
    --deselect tests/unit/sagemaker/serve/builder/test_djl_builder.py::TestDjlBuilder::test_tune_for_djl_local_container_invoke_ex \
    --deselect tests/unit/sagemaker/serve/builder/test_djl_builder.py::TestDjlBuilder::test_tune_for_djl_local_container_load_ex \
    --deselect tests/unit/sagemaker/serve/builder/test_djl_builder.py::TestDjlBuilder::test_tune_for_djl_local_container_oom_ex \
    --deselect tests/unit/sagemaker/tensorflow/test_estimator.py::test_insert_invalid_source_code_args || exit $?
