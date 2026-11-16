from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[1]
CLONE_SCRIPTS = tuple(
    ROOT / "template" / "v5" / minor / "dirs" / "etc" / "sagemaker" / "skills" / "clone_skills.sh"
    for minor in ("v5.0", "v5.1")
)
SKILL_NAME = "aws-ai-ml"
MARKER_NAME = ".aws-skill-metadata"


@pytest.fixture(params=CLONE_SCRIPTS, ids=("v5.0", "v5.1"))
def clone_script(request: pytest.FixtureRequest) -> Path:
    return request.param


def _create_skill_repo(tmp_path: Path, skill_name: str, version: str | None) -> tuple[Path, str]:
    repo = tmp_path / "repo"
    skill_path = Path("plugins") / "aws-core" / "skills" / skill_name
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
    return repo, skill_path.as_posix()


def _run_clone(
    tmp_path: Path,
    clone_script: Path,
    skill_name: str = SKILL_NAME,
    version: str | None = "5",
) -> tuple[subprocess.CompletedProcess[str], Path]:
    repo, skill_path = _create_skill_repo(tmp_path, skill_name, version)
    manifest = tmp_path / "skills-manifest.json"
    manifest.write_text(
        json.dumps([{"repo": f"file://{repo}", "path": skill_path}]),
        encoding="utf-8",
    )
    destination = tmp_path / "image-skills"
    destination.mkdir()
    result = subprocess.run(
        ["bash", str(clone_script), str(manifest), str(destination)],
        check=False,
        capture_output=True,
        text=True,
    )
    return result, destination


def test_build_adds_agent_toolkit_metadata(tmp_path, clone_script):
    result, destination = _run_clone(tmp_path, clone_script)

    assert result.returncode == 0, result.stderr
    marker = destination / SKILL_NAME / MARKER_NAME
    assert json.loads(marker.read_text(encoding="utf-8")) == {"version": "v5"}


@pytest.mark.parametrize("version", [None, "v5", "5.1", "five"])
def test_build_fails_for_invalid_aws_ai_ml_version(tmp_path, clone_script, version):
    result, destination = _run_clone(tmp_path, clone_script, version=version)

    assert result.returncode != 0
    assert "valid numeric metadata.version not found" in result.stderr
    assert not (destination / SKILL_NAME / MARKER_NAME).exists()


def test_build_does_not_add_metadata_to_other_skills(tmp_path, clone_script):
    result, destination = _run_clone(tmp_path, clone_script, skill_name="other-skill", version="2")

    assert result.returncode == 0, result.stderr
    assert not (destination / "other-skill" / MARKER_NAME).exists()


def test_v5_clone_scripts_remain_identical():
    contents = [path.read_text(encoding="utf-8") for path in CLONE_SCRIPTS]

    assert contents[0] == contents[1]
