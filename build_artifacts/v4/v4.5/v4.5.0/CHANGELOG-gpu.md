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

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
argon2-cffi-bindings|25.1.0|26.1.0|major
optree|0.19.1|0.20.0|minor
narwhals|2.24.0|2.25.0|minor
google-api-core|2.29.0|2.33.0|minor
cloudpathlib|0.24.0|0.25.0|minor
databricks-sdk|0.132.0|0.133.0|minor
fastar|0.11.0|0.12.0|minor
google-cloud-bigquery-core|3.43.0|3.18.0|minor
sqlalchemy-bigquery|1.17.2|1.16.0|minor
trino-python-client|0.338.0|0.339.0|minor
cpython|3.12.13|3.12.14|patch
python-gil|3.12.13|3.12.14|patch
filelock|3.32.3|3.32.4|patch
cyclopts|4.23.0|4.23.1|patch
deltalake|1.6.2|1.6.3|patch
langsmith|0.11.0|0.11.1|patch
nh3|0.3.6|0.3.7|patch

### Removed

Package | Last Version
---|---
google-api-core-grpc|2.29.0
