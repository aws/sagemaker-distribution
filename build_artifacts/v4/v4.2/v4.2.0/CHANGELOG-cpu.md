# Change log: 4.2.0 (cpu)

This page lists all package changes since the previous release (4.1.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
s3fs|2026.3.0|2026.4.0|minor
jupyterlab|4.5.6|4.5.7|patch
notebook|7.5.5|7.5.6|patch
sagemaker-code-editor|1.9.5|1.9.6|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
cryptography|46.0.7|44.0.3|major
pyopenssl|25.3.0|24.3.0|major
fastmcp|3.2.4|2.10.6|major
fsspec|2026.3.0|2026.4.0|minor
libdeflate|1.24|1.25|minor
snowflake-connector-python|3.17.4|3.13.2|minor
cloudpathlib|0.23.0|0.24.0|minor
databricks-sdk|0.105.0|0.106.0|minor
dnspython|2.8.0|2.7.0|minor
sagemaker-core|2.9.0|2.7.1|minor
typer|0.25.0|0.25.1|patch
gitpython|3.1.48|3.1.49|patch
jupyter-ai-router|0.0.4|0.0.5|patch
langsmith|0.7.37|0.7.38|patch

### Removed

Package | Last Version
---|---
caio|0.9.25
aiofile|3.9.0
backports|1.0
backports.tarfile|1.2.0
griffelib|2.0.2
joserfc|1.6.4
jsonref|1.1.0
pathable|0.5.0
jsonschema-path|0.4.6
more-itertools|11.0.2
jaraco.classes|3.4.0
jaraco.context|6.1.2
jaraco.functools|4.4.0
jeepney|0.9.0
secretstorage|3.4.1
keyring|25.7.0
py-key-value-aio|0.4.4
uncalled-for|0.3.1
