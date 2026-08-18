# Change log: 4.1.9 (gpu)

This page lists all package changes since the previous release (4.1.8).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
sagemaker-jupyterlab-extension-common|0.4.7|0.4.8|patch
sagemaker-studio|1.1.29|1.1.30|patch
sagemaker-studio-dataengineering-extensions|1.3.13|1.3.14|patch
sagemaker-studio-dataengineering-sessions|1.3.23|1.3.24|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
harfbuzz|12.2.0|11.0.0|major
graphviz|13.1.2|12.2.1|major
libffi|3.5.2|3.7.0|minor
charset-normalizer|3.4.9|3.5.1|minor
libsystemd0|261.1|261.2|minor
libudev1|261.1|261.2|minor
pcre2|10.46|10.44|minor
libglib|2.86.2|2.84.0|minor
gdk-pixbuf|2.44.4|2.42.12|minor
python-json-logger|4.1.0|4.2.0|minor
dbus|1.16.2|1.13.6|minor
wheel|0.47.0|0.48.0|minor
glib-tools|2.86.2|2.84.0|minor
orjson|3.11.9|3.12.0|minor
backports.zstd|1.6.0|1.7.0|minor
databricks-sdk|0.125.0|0.130.0|minor
uncalled-for|0.3.2|0.4.0|minor
langsmith|0.10.17|0.11.0|minor
sqlglot|30.15.0|30.17.0|minor
filelock|3.32.2|3.32.3|patch
fontconfig|2.18.2|2.18.3|patch
pango|1.56.4|1.56.3|patch
typing-inspection|0.4.3|0.4.4|patch
greenlet|3.5.4|3.5.5|patch
sqlalchemy|2.0.51|2.0.52|patch
platformdirs|4.11.1|4.11.3|patch
python-fastjsonschema|2.22.1|2.22.2|patch
pandoc|3.10.1|3.10.2|patch
libdrm|2.4.127|2.4.129|patch
qt6-main|6.9.2|6.9.0|patch
pyside6|6.9.2|6.9.0|patch
python-discovery|1.5.1|1.5.2|patch
virtualenv|21.7.3|21.7.4|patch
omegaconf|2.3.0|2.3.1|patch
fastcore|2.2.10|2.2.12|patch
fastmcp-slim|3.4.6|3.4.7|patch
fastmcp|3.4.6|3.4.7|patch
gitpython|3.1.58|3.1.59|patch
poppler|25.12.0|25.02.0|

### New

Package | Version
---|---
expat|2.8.1
libllvm20|20.1.8
libclang-cpp20.1|20.1.8
mysql-common|9.0.1
mysql-libs|9.0.1

### Removed

Package | Last Version
---|---
libclang-cpp21.1|21.1.0
