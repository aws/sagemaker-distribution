# Change log: 2.13.8 (gpu)

This page lists all package changes since the previous release (2.13.7).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
sagemaker-jupyterlab-extension|0.5.7|0.5.9|patch
sagemaker-studio|1.1.15|1.1.20|patch
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
idna|3.13|3.17|minor
libcap|2.77|2.78|minor
libsystemd0|260.1|260.2|minor
libudev1|260.1|260.2|minor
libuv|1.51.0|1.52.1|minor
fontconfig|2.17.1|2.18.1|minor
frozenlist|1.7.0|1.8.0|minor
propcache|0.3.1|0.5.2|minor
yarl|1.23.0|1.24.2|minor
narwhals|2.21.2|2.22.0|minor
platformdirs|4.9.6|4.10.0|minor
jupyter_server|2.18.2|2.19.0|minor
python-xxhash|3.6.0|3.7.0|minor
uuid-utils|0.15.0|0.16.0|minor
pyjwt|2.12.1|2.13.0|minor
python-discovery|1.3.1|1.4.0|minor
virtualenv|21.3.3|21.4.2|minor
gdown|6.0.0|6.1.0|minor
typer|0.25.1|0.26.7|minor
libboost|1.88.0|1.90.0|minor
optuna|4.8.0|4.9.0|minor
black|26.3.1|26.5.1|minor
httptools|0.7.1|0.8.0|minor
jiter|0.13.0|0.15.0|minor
opentelemetry-api|1.41.0|1.42.1|minor
opentelemetry-sdk|1.41.0|1.42.1|minor
param|2.3.3|2.4.0|minor
panel|1.8.10|1.9.3|minor
snowballstemmer|3.0.1|3.1.1|minor
snowflake-sqlalchemy|1.9.0|1.10.0|minor
llvm-openmp|22.1.5|22.1.7|patch
libexpat|2.8.0|2.8.1|patch
filelock|3.29.0|3.29.1|patch
graphite2|1.3.14|1.3.15|patch
aiohappyeyeballs|2.6.1|2.6.2|patch
greenlet|3.5.0|3.5.1|patch
sqlalchemy|2.0.49|2.0.50|patch
alsa-lib|1.2.15.3|1.2.16|patch
debugpy|1.8.20|1.8.21|patch
traitlets|5.15.0|5.15.1|patch
tornado|6.5.5|6.5.6|patch
soupsieve|2.8.3|2.8.4|patch
click|8.4.0|8.4.1|patch
langsmith|0.8.5|0.8.9|patch
sagemaker-jupyterlab-extension-common|0.4.3|0.4.5|patch
expat|2.8.0|2.8.1|patch
distlib|0.4.0|0.4.1|patch
pytorch-lightning|2.6.1|2.6.5|patch
libavif16|1.4.1|1.4.2|patch
python-multipart|0.0.29|0.0.30|patch
ujson|5.12.0|5.12.1|patch
ocl-icd|2.3.3|2.3.4|patch
awswrangler|3.16.0|3.16.1|patch
libsolv|0.7.37|0.7.39|patch
coverage|7.14.0|7.14.1|patch
python-duckdb|1.5.2|1.5.3|patch
duckdb|1.5.2|1.5.3|patch
rich-toolkit|0.19.9|0.19.10|patch
fastapi-cli|0.0.23|0.0.24|patch
opentelemetry-semantic-conventions|0.62b0|0.63b1|
opentelemetry-instrumentation|0.62b0|0.63b1|
opentelemetry-instrumentation-threading|0.62b0|0.63b1|

### New

Package | Version
---|---
lz4|4.4.5
nh3|0.3.5
panel-core|1.9.3
panel-material-ui|0.11.2
tzlocal|5.3.1
trino-python-client|0.337.0
vertica-python|1.4.0
