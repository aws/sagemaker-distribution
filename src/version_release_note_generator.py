from semver import Version

from utils import get_semver


def generate_new_version_release_note(args):
    image_version: Version = get_semver(args.target_patch_version)
    image_type = args.image_type

    print(f"### Public ECR Gallery URL")
    print(f"https://gallery.ecr.aws/sagemaker/sagemaker-distribution")
    print(f"### Public ECR Image URL")
    print("```")
    print(f"public.ecr.aws/sagemaker/sagemaker-distribution:{image_version}-{image_type}")
    print("```")

    print("## Change Logs")
    print(
        f"Change log: https://github.com/aws/sagemaker-distribution/blob/main/build_artifacts/v{image_version.major}/v{image_version.major}.{image_version.minor}/v{image_version.major}.{image_version.minor}.{image_version.patch}/CHANGELOG-{image_type}.md"
    )
    print(
        f"Release note: https://github.com/aws/sagemaker-distribution/blob/main/build_artifacts/v{image_version.major}/v{image_version.major}.{image_version.minor}/v{image_version.major}.{image_version.minor}.{image_version.patch}/RELEASE.md"
    )
