# Change log: 4.4.3 (cpu)

This page lists all package changes since the previous release (4.4.2).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
mlflow|3.15.1|3.15.2|patch
uv|0.12.5|0.12.6|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
llvm-openmp|22.1.8|23.1.0|major
jupyter_server|2.20.0|2.21.0|minor
google-auth|2.56.3|2.57.0|minor
statsmodels|0.14.6|0.15.0|minor
websockets|17.0.1|17.1|minor
google-resumable-media|2.8.0|2.10.2|minor
google-cloud-bigquery-core|3.43.0|3.44.0|minor
jiter|0.15.0|0.16.0|minor
mmh3|5.2.1|5.3.0|minor
sagemaker-core|2.20.0|2.21.0|minor
slack-sdk|3.43.0|3.44.0|minor
platformdirs|4.11.4|4.11.5|patch
msgpack-python|1.2.1|1.2.2|patch
virtualenv|21.7.4|21.7.5|patch
fastcore|2.2.15|2.2.16|patch
gitpython|3.1.59|3.1.60|patch
graphql-core|3.2.11|3.2.12|patch
mlflow-skinny|3.15.1|3.15.2|patch
mlflow-ui|3.15.1|3.15.2|patch

### New

Package | Version
---|---
interface_meta|1.3.0
formulaic|1.2.2
