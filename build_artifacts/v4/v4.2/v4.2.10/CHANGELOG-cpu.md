# Change log: 4.2.10 (cpu)

This page lists all package changes since the previous release (4.2.9).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
jupyterlab|4.5.10|4.5.11|patch
sagemaker-studio-dataengineering-extensions|1.3.14|1.3.15|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
adwaita-icon-theme|50.0|51.0|major
unicodedata2|17.0.1|18.0.0|major
idna|3.19|3.20|minor
networkx|3.6.1|3.7|minor
pyjwt|2.13.0|2.14.0|minor
google-api-core|2.29.0|2.33.0|minor
virtualenv|21.7.9|21.10.0|minor
threadpoolctl|3.6.0|3.7.0|minor
gdown|6.2.0|6.4.0|minor
cachetools|7.1.8|7.2.0|minor
conda-self|0.2.1|0.3.0|minor
watchfiles|1.2.0|1.3.0|minor
google-cloud-bigquery-core|3.45.0|3.18.0|minor
langsmith|0.12.4|0.13.0|minor
skops|0.14|0.15|minor
pytoolconfig|1.2.5|1.3.1|minor
sqlalchemy-bigquery|1.17.2|1.16.0|minor
libexpat|2.8.1|2.8.4|patch
fribidi|1.0.16|1.0.17|patch
wrapt|2.4.0|2.4.1|patch
greenlet|3.5.5|3.5.6|patch
sqlalchemy|2.0.52|2.0.54|patch
platformdirs|4.11.8|4.11.11|patch
tornado|6.5.8|6.5.10|patch
debugpy|1.8.21|1.8.22|patch
wcwidth|0.8.3|0.8.4|patch
jupyterlab_server|2.28.0|2.28.1|patch
fastcore|2.2.25|2.2.29|patch
expat|2.8.1|2.8.4|patch
pyparsing|3.3.2|3.3.3|patch
python-discovery|1.6.0|1.6.1|patch
coverage|7.16.0|7.16.1|patch
jupyterlab-chat|0.25.0|0.25.1|patch

### New

Package | Version
---|---
python-abi3|3.12

### Removed

Package | Last Version
---|---
google-api-core-grpc|2.29.0
