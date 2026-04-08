# Change log: 4.1.0 (gpu)

This page lists all package changes since the previous release (4.0.0).

## Direct dependencies

> [!NOTE]
> These packages are explicitly included in the image. Their updates follow SageMaker Distribution's [versioning strategy](https://github.com/aws/sagemaker-distribution#versioning-strategy).

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
uvicorn|0.43.0|0.44.0|minor
conda|26.1.1|26.3.1|minor
docker-cli|29.3.1|29.4.0|minor

## Indirect dependencies

> [!NOTE]
> These packages are pulled in automatically to satisfy the requirements of the direct dependencies. Their versions may vary between releases.

### Changed

Package | Previous Version | Current Version | Change Type
---|---|---|---
cryptography|44.0.3|46.0.5|major
pyopenssl|24.3.0|25.3.0|major
conda-libmamba-solver|25.11.0|26.3.0|major
invoke|2.2.1|3.0.3|major
narwhals|2.18.1|2.19.0|minor
regex|2026.3.32|2026.4.4|minor
snowflake-connector-python|3.13.2|3.17.4|minor
dnspython|2.7.0|2.8.0|minor
uvicorn-standard|0.43.0|0.44.0|minor
slack-bolt|1.27.0|1.28.0|minor
openssl|3.6.1|3.6.2|patch
langsmith|0.7.25|0.7.26|patch
python-discovery|1.2.1|1.2.2|patch
python-multipart|0.0.22|0.0.24|patch
python-fasthtml|0.13.2|0.13.3|patch
pydantic-extra-types|2.11.1|2.11.2|patch
smmap|5.0.2|5.0.3|patch
pydynamodb|0.8.1|0.8.2|patch
pytest|9.0.2|9.0.3|patch
