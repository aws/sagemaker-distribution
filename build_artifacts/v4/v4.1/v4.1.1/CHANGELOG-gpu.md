# Change log: 4.1.1 (gpu)

This page lists all package changes since the previous release (4.1.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
jupyterlab|4.5.6|4.5.7|patch
notebook|7.5.5|7.5.6|patch
sagemaker-code-editor|1.9.5|1.9.6|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
libdeflate|1.24|1.25|minor
cloudpathlib|0.23.0|0.24.0|minor
databricks-sdk|0.105.0|0.106.0|minor
nccl|2.30.3.1|2.30.4.1|patch
typer|0.25.0|0.25.1|patch
gitpython|3.1.48|3.1.49|patch
jupyter-ai-router|0.0.4|0.0.5|patch
langsmith|0.7.37|0.7.38|patch
