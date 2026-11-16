from __future__ import annotations

import json
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
COLLECTION_SOURCE_VERSIONS = {"v4.1", "v4.2", "v4.3", "v4.4"}
SKILL_NAME = "aws-ai-ml"
MARKER_NAME = ".aws-skill-metadata"


class CloneScriptCase(NamedTuple):
    version: str
    path: Path
    copies_collection: bool


CLONE_SCRIPT_CASES = tuple(
    CloneScriptCase(
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
            / "clone_skills.sh"
        ),
        copies_collection=version in COLLECTION_SOURCE_VERSIONS,
    )
    for version in TEMPLATE_VERSIONS
)


@pytest.fixture(params=CLONE_SCRIPT_CASES, ids=TEMPLATE_VERSIONS)
def clone_script_case(request: pytest.FixtureRequest) -> CloneScriptCase:
    return request.param


def _create_skill_repo(
    tmp_path: Path,
    skill_name: str,
    version: str | None,
    copies_collection: bool,
) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    skills_path = Path("plugins") / "test-plugin" / "skills"
    skill_path = skills_path / skill_name
    skill = repo / skill_path
    skill.mkdir(parents=True)
    metadata = f'\nmetadata:\n  version: "{version}"' if version is not None else ""
    (skill / "SKILL.md").write_text(
        f"---\nname: {skill_name}\ndescription: Test Skill.{metadata}\n---\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "-c",
            "user.name=SMD Test",
            "-c",
            "user.email=smd-test@example.com",
            "commit",
            "-q",
            "-m",
            "test skill",
        ],
        check=True,
    )
    source_path = skills_path if copies_collection else skill_path
    return repo, source_path.as_posix()


def _run_clone(
    tmp_path: Path,
    clone_script_case: CloneScriptCase,
    skill_name: str = SKILL_NAME,
    version: str | None = "5",
) -> tuple[subprocess.CompletedProcess[str], Path]:
    repo, source_path = _create_skill_repo(
        tmp_path,
        skill_name,
        version,
        clone_script_case.copies_collection,
    )
    manifest = tmp_path / "skills-manifest.json"
    manifest.write_text(
        json.dumps([{"repo": f"file://{repo}", "path": source_path}]),
        encoding="utf-8",
    )
    destination = tmp_path / "image-skills"
    destination.mkdir()
    result = subprocess.run(
        ["bash", str(clone_script_case.path), str(manifest), str(destination)],
        check=False,
        capture_output=True,
        text=True,
    )
    return result, destination


def test_build_adds_agent_toolkit_metadata(tmp_path, clone_script_case):
    result, destination = _run_clone(tmp_path, clone_script_case)

    assert result.returncode == 0, result.stderr
    marker = destination / SKILL_NAME / MARKER_NAME
    assert json.loads(marker.read_text(encoding="utf-8")) == {"version": "v5"}


@pytest.mark.parametrize("version", [None, "v5", "5.1", "five"])
def test_build_fails_for_invalid_aws_ai_ml_version(tmp_path, clone_script_case, version):
    result, destination = _run_clone(tmp_path, clone_script_case, version=version)

    assert result.returncode != 0
    assert "valid numeric metadata.version not found" in result.stderr
    assert not (destination / SKILL_NAME / MARKER_NAME).exists()


def test_build_does_not_add_metadata_to_other_skills(tmp_path, clone_script_case):
    result, destination = _run_clone(tmp_path, clone_script_case, skill_name="other-skill", version="2")

    assert result.returncode == 0, result.stderr
    assert not (destination / "other-skill" / MARKER_NAME).exists()


def test_clone_scripts_remain_identical_by_source_layout():
    for copies_collection in (True, False):
        contents = {
            case.path.read_text(encoding="utf-8")
            for case in CLONE_SCRIPT_CASES
            if case.copies_collection is copies_collection
        }
        assert len(contents) == 1
