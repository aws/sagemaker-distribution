# Change log: 4.5.0 (gpu)

This page lists all package changes since the previous release (4.4.1).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
python|3.12.13|3.12.14|patch
conda|26.7.0|26.7.1|patch
mlflow|3.15.1|3.15.2|patch
sagemaker-studio|1.1.30|1.1.32|patch
uv|0.12.5|0.12.6|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
llvm-openmp|22.1.8|23.1.0|major
argon2-cffi-bindings|25.1.0|26.1.0|major
cached_property|1.5.2|2.0.1|major
cached-property|1.5.2|2.0.1|major
libgcc|16.1.0|16.2.0|minor
libstdcxx|16.1.0|16.2.0|minor
libgcc-ng|16.1.0|16.2.0|minor
libstdcxx-ng|16.1.0|16.2.0|minor
rdma-core|63.0|63.1|minor
optree|0.19.1|0.20.0|minor
narwhals|2.24.0|2.25.0|minor
libgfortran5|16.1.0|16.2.0|minor
libgfortran|16.1.0|16.2.0|minor
google-auth|2.56.3|2.57.0|minor
google-api-core|2.29.0|2.33.0|minor
cloudpathlib|0.24.0|0.25.0|minor
databricks-sdk|0.132.0|0.133.0|minor
websockets|17.0.1|17.1|minor
fastar|0.11.0|0.12.0|minor
google-resumable-media|2.8.0|2.10.2|minor
google-cloud-bigquery-core|3.43.0|3.18.0|minor
gunicorn|26.1.0|26.2.0|minor
mmh3|5.2.1|5.3.0|minor
sagemaker-core|2.20.0|2.21.0|minor
sqlalchemy-bigquery|1.17.2|1.16.0|minor
trino-python-client|0.338.0|0.339.0|minor
openssl|3.6.3|3.6.4|patch
cpython|3.12.13|3.12.14|patch
python-gil|3.12.13|3.12.14|patch
filelock|3.32.3|3.32.4|patch
platformdirs|4.11.3|4.11.4|patch
python-discovery|1.5.2|1.5.3|patch
virtualenv|21.7.4|21.7.5|patch
fastcore|2.2.13|2.2.16|patch
cyclopts|4.23.0|4.23.1|patch
deltalake|1.6.2|1.6.3|patch
gitpython|3.1.59|3.1.60|patch
langsmith|0.11.0|0.11.1|patch
linkify-it-py|2.1.0|2.1.1|patch
mlflow-skinny|3.15.1|3.15.2|patch
mlflow-ui|3.15.1|3.15.2|patch
nh3|0.3.6|0.3.7|patch

### Removed

Package | Last Version
---|---
google-api-core-grpc|2.29.0
