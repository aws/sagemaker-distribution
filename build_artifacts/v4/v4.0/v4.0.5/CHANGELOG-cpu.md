# Change log: 4.0.5 (cpu)

This page lists all package changes since the previous release (4.0.4).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
sagemaker-jupyterlab-extension|0.5.7|0.5.9|patch
sagemaker-studio|1.1.19|1.1.20|patch
uv|0.11.15|0.11.16|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
idna|3.15|3.17|minor
libuv|1.51.0|1.52.1|minor
fontconfig|2.17.1|2.18.0|minor
python-xxhash|3.6.0|3.7.0|minor
platformdirs|4.9.6|4.10.0|minor
pyjwt|2.12.1|2.13.0|minor
pyathena|3.30.1|3.31.0|minor
google-api-core|2.30.3|2.29.0|minor
opentelemetry-api|1.41.0|1.42.1|minor
opentelemetry-sdk|1.41.0|1.42.1|minor
python-discovery|1.3.1|1.4.0|minor
virtualenv|21.3.3|21.4.1|minor
starlette|1.0.0|1.1.0|minor
typer|0.25.1|0.26.3|minor
libboost|1.88.0|1.90.0|minor
black|26.3.1|26.5.1|minor
databricks-sdk|0.110.0|0.112.0|minor
httptools|0.7.1|0.8.0|minor
google-cloud-bigquery-core|3.18.0|3.41.0|minor
jiter|0.13.0|0.15.0|minor
snowballstemmer|3.0.1|3.1.0|minor
sqlalchemy-bigquery|1.16.0|1.17.0|minor
sqlalchemy|2.0.49|2.0.50|patch
tornado|6.5.5|6.5.6|patch
langsmith|0.8.5|0.8.6|patch
soupsieve|2.8.3|2.8.4|patch
libavif16|1.4.1|1.4.2|patch
ujson|5.12.0|5.12.1|patch
libsolv|0.7.37|0.7.38|patch
coverage|7.14.0|7.14.1|patch
panel|1.9.0|1.9.1|patch
opentelemetry-semantic-conventions|0.62b0|0.63b1|
opentelemetry-exporter-prometheus|0.62b0|0.63b1|
opentelemetry-instrumentation|0.62b0|0.63b1|
opentelemetry-instrumentation-threading|0.62b0|0.63b1|

### New

Package | Version
---|---
google-api-core-grpc|2.29.0
lz4|4.4.5
tzlocal|5.3.1
trino-python-client|0.337.0
