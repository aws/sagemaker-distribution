import unittest
from unittest.mock import patch

from version_release_note_generator import generate_new_version_release_note


class TestVersionReleaseGenerator(unittest.TestCase):
    def test_generate_new_version_release_v0(self):
        args = lambda: None
        args.target_patch_version = "0.13.0"
        args.image_type = "cpu"

        # Act
        with patch("builtins.print") as mock_print:
            generate_new_version_release_note(args)

        # Assert
        expected_output = [
            "### Public ECR Gallery URL",
            "https://gallery.ecr.aws/sagemaker/sagemaker-distribution",
            "### Public ECR Image URL",
            "```",
            "public.ecr.aws/sagemaker/sagemaker-distribution:0.13.0-cpu",
            "```",
            "## Change Logs",
            "Change log: https://github.com/aws/sagemaker-distribution/blob/main/build_artifacts/v0/v0.13/v0.13.0/CHANGELOG-cpu.md",
            "Release note: https://github.com/aws/sagemaker-distribution/blob/main/build_artifacts/v0/v0.13/v0.13.0/RELEASE.md",
        ]
        mock_print.assert_has_calls([unittest.mock.call(line) for line in expected_output])

    def test_generate_new_version_release_v1(self):
        args = lambda: None
        args.target_patch_version = "1.2.3"
        args.image_type = "cpu"

        # Act
        with patch("builtins.print") as mock_print:
            generate_new_version_release_note(args)

        # Assert
        expected_output = [
            "### Public ECR Gallery URL",
            "https://gallery.ecr.aws/sagemaker/sagemaker-distribution",
            "### Public ECR Image URL",
            "```",
            "public.ecr.aws/sagemaker/sagemaker-distribution:1.2.3-cpu",
            "```",
            "## Change Logs",
            "Change log: https://github.com/aws/sagemaker-distribution/blob/main/build_artifacts/v1/v1.2/v1.2.3/CHANGELOG-cpu.md",
            "Release note: https://github.com/aws/sagemaker-distribution/blob/main/build_artifacts/v1/v1.2/v1.2.3/RELEASE.md",
        ]
        mock_print.assert_has_calls([unittest.mock.call(line) for line in expected_output])

    def test_generate_new_version_release_v2(self):
        args = lambda: None
        args.target_patch_version = "2.0.0"
        args.image_type = "gpu"

        # Act
        with patch("builtins.print") as mock_print:
            generate_new_version_release_note(args)

        # Assert
        expected_output = [
            "### Public ECR Gallery URL",
            "https://gallery.ecr.aws/sagemaker/sagemaker-distribution",
            "### Public ECR Image URL",
            "```",
            "public.ecr.aws/sagemaker/sagemaker-distribution:2.0.0-gpu",
            "```",
            "## Change Logs",
            "Change log: https://github.com/aws/sagemaker-distribution/blob/main/build_artifacts/v2/v2.0/v2.0.0/CHANGELOG-gpu.md",
            "Release note: https://github.com/aws/sagemaker-distribution/blob/main/build_artifacts/v2/v2.0/v2.0.0/RELEASE.md",
        ]
        mock_print.assert_has_calls([unittest.mock.call(line) for line in expected_output])
