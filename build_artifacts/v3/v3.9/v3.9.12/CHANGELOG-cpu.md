# Change log: 3.9.12 (cpu)

This page lists all package changes since the previous release (3.9.11).

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
dask-core|2026.7.1|2026.8.0|minor
distributed|2026.7.1|2026.8.0|minor
websockets|17.0.1|17.1|minor
langsmith|0.11.1|0.12.1|minor
regex|2026.7.19|2026.9.3|minor
pandoc|3.10.2|3.11|minor
joblib|1.5.3|1.6.0|minor
google-auth|2.56.3|2.57.0|minor
python-discovery|1.5.3|1.6.0|minor
statsmodels|0.14.6|0.15.0|minor
coverage|7.15.4|7.16.0|minor
google-resumable-media|2.8.0|2.10.2|minor
google-cloud-bigquery-core|3.43.0|3.44.0|minor
jiter|0.15.0|0.16.0|minor
linkify-it-py|2.1.1|2.2.0|minor
opentelemetry-api|1.43.0|1.44.0|minor
opentelemetry-sdk|1.43.0|1.44.0|minor
mmh3|5.2.1|5.3.0|minor
slack-sdk|3.43.0|3.44.0|minor
filelock|3.32.4|3.32.5|patch
wcwidth|0.8.2|0.8.3|patch
platformdirs|4.11.4|4.11.6|patch
websocket-client|1.9.0|1.9.2|patch
msgpack-python|1.2.1|1.2.2|patch
pydantic-core|2.46.4|2.46.5|patch
pydantic|2.13.4|2.13.5|patch
kiwisolver|1.5.0|1.5.1|patch
virtualenv|21.7.4|21.7.8|patch
fastcore|2.2.15|2.2.19|patch
typer|0.27.1|0.27.2|patch
patsy|1.0.2|1.0.3|patch
reproc|14.2.7.post0|14.2.8.post0|patch
reproc-cpp|14.2.7.post0|14.2.8.post0|patch
gitpython|3.1.59|3.1.61|patch
graphql-core|3.2.11|3.2.12|patch
pylint|4.0.7|4.0.8|patch
pyspnego|0.12.1|0.12.2|patch
opentelemetry-semantic-conventions|0.64b0|0.65b0|
opentelemetry-instrumentation|0.64b0|0.65b0|
opentelemetry-instrumentation-threading|0.64b0|0.65b0|

### New

Package | Version
---|---
interface_meta|1.3.0
formulaic|1.2.2
