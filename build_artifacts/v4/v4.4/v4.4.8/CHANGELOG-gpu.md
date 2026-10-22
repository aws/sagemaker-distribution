# Change log: 4.4.8 (gpu)

This page lists all package changes since the previous release (4.4.7).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
amazon_sagemaker_sql_editor|0.2.7|0.2.8|patch
pip|26.2.1|26.2.2|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
ca-certificates|2026.7.22|2026.10.19|minor
certifi|2026.7.22|2026.10.19|minor
setuptools|84.0.0|84.2.1|minor
multidict|6.7.1|6.9.1|minor
jsonpointer|3.2.1|3.4|minor
webencodings|0.5.1|0.6.1|minor
mistune|3.3.4|3.4.0|minor
qt6-main|6.8.3|6.9.0|minor
pyside6|6.8.3|6.9.0|minor
google-api-core|2.29.0|2.33.0|minor
python-slugify|9.0.0|9.1.3|minor
starlette|1.8.0|1.9.0|minor
beartype|0.22.9|0.23.1|minor
databricks-sdk|0.153.0|0.155.0|minor
paramiko|5.0.0|5.1.0|minor
websockets|17.2|17.3|minor
griffelib|2.3.2|2.4.0|minor
google-cloud-bigquery-core|3.46.1|3.18.0|minor
sagemaker-core|2.25.0|2.26.0|minor
sagemaker-train|1.25.0|1.26.0|minor
sagemaker-serve|1.25.0|1.26.0|minor
sagemaker-mlops|1.25.0|1.26.0|minor
sqlalchemy-bigquery|1.17.3|1.16.0|minor
llvm-openmp|23.1.3|23.1.4|patch
c-ares|1.34.8|1.34.9|patch
xorg-libx11|1.8.13|1.8.14|patch
xorg-libxrender|0.9.12|0.9.13|patch
zipp|4.1.1|4.1.2|patch
platformdirs|4.13.0|4.13.5|patch
wcwidth|0.9.2|0.9.3|patch
s3transfer|0.19.2|0.19.3|patch
tomlkit|0.15.1|0.15.2|patch
xorg-libxi|1.8.3|1.8.4|patch
xorg-libxtst|1.2.5|1.2.6|patch
joserfc|1.7.5|1.7.7|patch
smart_open|8.0.3|8.0.4|patch
distlib|0.4.3|0.4.4|patch
python-discovery|1.6.2|1.6.4|patch
markdown|3.11.1|3.11.2|patch
python-fasthtml|0.14.13|0.14.14|patch
smart-open|8.0.3|8.0.4|patch
cachetools|7.2.2|7.2.4|patch
pydantic-settings|2.16.0|2.16.1|patch
jupyterlab-chat|0.25.2|0.25.3|patch
langsmith|0.14.9|0.14.12|patch
panel-material-ui|0.16.3|0.16.5|patch
pyspnego|0.12.2|0.12.4|patch
libsystemd0|262|262.1|
libudev1|262|262.1|

### Removed

Package | Last Version
---|---
google-api-core-grpc|2.29.0
