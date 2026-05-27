# Change log: 2.14.6 (cpu)

This page lists all package changes since the previous release (2.14.5).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
sagemaker-jupyterlab-extension|0.5.7|0.5.9|patch
sagemaker-studio|1.1.15|1.1.19|patch
sagemaker-studio-dataengineering-sessions|1.3.20|1.3.21|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
pycparser|2.22|3.0|major
ca-certificates|2026.4.22|2026.5.20|minor
certifi|2026.4.22|2026.5.20|minor
idna|3.13|3.15|minor
libuv|1.51.0|1.52.1|minor
fontconfig|2.17.1|2.18.0|minor
yarl|1.23.0|1.24.2|minor
uuid-utils|0.15.0|0.16.0|minor
pyjwt|2.12.1|2.13.0|minor
starlette|1.0.0|1.1.0|minor
typer|0.25.1|0.26.0|minor
libboost|1.88.0|1.90.0|minor
black|26.3.1|26.5.1|minor
httptools|0.7.1|0.8.0|minor
opentelemetry-api|1.41.0|1.42.1|minor
opentelemetry-sdk|1.41.0|1.42.1|minor
param|2.3.3|2.4.0|minor
panel|1.8.10|1.9.1|minor
snowballstemmer|3.0.1|3.1.0|minor
snowflake-sqlalchemy|1.9.0|1.10.0|minor
llvm-openmp|22.1.5|22.1.6|patch
libexpat|2.8.0|2.8.1|patch
aiohappyeyeballs|2.6.1|2.6.2|patch
greenlet|3.5.0|3.5.1|patch
sqlalchemy|2.0.49|2.0.50|patch
soupsieve|2.8.3|2.8.4|patch
expat|2.8.0|2.8.1|patch
ujson|5.12.0|5.12.1|patch
awswrangler|3.16.0|3.16.1|patch
libsolv|0.7.37|0.7.38|patch
coverage|7.14.0|7.14.1|patch
python-duckdb|1.5.2|1.5.3|patch
duckdb|1.5.2|1.5.3|patch
rich-toolkit|0.19.9|0.19.10|patch
opentelemetry-semantic-conventions|0.62b0|0.63b1|
opentelemetry-instrumentation|0.62b0|0.63b1|
opentelemetry-instrumentation-threading|0.62b0|0.63b1|

### New

Package | Version
---|---
nh3|0.3.5
panel-material-ui|0.11.0
vertica-python|1.4.0
