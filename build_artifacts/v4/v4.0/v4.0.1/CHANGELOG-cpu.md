# Change log: 4.0.1 (cpu)

This page lists all package changes since the previous release (4.0.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
amzn-sagemaker-aiops-jupyterlab-extension|1.0.5|1.0.6|patch
conda|26.3.1|26.3.2|patch
sagemaker-code-editor|1.9.4|1.9.5|patch
sagemaker-studio|1.1.8|1.1.12|patch
uv|0.11.4|0.11.7|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
importlib_resources|6.5.2|7.1.0|major
cryptography|44.0.3|46.0.7|major
pyopenssl|24.3.0|25.3.0|major
gdown|5.2.1|6.0.0|major
libsqlite|3.52.0|3.53.0|minor
filelock|3.25.2|3.28.0|minor
greenlet|3.3.2|3.4.0|minor
prometheus_client|0.24.1|0.25.0|minor
pydantic-core|2.41.5|2.46.2|minor
pydantic|2.12.5|2.13.2|minor
snowflake-connector-python|3.13.2|3.17.4|minor
apsw|3.52.0.0|3.53.0.0|minor
google-api-core|2.30.2|2.29.0|minor
opentelemetry-api|1.40.0|1.41.0|minor
opentelemetry-sdk|1.40.0|1.41.0|minor
opentelemetry-proto|1.40.0|1.41.0|minor
smart_open|7.5.1|7.6.0|minor
smart-open|7.5.1|7.6.0|minor
awswrangler|3.15.1|3.16.0|minor
deltalake|1.3.2|1.5.0|minor
dnspython|2.7.0|2.8.0|minor
google-cloud-bigquery-core|3.18.0|3.41.0|minor
sagemaker-core|2.7.1|2.8.0|minor
llvm-openmp|22.1.2|22.1.3|patch
liblzma|5.8.2|5.8.3|patch
libpng|1.6.56|1.6.58|patch
libjpeg-turbo|3.1.2|3.1.4.1|patch
zipp|3.23.0|3.23.1|patch
mako|1.3.10|1.3.11|patch
platformdirs|4.9.4|4.9.6|patch
langsmith|0.7.26|0.7.32|patch
fastcore|1.12.34|1.12.39|patch
google-auth|2.49.1|2.49.2|patch
virtualenv|21.2.0|21.2.4|patch
rich|14.3.3|14.3.4|patch
python-multipart|0.0.24|0.0.26|patch
reproc|14.2.5.post0|14.2.7.post0|patch
reproc-cpp|14.2.5.post0|14.2.7.post0|patch
python-duckdb|1.5.1|1.5.2|patch
duckdb|1.5.1|1.5.2|patch
jupyter_ydoc|3.4.0|3.4.1|patch
param|2.3.2|2.3.3|patch
opentelemetry-semantic-conventions|0.61b0|0.62b0|
opentelemetry-exporter-prometheus|0.61b0|0.62b0|
opentelemetry-instrumentation|0.61b0|0.62b0|
opentelemetry-instrumentation-threading|0.61b0|0.62b0|

### New

Package | Version
---|---
google-api-core-grpc|2.29.0
sqlglot|28.10.1
