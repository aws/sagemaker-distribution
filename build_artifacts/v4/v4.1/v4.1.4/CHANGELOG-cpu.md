# Change log: 4.1.4 (cpu)

This page lists all package changes since the previous release (4.1.3).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
sagemaker-jupyterlab-extension-common|0.4.3|0.4.5|patch
fastapi|0.136.1|0.136.3|patch
sagemaker-jupyterlab-extension|0.5.7|0.5.9|patch
uv|0.11.15|0.11.16|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
rich-rst|1.3.2|2.0.1|major
libuv|1.51.0|1.52.1|minor
fontconfig|2.17.1|2.18.0|minor
pyjwt|2.12.1|2.13.0|minor
pyathena|3.30.1|3.31.0|minor
opentelemetry-api|1.41.0|1.42.1|minor
opentelemetry-sdk|1.41.0|1.42.1|minor
starlette|1.0.0|1.1.0|minor
typer|0.25.1|0.26.0|minor
libboost|1.88.0|1.90.0|minor
black|26.3.1|26.5.1|minor
cyclopts|4.14.0|4.16.1|minor
databricks-sdk|0.110.0|0.111.0|minor
httptools|0.7.1|0.8.0|minor
more-itertools|11.0.2|11.1.0|minor
param|2.3.3|2.4.0|minor
panel|1.8.10|1.9.1|minor
snowballstemmer|3.0.1|3.1.0|minor
sagemaker-train|1.11.0|1.12.0|minor
sagemaker-serve|1.11.0|1.12.0|minor
sagemaker-mlops|1.11.0|1.12.0|minor
snowflake-sqlalchemy|1.9.0|1.10.0|minor
llvm-openmp|22.1.5|22.1.6|patch
sqlalchemy|2.0.49|2.0.50|patch
soupsieve|2.8.3|2.8.4|patch
joserfc|1.6.5|1.6.7|patch
opentelemetry-proto|1.42.0|1.42.1|patch
ujson|5.12.0|5.12.1|patch
awswrangler|3.16.0|3.16.1|patch
libsolv|0.7.37|0.7.38|patch
coverage|7.14.0|7.14.1|patch
rich-toolkit|0.19.9|0.19.10|patch
fastapi-core|0.136.1|0.136.3|patch
opentelemetry-semantic-conventions|0.62b0|0.63b1|
opentelemetry-exporter-prometheus|0.62b0|0.63b1|
opentelemetry-instrumentation|0.62b0|0.63b1|
opentelemetry-instrumentation-threading|0.62b0|0.63b1|

### New

Package | Version
---|---
nh3|0.3.5
panel-material-ui|0.11.0

### Removed

Package | Last Version
---|---
docutils|0.22.4
