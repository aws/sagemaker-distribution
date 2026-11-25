# Change log: 5.1.1 (cpu)

This page lists all package changes since the previous release (5.1.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
langchain-openai|1.8.3|1.8.5|patch
sagemaker-code-editor|1.10.3|1.10.5|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
nodejs|20.19.6|22.23.5|major
tbb|2023.1.0|2023.2.0|minor
slack-sdk|3.47.0|3.48.0|minor
platformdirs|4.14.7|4.14.8|patch
soupsieve|4.1.2|4.1.3|patch
exceptiongroup|1.3.1|1.3.2|patch
cloudpickle|3.1.2|3.1.3|patch
coverage|7.17.3|7.17.4|patch
langsmith|0.15.0|0.15.1|patch
langchain-core|1.8.3|1.8.4|patch
langgraph|1.2.23|1.2.24|patch

### New

Package | Version
---|---
tcm|1.6.0
