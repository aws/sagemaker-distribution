# Change log: 4.1.8 (cpu)

This page lists all package changes since the previous release (4.1.7).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
sagemaker-gen-ai-jupyterlab-extension|1.0.18|1.0.19|patch
sagemaker-studio|1.1.26|1.1.28|patch
uv|0.11.30|0.11.33|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
libgcc|15.2.0|16.1.0|major
libstdcxx|15.2.0|16.1.0|major
libgcc-ng|15.2.0|16.1.0|major
libstdcxx-ng|15.2.0|16.1.0|major
libgfortran5|15.2.0|16.1.0|major
libgfortran|15.2.0|16.1.0|major
websockets|16.1.1|17.0.1|major
sqlglot|28.10.1|30.14.0|major
ca-certificates|2026.6.17|2026.7.22|minor
certifi|2026.6.17|2026.7.22|minor
tqdm|4.69.0|4.70.0|minor
lerc|4.1.0|4.2.0|minor
annotated-types|0.7.0|0.8.0|minor
traitlets|5.15.1|5.16.1|minor
python-fastjsonschema|2.21.2|2.22.1|minor
prometheus_client|0.25.0|0.26.0|minor
h2|4.3.0|4.4.1|minor
boltons|26.0.0|26.1.0|minor
databricks-sdk|0.122.0|0.123.0|minor
sagemaker-core|2.16.0|2.17.0|minor
libsqlite|3.53.3|3.53.4|patch
libxcrypt|4.4.36|4.4.38|patch
filelock|3.32.0|3.32.2|patch
gflags|2.3.0|2.3.1|patch
fontconfig|2.18.1|2.18.2|patch
aiohttp|3.14.2|3.14.3|patch
greenlet|3.5.3|3.5.4|patch
mistune|3.3.3|3.3.4|patch
pandoc|3.10|3.10.1|patch
prompt-toolkit|3.0.52|3.0.53|patch
pyathena|3.35.2|3.35.4|patch
scramp|1.4.12|1.4.15|patch
annotated-doc|0.0.4|0.0.5|patch
google-auth|2.56.0|2.56.2|patch
proto-plus|1.28.1|1.28.2|patch
python-discovery|1.5.0|1.5.1|patch
virtualenv|21.7.0|21.7.1|patch
datasets|5.0.0|5.0.1|patch
markdown|3.10.2|3.10.3|patch
fastcore|2.1.4|2.1.19|patch
python-fasthtml|0.14.9|0.14.11|patch
typer|0.27.0|0.27.1|patch
prompt_toolkit|3.0.52|3.0.53|patch
awswrangler|3.17.0|3.17.1|patch
bokeh|3.9.1|3.9.2|patch
coverage|7.15.2|7.15.3|patch
cyclopts|4.22.0|4.22.5|patch
fastmcp-slim|3.4.4|3.4.5|patch
fastmcp|3.4.4|3.4.5|patch
gitpython|3.1.53|3.1.57|patch
google-cloud-bigquery-core|3.42.2|3.42.3|patch
jupyter-collaboration-ui|2.4.1|2.4.2|patch
jupyter-docprovider|2.4.1|2.4.2|patch
jupyter-ai-router|0.0.5|0.0.6|patch
langsmith|0.10.9|0.10.15|patch
panel-material-ui|0.14.0|0.14.1|patch
sqlalchemy-bigquery|1.17.0|1.17.1|patch

### Removed

Package | Last Version
---|---
apsw|3.53.3.1
apswutils|0.1.2
fastlite|0.2.3
