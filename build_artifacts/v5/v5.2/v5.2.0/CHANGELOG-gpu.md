# Change log: 5.2.0 (gpu)

This page lists all package changes since the previous release (5.1.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
langchain-aws|1.9.3|1.10.0|minor
langchain-openai|1.8.3|1.8.5|patch
sagemaker-code-editor|1.10.3|1.10.5|patch

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
rdma-core|65.0|66.0|major
smart_open|9.0.6|10.0.0|major
python-xxhash|3.7.0|4.1.0|major
smart-open|9.0.6|10.0.0|major
nodejs|20.19.6|22.23.5|major
ca-certificates|2026.10.23|2026.11.20|minor
certifi|2026.10.23|2026.11.20|minor
tbb|2023.1.0|2023.2.0|minor
argon2-cffi-bindings|26.1.0|26.2.0|minor
google-auth|2.62.2|2.63.1|minor
databricks-sdk|0.169.0|0.170.0|minor
langsmith|0.15.0|0.16.0|minor
slack-sdk|3.47.0|3.48.0|minor
yaml|0.2.5|0.2.6|patch
charset-normalizer|3.5.2|3.5.3|patch
platformdirs|4.14.7|4.14.8|patch
soupsieve|4.1.2|4.1.3|patch
decorator|5.3.1|5.3.2|patch
exceptiongroup|1.3.1|1.3.2|patch
wcwidth|0.9.4|0.9.5|patch
authlib|1.9.9|1.9.10|patch
cloudpickle|3.1.2|3.1.3|patch
virtualenv|21.15.9|21.15.12|patch
fastcore|2.2.45|2.2.46|patch
python-fasthtml|0.14.26|0.14.30|patch
coverage|7.17.3|7.17.5|patch
sse-starlette|3.7.0|3.7.1|patch
langchain-core|1.8.3|1.8.4|patch
ormsgpack|1.13.0|1.13.1|patch
langgraph|1.2.23|1.2.24|patch

### New

Package | Version
---|---
tcm|1.6.0
