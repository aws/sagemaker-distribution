from __future__ import absolute_import

import unittest.mock as mock

import pytest

pytestmark = pytest.mark.unit

from changelog_generator import _write_dependency_section, generate_change_log
from utils import DependencyChanges, get_semver

_CPU_CONFIG = {
    "build_args": {"ENV_IN_FILENAME": "cpu.env.in"},
    "env_out_filename": "cpu.env.out",
    "image_type": "cpu",
}


# ---------------------------------------------------------------------------
# Rendering tests — use a hand-crafted Changeset, no file I/O for env files
# ---------------------------------------------------------------------------


def _render_section(dep_changes):
    """Render a DependencyChanges to a string via _write_dependency_section."""
    import io

    buf = io.StringIO()
    _write_dependency_section(buf, dep_changes)
    return buf.getvalue()


def test_changed_table():
    section = _render_section(
        DependencyChanges(
            changed={
                "boto3": ["1.26.0", "1.27.0"],  # minor
                "numpy": ["1.24.0", "2.0.0"],  # major
                "requests": ["2.28.0", "2.28.1"],  # patch
            }
        )
    )
    assert "### Changed" in section
    assert "boto3" in section
    assert "1.26.0" in section
    assert "1.27.0" in section
    assert "minor" in section
    assert "major" in section
    assert "patch" in section


def test_added_table():
    section = _render_section(DependencyChanges(added={"boto3": "1.27.0"}))
    assert "### New" in section
    assert "boto3" in section
    assert "1.27.0" in section


def test_removed_table():
    section = _render_section(DependencyChanges(removed={"boto3": "1.26.0"}))
    assert "### Removed" in section
    assert "boto3" in section
    assert "1.26.0" in section


def test_empty_section_writes_nothing():
    assert _render_section(DependencyChanges()) == ""


# ---------------------------------------------------------------------------
# Integration tests — verify file I/O and top-level structure
# ---------------------------------------------------------------------------


def _make_env_in(path, packages):
    path.write_text("\n".join(packages) + "\n")


def _make_env_out(path, urls):
    header = (
        "# This file may be used to create an environment using:\n"
        "# $ conda create --name <env> --file <this file>\n"
        "# platform: linux-64\n"
        "@EXPLICIT\n"
    )
    path.write_text(header + "\n".join(urls) + "\n")


def _conda_url(package, version, build="pyh210e3f2_0", subdir="noarch"):
    return f"https://conda.anaconda.org/conda-forge/{subdir}/{package}-{version}-{build}.conda#abc"


def _run(
    tmp_path,
    source_version,
    target_version,
    source_in,
    source_out,
    target_in,
    target_out,
):
    src_dir = tmp_path / source_version
    tgt_dir = tmp_path / target_version
    src_dir.mkdir()
    tgt_dir.mkdir()

    _make_env_in(src_dir / "cpu.env.in", source_in)
    _make_env_out(src_dir / "cpu.env.out", source_out)
    _make_env_in(tgt_dir / "cpu.env.in", target_in)
    _make_env_out(tgt_dir / "cpu.env.out", target_out)
    (tgt_dir / "source-version.txt").write_text(source_version)

    src_str, tgt_str = str(src_dir), str(tgt_dir)
    with mock.patch(
        "changelog_generator.get_dir_for_version",
        side_effect=lambda v: tgt_str if str(v) == target_version else src_str,
    ):
        generate_change_log(get_semver(target_version), _CPU_CONFIG)

    return (tgt_dir / "CHANGELOG-cpu.md").read_text()


def test_changelog_structure(tmp_path):
    # ipykernel is a direct dep that changes; boto3 is indirect and also changes
    content = _run(
        tmp_path,
        source_version="1.0.0",
        target_version="1.0.1",
        source_in=["conda-forge::ipykernel"],
        source_out=[
            _conda_url("ipykernel", "6.21.3"),
            _conda_url("boto3", "1.26.0", subdir="linux-64"),
        ],
        target_in=["conda-forge::ipykernel"],
        target_out=[
            _conda_url("ipykernel", "6.21.6"),
            _conda_url("boto3", "1.27.0", subdir="linux-64"),
        ],
    )
    assert "# Change log: 1.0.1 (cpu)" in content
    assert "since the previous release (1.0.0)" in content
    assert "## Direct dependencies" in content
    assert "versioning strategy" in content
    assert "## Indirect dependencies" in content
    assert "pulled in automatically" in content


def test_no_sections_when_no_changes(tmp_path):
    content = _run(
        tmp_path,
        source_version="1.0.0",
        target_version="1.0.1",
        source_in=["conda-forge::ipykernel"],
        source_out=[_conda_url("ipykernel", "6.21.3")],
        target_in=["conda-forge::ipykernel"],
        target_out=[_conda_url("ipykernel", "6.21.3")],
    )
    assert "## Direct dependencies" not in content
    assert "## Indirect dependencies" not in content


def test_no_changelog_without_source_version_file(tmp_path, capsys):
    tgt_dir = tmp_path / "1.0.1"
    tgt_dir.mkdir()
    _make_env_in(tgt_dir / "cpu.env.in", ["conda-forge::ipykernel"])
    _make_env_out(tgt_dir / "cpu.env.out", [_conda_url("ipykernel", "6.21.3")])

    with mock.patch("changelog_generator.get_dir_for_version", return_value=str(tgt_dir)):
        generate_change_log(get_semver("1.0.1"), _CPU_CONFIG)

    assert not (tgt_dir / "CHANGELOG-cpu.md").exists()
    assert "WARN" in capsys.readouterr().out
