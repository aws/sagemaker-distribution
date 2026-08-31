# Change log: 4.2.8 (gpu)

This page lists all package changes since the previous release (4.2.7).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
sagemaker-studio-dataengineering-sessions|1.3.24|1.3.25|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
llvm-openmp|22.1.8|23.1.0|major
isort|8.0.1|9.0.1|major
jupyter_client|8.9.1|8.10.0|minor
jupyter_server|2.20.0|2.21.0|minor
authlib|1.7.2|1.8.0|minor
google-auth|2.56.3|2.57.0|minor
google-api-core|2.33.0|2.29.0|minor
python-discovery|1.5.3|1.6.0|minor
statsmodels|0.14.6|0.15.0|minor
python-build|1.5.0|1.6.0|minor
coverage|7.15.4|7.16.0|minor
websockets|17.0.1|17.1|minor
google-resumable-media|2.8.0|2.10.2|minor
google-cloud-bigquery-core|3.18.0|3.44.0|minor
jiter|0.15.0|0.16.0|minor
mmh3|5.2.1|5.3.0|minor
sagemaker-core|2.20.0|2.21.0|minor
sqlalchemy-bigquery|1.16.0|1.17.2|minor
slack-sdk|3.43.0|3.44.0|minor
pydantic-core|2.46.4|2.46.5|patch
pydantic|2.13.4|2.13.5|patch
platformdirs|4.11.4|4.11.5|patch
fastcore|2.2.15|2.2.17|patch
joserfc|1.7.4|1.7.5|patch
kiwisolver|1.5.0|1.5.1|patch
msgpack-python|1.2.1|1.2.2|patch
virtualenv|21.7.4|21.7.7|patch
typer|0.27.1|0.27.2|patch
patsy|1.0.2|1.0.3|patch
gitpython|3.1.59|3.1.61|patch
graphql-core|3.2.11|3.2.12|patch
langsmith|0.11.1|0.11.2|patch
pylint|4.0.7|4.0.8|patch
pyspnego|0.12.1|0.12.2|patch

### New

Package | Version
---|---
interface_meta|1.3.0
formulaic|1.2.2
google-api-core-grpc|2.29.0
