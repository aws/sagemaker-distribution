from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import NamedTuple

import pytest

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_VERSIONS = (
    "v4.1",
    "v4.2",
    "v4.3",
    "v4.4",
    "v4.5",
    "v4.6",
    "v4.7",
    "v4.8",
    "v5.0",
    "v5.1",
)
UNIFIED_MIGRATION_VERSIONS = {"v4.5", "v4.6", "v4.7", "v4.8", "v5.0", "v5.1"}
SKILL_NAME = "aws-ai-ml"
MARKER_NAME = ".aws-skill-metadata"


class SyncScriptCase(NamedTuple):
    version: str
    path: Path
    has_unified_migration: bool


SYNC_SCRIPT_CASES = tuple(
    SyncScriptCase(
        version=version,
        path=(
            ROOT
            / "template"
            / version.split(".")[0]
            / version
            / "dirs"
            / "etc"
            / "sagemaker"
            / "skills"
            / "sync_skills.sh"
        ),
        has_unified_migration=version in UNIFIED_MIGRATION_VERSIONS,
    )
    for version in TEMPLATE_VERSIONS
)


@pytest.fixture(params=SYNC_SCRIPT_CASES, ids=TEMPLATE_VERSIONS)
def sync_script_case(request: pytest.FixtureRequest) -> SyncScriptCase:
    return request.param


def _write_image_skill(image_root: Path, marker_version: str | None = "v5") -> Path:
    skill = image_root / SKILL_NAME
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f'---\nname: {SKILL_NAME}\ndescription: Test SageMaker Skill.\nmetadata:\n  version: "5"\n---\n\n# Test\n',
        encoding="utf-8",
    )
    (skill / "reference.md").write_text("image content\n", encoding="utf-8")
    if marker_version is not None:
        (skill / MARKER_NAME).write_text(
            json.dumps({"version": marker_version}, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
    return skill


def _run_sync(
    home: Path,
    image_root: Path,
    sync_script_case: SyncScriptCase,
) -> subprocess.CompletedProcess[str]:
    home.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment["HOME"] = str(home)
    return subprocess.run(
        ["bash", str(sync_script_case.path), str(image_root)],
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


def test_fresh_install_copies_cli_metadata_and_agent_links(tmp_path, sync_script_case):
    image = tmp_path / "image"
    home = tmp_path / "home"
    _write_image_skill(image)

    result = _run_sync(home, image, sync_script_case)

    assert result.returncode == 0, result.stderr
    assert _marker_version(home) == "v5"
    lock = json.loads((home / ".agent" / "skills" / ".sagemaker-lock").read_text())
    if sync_script_case.has_unified_migration:
        assert lock["source"] == "agent-toolkit-for-aws"
    else:
        assert "source" not in lock
    for agent_directory in (home / ".kiro" / "skills", home / ".claude" / "skills"):
        link = agent_directory / SKILL_NAME
        assert link.is_symlink()
        assert link.resolve() == _managed_skill(home).resolve()


def test_clean_legacy_copy_missing_marker_is_migrated(tmp_path, sync_script_case):
    legacy_image = tmp_path / "legacy-image"
    current_image = tmp_path / "current-image"
    home = tmp_path / "home"
    _write_image_skill(legacy_image, marker_version=None)
    _write_image_skill(current_image)
    assert _run_sync(home, legacy_image, sync_script_case).returncode == 0
    assert not (_managed_skill(home) / MARKER_NAME).exists()

    result = _run_sync(home, current_image, sync_script_case)

    assert result.returncode == 0, result.stderr
    assert _marker_version(home) == "v5"
    assert "Updated skill 'aws-ai-ml'" in result.stdout


def test_toolkit_metadata_change_is_preserved(tmp_path, sync_script_case):
    image = tmp_path / "image"
    home = tmp_path / "home"
    _write_image_skill(image)
    assert _run_sync(home, image, sync_script_case).returncode == 0
    marker = _managed_skill(home) / MARKER_NAME
    marker.write_text('{"version":"v7"}\n', encoding="utf-8")

    result = _run_sync(home, image, sync_script_case)

    assert result.returncode == 0, result.stderr
    assert _marker_version(home) == "v7"
    assert "user modified" in result.stdout


def test_modified_copy_is_preserved_without_migration(tmp_path, sync_script_case):
    image = tmp_path / "image"
    home = tmp_path / "home"
    _write_image_skill(image)
    assert _run_sync(home, image, sync_script_case).returncode == 0
    marker = _managed_skill(home) / MARKER_NAME
    marker.unlink()
    customer_file = _managed_skill(home) / "customer-change.md"
    customer_file.write_text("keep me\n", encoding="utf-8")

    result = _run_sync(home, image, sync_script_case)

    assert result.returncode == 0, result.stderr
    assert customer_file.read_text(encoding="utf-8") == "keep me\n"
    assert not marker.exists()
    assert "user modified" in result.stdout


def test_cli_updated_copy_is_not_downgraded(tmp_path, sync_script_case):
    image = tmp_path / "image"
    home = tmp_path / "home"
    _write_image_skill(image)
    assert _run_sync(home, image, sync_script_case).returncode == 0
    active = _managed_skill(home)
    (active / "reference.md").write_text("catalog v6 content\n", encoding="utf-8")
    (active / MARKER_NAME).write_text('{"version":"v6"}\n', encoding="utf-8")

    result = _run_sync(home, image, sync_script_case)

    assert result.returncode == 0, result.stderr
    assert (active / "reference.md").read_text(encoding="utf-8") == "catalog v6 content\n"
    assert _marker_version(home) == "v6"
    assert "user modified" in result.stdout


def test_sync_does_not_invent_metadata_for_other_skills(tmp_path, sync_script_case):
    image = tmp_path / "image"
    home = tmp_path / "home"
    other = image / "other-skill"
    other.mkdir(parents=True)
    (other / "SKILL.md").write_text(
        '---\nname: other-skill\ndescription: Another test Skill.\nmetadata:\n  version: "2"\n---\n',
        encoding="utf-8",
    )

    result = _run_sync(home, image, sync_script_case)

    assert result.returncode == 0, result.stderr
    assert not (home / ".agent" / "skills" / "other-skill" / MARKER_NAME).exists()


def test_sync_scripts_remain_identical_by_migration_generation():
    for has_unified_migration in (True, False):
        contents = {
            case.path.read_text(encoding="utf-8")
            for case in SYNC_SCRIPT_CASES
            if case.has_unified_migration is has_unified_migration
        }
        assert len(contents) == 1
