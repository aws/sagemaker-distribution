# Change log: 4.2.3 (gpu)

This page lists all package changes since the previous release (4.2.2).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
sagemaker-jupyterlab-extension-common|0.4.5|0.4.6|patch
jupyter-ai|3.0.0|3.0.1|patch
uv|0.11.24|0.11.26|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
smart_open|7.6.1|8.0.0|major
smart-open|7.6.1|8.0.0|major
narwhals|2.22.1|2.23.0|minor
regex|2026.5.9|2026.6.28|minor
fastprogress|1.1.6|1.0.3|minor
conda-libmamba-solver|26.4.2|26.6.0|minor
cyclopts|4.19.0|4.20.0|minor
sagemaker-core|2.14.0|2.15.0|minor
trino-python-client|0.337.0|0.338.0|minor
slack-sdk|3.42.0|3.43.0|minor
slack-bolt|1.28.0|1.29.0|minor
libsqlite|3.53.2|3.53.3|patch
greenlet|3.5.2|3.5.3|patch
wcwidth|0.8.1|0.8.2|patch
scramp|1.4.9|1.4.10|patch
joserfc|1.7.1|1.7.2|patch
fastcore|1.13.7|1.13.9|patch
langsmith|0.9.2|0.9.5|patch
tzlocal|5.4.3|5.4.4|patch

### Removed

Package | Last Version
---|---
apsw|3.53.2.0
apswutils|0.1.2
fastlite|0.2.3
oauthlib|3.3.1
python-fasthtml|0.12.50
