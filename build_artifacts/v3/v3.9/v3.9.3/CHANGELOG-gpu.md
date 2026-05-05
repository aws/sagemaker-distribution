# Change log: 3.9.3 (gpu)

This page lists all package changes since the previous release (3.9.2).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
matplotlib-base|3.10.8|3.10.9|patch
sagemaker-code-editor|1.9.5|1.9.6|patch
sagemaker-gen-ai-jupyterlab-extension|1.0.15|1.0.16|patch
sagemaker-jupyterlab-extension|0.5.4|0.5.7|patch
sagemaker-studio|1.1.13|1.1.14|patch
sagemaker-studio-dataengineering-sessions|1.3.18|1.3.19|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
python-json-logger|2.0.7|3.2.1|major
libexpat|2.7.5|2.8.0|minor
ncurses|6.5|6.6|minor
ca-certificates|2026.2.25|2026.4.22|minor
certifi|2026.2.25|2026.4.22|minor
idna|3.11|3.13|minor
python-tzdata|2026.1|2026.2|minor
libdeflate|1.24|1.25|minor
greenlet|3.4.0|3.5.0|minor
wcwidth|0.6.0|0.7.0|minor
jupyter_server|2.17.0|2.18.0|minor
langsmith|0.7.33|0.8.0|minor
wheel|0.46.3|0.47.0|minor
expat|2.7.5|2.8.0|minor
lcms2|2.18|2.19|minor
google-auth|2.49.2|2.50.0|minor
virtualenv|21.2.4|21.3.0|minor
plum-dispatch|2.8.0|2.9.0|minor
typer|0.24.1|0.25.1|minor
cloudpathlib|0.23.0|0.24.0|minor
pathspec|1.0.4|1.1.1|minor
conda-libmamba-solver|26.3.0|26.4.1|minor
sse-starlette|3.3.4|3.4.1|minor
thrift|0.22.0|0.23.0|minor
llvm-openmp|22.1.3|22.1.4|patch
nccl|2.30.3.1|2.30.4.1|patch
mako|1.3.11|1.3.12|patch
parso|0.8.6|0.8.7|patch
jupyter_events|0.12.0|0.12.1|patch
mistune|3.2.0|3.2.1|patch
click|8.3.2|8.3.3|patch
marshmallow|3.26.1|3.26.2|patch
redshift_connector|2.1.5|2.1.10|patch
fastcore|1.12.40|1.12.44|patch
matplotlib|3.10.8|3.10.9|patch
py-spy|0.4.1|0.4.2|patch
python-multipart|0.0.26|0.0.27|patch
python-fasthtml|0.13.3|0.13.4|patch
numba|0.65.0|0.65.1|patch
libsolv|0.7.36|0.7.37|patch
gitpython|3.1.46|3.1.49|patch
pymysql|1.1.2|1.1.3|patch

### New

Package | Version
---|---
opensearch-py|2.5.0
