# Change log: 4.6.0 (cpu)

This page lists all package changes since the previous release (4.5.1).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
uvicorn|0.52.4|0.53.0|minor
docker-cli|29.7.1|29.8.1|minor
jupyter-server-proxy|4.5.0|4.6.0|minor
mlflow|3.15.2|3.16.0|minor
jupyterlab|4.5.10|4.5.11|patch
sagemaker-studio-dataengineering-extensions|1.3.14|1.3.15|patch
uv|0.12.15|0.12.18|patch

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
python-tzdata|2026.3|2026.4|minor
pyjwt|2.13.0|2.14.0|minor
virtualenv|21.7.9|21.10.0|minor
gdown|6.2.0|6.4.0|minor
cachetools|7.1.8|7.2.0|minor
conda-self|0.2.1|0.3.0|minor
databricks-sdk|0.138.0|0.141.0|minor
watchfiles|1.2.0|1.3.0|minor
uvicorn-standard|0.52.4|0.53.0|minor
langsmith|0.12.4|0.14.0|minor
mlflow-skinny|3.15.2|3.16.0|minor
mlflow-ui|3.15.2|3.16.0|minor
skops|0.14|0.15|minor
sqlglot|30.18.0|30.19.0|minor
llvm-openmp|23.1.1|23.1.2|patch
libexpat|2.8.1|2.8.4|patch
libuuid|2.42.3|2.42.4|patch
fribidi|1.0.16|1.0.17|patch
wrapt|2.4.0|2.4.1|patch
greenlet|3.5.5|3.5.6|patch
sqlalchemy|2.0.52|2.0.54|patch
platformdirs|4.11.8|4.11.12|patch
tornado|6.5.8|6.5.10|patch
debugpy|1.8.21|1.8.22|patch
wcwidth|0.8.3|0.8.5|patch
expat|2.8.1|2.8.4|patch
pyparsing|3.3.2|3.3.3|patch
python-discovery|1.6.0|1.6.1|patch
fastcore|2.2.25|2.2.30|patch
conda-lockfiles|0.2.1|0.2.2|patch
python-build|1.6.0|1.6.1|patch
coverage|7.16.0|7.16.1|patch
cyclopts|4.25.2|4.25.3|patch
jupyterlab-chat|0.25.0|0.25.1|patch
pylint|4.0.8|4.0.9|patch

### New

Package | Version
---|---
python-abi3|3.12
