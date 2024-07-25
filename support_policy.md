# Framework Support Policy
Amazon SageMaker Distribution is a set of Docker images that include popular frameworks for machine learning, data science, and visualization. This page details the framework support policy for SageMaker Distribution Images.

## Support Policy
The table below outlines the release schedule for SageMaker Distribution Image versions and their planned support timelines. AWS provides ongoing functionality and security updates for supported image versions. In some cases, an image version may need to be designated end of support earlier than originally planned if (a) security issues cannot be addressed while maintaining semantic versioning guidelines or (b) any of our major dependencies, like Python, reach end-of-life. AWS can release ad-hoc major or minor versions on an as-needed basis.

| Version | Description | Release Cadence |
| :---:   | :---:       | :---:           |
| Major   | Amazon SageMaker Distribution's major version releases involve upgrading all of its core dependencies to the latest compatible versions. These major releases may also add or remove packages as part of the update. Major versions are denoted by the first number in the version string, such as 1.0, 2.0, or 3.0. | 6 months |
| Minor   | Amazon SageMaker Distribution's minor version releases include upgrading all of its core dependencies to the latest compatible minor versions within the same major version. SageMaker Distribution can add new packages during a minor version release. Minor versions are denoted by the second number in the version string, for example, 1.1, 1.2, or 2.1. | 1 month |
| Patch   | Amazon SageMaker Distribution's patch version releases include updating all of its core dependencies to the latest compatible patch versions within the same minor version. SageMaker Distribution does not add or remove any packages during a patch version release. Patch versions are denoted by the third number in the version string, for example, 1.1.1, 1.2.1, or 2.1.3. | As neccessary for fixing security vulnerabilities |

## Vulnerability scanning
AWS leverages [Amazon Elastic Container Registry (ECR) enhanced scanning](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning-enhanced.html) to automatically detect vulnerabilities in SageMaker Distribution Images. AWS continuously runs ECR enhanced scanning on all supported image versions. When vulnerabilities are detected and a fix is available that satisfies the Semantic Versioning (SEMVER) constraints, AWS will release an update to remediate the issue.

## Supported Image Versions
The tables below lists the supported SageMaker Distribution image versions and their planned end of support dates. When you are building images or pulling images from the ECR repository, we recommend you choose supported image versions from the tables below.

### CPU Images

| Image Version | ECR Image URI | Planned End of Support Date |
| :---:         | :---:         | :---:                       |
| 1.9.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.9-cpu  | Jan 15th, 2025 |
| 1.8.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.8-cpu  | Dec 31st, 2024 |
| 1.7.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.7-cpu  | Dec 15th, 2024 |
| 1.6.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.6-cpu  | Dec 15th, 2024 |
| 1.5.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.5-cpu  | Oct 31st 2024  |
| 1.4.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.4-cpu  | Oct 31st 2024  |
| 0.12.x        | public.ecr.aws/sagemaker/sagemaker-distribution:0.12-cpu | Sept 1st, 2024 |

### GPU Images

| Image Version | ECR Image URI | Planned End of Support Date |
| :---:         | :---:         | :---:                       |
| 1.9.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.9-gpu  | Jan 15th, 2025 |
| 1.8.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.8-gpu  | Dec 31st, 2024 |
| 1.7.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.7-gpu  | Dec 15th, 2024 |
| 1.6.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.6-gpu  | Dec 15th, 2024 |
| 1.5.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.5-gpu  | Oct 31st 2024  |
| 1.4.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.4-gpu  | Oct 31st 2024  |
| 0.12.x        | public.ecr.aws/sagemaker/sagemaker-distribution:0.12-gpu | Sept 1st, 2024 |

## Unsupported Image Versions
The tables below list SageMaker Distribution Image versions that are no longer supportedand the dates when they reached end of support. AWS will not release any new functionality or security patch updates for these image versions. These unsupported versions will remain visible in the below table for 1 year after their end of support date.

### CPU Images

| Image Version | ECR Image URI | End of Support Date |
| :---:         | :---:         | :---:               |
| 1.3.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.3-cpu  | June 28th, 2024  |
| 1.2.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.2-cpu  | June 28th, 2024  |
| 1.1.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.1-cpu  | May 2nd, 2024    |
| 1.0.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.0-cpu  | April 23rd, 2024 |
| 0.11.x        | public.ecr.aws/sagemaker/sagemaker-distribution:0.11-cpu | July 3rd, 2024   |
| 0.10.x        | public.ecr.aws/sagemaker/sagemaker-distribution:0.10-cpu | June 6th, 2024   |
| 0.9.x         | public.ecr.aws/sagemaker/sagemaker-distribution:0.9-cpu  | May 3rd, 2024    |
| 0.8.x         | public.ecr.aws/sagemaker/sagemaker-distribution:0.8-cpu  | April 9th, 2024  |
| 0.7.x         | public.ecr.aws/sagemaker/sagemaker-distribution:0.7-cpu  | April 5th, 2024  |

### GPU Images
| Image Version | ECR Image URI | End of Support Date |
| :---:         | :---:         | :---:               |
| 1.3.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.3-gpu  | June 28th, 2024  |
| 1.2.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.2-gpu  | June 28th, 2024  |
| 1.1.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.1-gpu  | May 2nd, 2024    |
| 1.0.x         | public.ecr.aws/sagemaker/sagemaker-distribution:1.0-gpu  | April 23rd, 2024 |
| 0.11.x        | public.ecr.aws/sagemaker/sagemaker-distribution:0.11-gpu | July 3rd, 2024   |
| 0.10.x        | public.ecr.aws/sagemaker/sagemaker-distribution:0.10-gpu | June 6th, 2024   |
| 0.9.x         | public.ecr.aws/sagemaker/sagemaker-distribution:0.9-gpu  | May 3rd, 2024    |
| 0.8.x         | public.ecr.aws/sagemaker/sagemaker-distribution:0.8-gpu  | April 9th, 2024  |
| 0.7.x         | public.ecr.aws/sagemaker/sagemaker-distribution:0.7-gpu  | April 5th, 2024  |

## Frequently Asked Questions

**[Q]** Can I still use older images after an image is no longer supported?

**[A]** Yes, older images remain available in ECR after they reach end of support. However, we highly recommend upgrading to a supported image version that are continuously receiving security updates and bug fixes. It is the customer's responsibility to manage any vulnerabilities that arise due to choosing an image version that is no longer supported by AWS. Do also refer to AWS's [Shared Responsibility Model documentation](https://aws.amazon.com/compliance/shared-responsibility-model/).
