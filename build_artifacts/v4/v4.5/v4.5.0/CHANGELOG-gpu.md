# Change log: 4.5.0 (gpu)

This page lists all package changes since the previous release (4.4.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
boto3|1.43.46|1.43.56|patch
uvicorn|0.52.1|0.52.3|patch
ipywidgets|8.1.8|8.1.9|patch
aws-smus-cicd-cli|1.0.5|1.0.6|patch
jupyter-ai|3.1.2|3.1.3|patch
sagemaker-studio|1.1.29|1.1.30|patch
sagemaker-studio-dataengineering-extensions|1.3.13|1.3.14|patch
sagemaker-studio-dataengineering-sessions|1.3.23|1.3.24|patch
uv|0.12.3|0.12.5|patch

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
idna|3.18|3.19|minor
libsystemd0|261.1|261.2|minor
libudev1|261.1|261.2|minor
pcre2|10.46|10.44|minor
libglib|2.86.2|2.84.0|minor
gdk-pixbuf|2.44.4|2.42.12|minor
aiobotocore|3.8.0|3.9.0|minor
python-json-logger|4.1.0|4.2.0|minor
pygments|2.20.0|2.21.0|minor
dbus|1.16.2|1.13.6|minor
google-api-core|2.29.0|2.33.0|minor
wheel|0.47.0|0.48.0|minor
glib-tools|2.86.2|2.84.0|minor
llvmlite|0.48.0|0.49.0|minor
numba|0.66.0|0.67.0|minor
orjson|3.11.9|3.12.0|minor
backports.zstd|1.6.0|1.7.0|minor
cyclopts|4.22.5|4.23.0|minor
databricks-sdk|0.125.0|0.132.0|minor
deltalake|1.5.0|1.6.2|minor
griffelib|2.1.0|2.2.0|minor
google-cloud-bigquery-core|3.43.0|3.18.0|minor
gunicorn|26.0.0|26.1.0|minor
langsmith|0.10.17|0.11.0|minor
tiktoken|0.13.0|0.14.0|minor
sagemaker-core|2.18.0|2.20.0|minor
sqlalchemy-bigquery|1.17.2|1.16.0|minor
sqlglot|30.15.0|30.17.0|minor
filelock|3.32.2|3.32.3|patch
gmpy2|2.3.0|2.3.1|patch
pango|1.56.4|1.56.3|patch
typing-inspection|0.4.3|0.4.4|patch
botocore|1.43.46|1.43.56|patch
sqlalchemy|2.0.51|2.0.52|patch
platformdirs|4.11.2|4.11.3|patch
python-fastjsonschema|2.22.1|2.22.2|patch
pandoc|3.10.1|3.10.2|patch
libdrm|2.4.127|2.4.129|patch
qt6-main|6.9.2|6.9.0|patch
pyside6|6.9.2|6.9.0|patch
python-discovery|1.5.1|1.5.2|patch
virtualenv|21.7.3|21.7.4|patch
fastcore|2.2.10|2.2.12|patch
jupyterlab_widgets|3.0.16|3.0.17|patch
widgetsnbextension|4.0.15|4.0.16|patch
unearth|0.18.2|0.18.3|patch
python-dotenv|1.2.2|1.2.3|patch
uvicorn-standard|0.52.1|0.52.3|patch
fastmcp-slim|3.4.6|3.4.7|patch
fastmcp|3.4.6|3.4.7|patch
gitpython|3.1.58|3.1.59|patch
jupyterlab-chat|0.23.1|0.23.2|patch
jupyter-ai-persona-manager|0.1.2|0.1.3|patch
panel-core|1.9.3|1.9.4|patch
panel|1.9.3|1.9.4|patch
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
google-api-core-grpc|2.29.0
