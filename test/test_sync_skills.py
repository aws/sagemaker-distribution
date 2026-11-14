from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[1]
SYNC_SCRIPTS = tuple(
    ROOT / "template" / "v5" / minor / "dirs" / "etc" / "sagemaker" / "skills" / "sync_skills.sh"
    for minor in ("v5.0", "v5.1")
)
SKILL_NAME = "aws-ai-ml"
MARKER_NAME = ".aws-skill-metadata"


@pytest.fixture(params=SYNC_SCRIPTS, ids=("v5.0", "v5.1"))
def sync_script(request: pytest.FixtureRequest) -> Path:
    return request.param


def _write_image_skill(image_root: Path, version: str | None = "5") -> Path:
    skill = image_root / SKILL_NAME
    skill.mkdir(parents=True)
    metadata = f'\nmetadata:\n  version: "{version}"' if version is not None else ""
    (skill / "SKILL.md").write_text(
        f"---\nname: {SKILL_NAME}\ndescription: Test SageMaker Skill.{metadata}\n---\n\n# Test\n",
        encoding="utf-8",
    )
    (skill / "reference.md").write_text("image content\n", encoding="utf-8")
    return skill


def _run_sync(home: Path, image_root: Path, sync_script: Path) -> subprocess.CompletedProcess[str]:
    home.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment["HOME"] = str(home)
    return subprocess.run(
        ["bash", str(sync_script), str(image_root)],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )


def _managed_skill(home: Path) -> Path:
    return home / ".agent" / "skills" / SKILL_NAME


def _marker_version(home: Path) -> str:
    marker = _managed_skill(home) / MARKER_NAME
    return json.loads(marker.read_text(encoding="utf-8"))["version"]


def test_fresh_install_adds_cli_metadata_and_agent_links(tmp_path, sync_script):
    image = tmp_path / "image"
    home = tmp_path / "home"
    _write_image_skill(image)

    result = _run_sync(home, image, sync_script)

    assert result.returncode == 0, result.stderr
    assert _marker_version(home) == "v5"
    assert json.loads((home / ".agent" / "skills" / ".sagemaker-lock").read_text())["source"] == (
        "agent-toolkit-for-aws"
    )
    for agent_directory in (home / ".kiro" / "skills", home / ".claude" / "skills"):
        link = agent_directory / SKILL_NAME
        assert link.is_symlink()
        assert link.resolve() == _managed_skill(home).resolve()


def test_clean_copy_missing_marker_is_migrated(tmp_path, sync_script):
    image = tmp_path / "image"
    home = tmp_path / "home"
    _write_image_skill(image)
    assert _run_sync(home, image, sync_script).returncode == 0
    (_managed_skill(home) / MARKER_NAME).unlink()

    result = _run_sync(home, image, sync_script)

    assert result.returncode == 0, result.stderr
    assert _marker_version(home) == "v5"
    assert "Enabled Agent Toolkit updates" in result.stdout


def test_existing_marker_is_excluded_from_checksum_and_preserved(tmp_path, sync_script):
    image = tmp_path / "image"
    home = tmp_path / "home"
    _write_image_skill(image)
    assert _run_sync(home, image, sync_script).returncode == 0
    marker = _managed_skill(home) / MARKER_NAME
    marker.write_text('{"version":"v7"}\n', encoding="utf-8")

    result = _run_sync(home, image, sync_script)

    assert result.returncode == 0, result.stderr
    assert _marker_version(home) == "v7"
    assert "already current" in result.stdout
    assert "user modified" not in result.stdout


def test_modified_copy_is_preserved_without_migration(tmp_path, sync_script):
    image = tmp_path / "image"
    home = tmp_path / "home"
    _write_image_skill(image)
    assert _run_sync(home, image, sync_script).returncode == 0
    marker = _managed_skill(home) / MARKER_NAME
    marker.unlink()
    customer_file = _managed_skill(home) / "customer-change.md"
    customer_file.write_text("keep me\n", encoding="utf-8")

    result = _run_sync(home, image, sync_script)

    assert result.returncode == 0, result.stderr
    assert customer_file.read_text(encoding="utf-8") == "keep me\n"
    assert not marker.exists()
    assert "user modified" in result.stdout


def test_cli_updated_copy_is_not_downgraded(tmp_path, sync_script):
    image = tmp_path / "image"
    home = tmp_path / "home"
    _write_image_skill(image)
    assert _run_sync(home, image, sync_script).returncode == 0
    active = _managed_skill(home)
    (active / "reference.md").write_text("catalog v6 content\n", encoding="utf-8")
    (active / MARKER_NAME).write_text('{"version":"v6"}\n', encoding="utf-8")

    result = _run_sync(home, image, sync_script)

    assert result.returncode == 0, result.stderr
    assert (active / "reference.md").read_text(encoding="utf-8") == "catalog v6 content\n"
    assert _marker_version(home) == "v6"
    assert "user modified" in result.stdout


@pytest.mark.parametrize("version", [None, "v5", "5.1", "five"])
def test_invalid_image_version_does_not_create_marker(tmp_path, sync_script, version):
    image = tmp_path / "image"
    home = tmp_path / "home"
    _write_image_skill(image, version)

    result = _run_sync(home, image, sync_script)

    assert result.returncode == 0
    assert not (_managed_skill(home) / MARKER_NAME).exists()
    assert "valid numeric metadata.version not found" in result.stderr


def test_other_skill_is_not_given_agent_toolkit_metadata(tmp_path, sync_script):
    image = tmp_path / "image"
    home = tmp_path / "home"
    other = image / "other-skill"
    other.mkdir(parents=True)
    (other / "SKILL.md").write_text(
        '---\nname: other-skill\ndescription: Another test Skill.\nmetadata:\n  version: "2"\n---\n',
        encoding="utf-8",
    )

    result = _run_sync(home, image, sync_script)

    assert result.returncode == 0, result.stderr
    assert not (home / ".agent" / "skills" / "other-skill" / MARKER_NAME).exists()
