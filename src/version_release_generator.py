
from image_version import ImageVersion
from utils import get_semver


def generate_new_version_release(args):
    target_version = str(get_semver(args.target_patch_version))
    image_type = args.image_type
    image_version = ImageVersion(target_version, image_type)

    print(f"### Public ECR Gallery URL")
    print(f"https://gallery.ecr.aws/sagemaker/sagemaker-distribution")
    print(f"### Public ECR Image URL")
    print("```")
    print(f"public.ecr.aws/sagemaker/sagemaker-distribution:{image_version.full_version_with_type()}")
    print("```")

    print("## Change Logs")
    print(
        f"Change log: https://github.com/aws/sagemaker-distribution/blob/main/build_artifacts/v{image_version.major_version}/v{image_version.major_minor()}/v{image_version.full_version()}/CHANGELOG-{image_type}.md"
    )
    print(
        f"Release note: https://github.com/aws/sagemaker-distribution/blob/main/build_artifacts/v{image_version.major_version}/v{image_version.major_minor()}/v{image_version.full_version()}/RELEASE.md"
    )
