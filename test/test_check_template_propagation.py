import subprocess

import pytest
from check_template_propagation import find_missing_changes, main, parse_template_path

pytestmark = pytest.mark.unit

ALL_FILES = [
    "template/v3/v3.9/Dockerfile",
    "template/v4/v4.5/Dockerfile",
    "template/v4/v4.5/dirs/a.sh",
    "template/v4/v4.6/Dockerfile",
    "template/v4/v4.6/dirs/a.sh",
]


def test_parse_template_path():
    assert parse_template_path("template/v4/v4.6/dirs/etc/x.sh") == (4, 6, "dirs/etc/x.sh")
    assert parse_template_path("template/v4/v3.9/Dockerfile") is None
    assert parse_template_path("template/v4/dirs/etc/x.sh") is None
    assert parse_template_path("build_artifacts/v4/v4.6/v4.6.0/Dockerfile") is None


def test_older_minor_change_must_also_change_the_newest_minor():
    assert find_missing_changes(["template/v4/v4.5/dirs/a.sh"], ALL_FILES) == [
        ("template/v4/v4.5/dirs/a.sh", "template/v4/v4.6/dirs/a.sh")
    ]
    both = ["template/v4/v4.5/dirs/a.sh", "template/v4/v4.6/dirs/a.sh"]
    assert find_missing_changes(both, ALL_FILES) == []


def test_changes_to_the_newest_minor_or_other_files_need_nothing_else():
    assert find_missing_changes(["template/v4/v4.6/dirs/a.sh"], ALL_FILES) == []
    # Each major has its own newest minor: v3.9 is the newest v3 template.
    assert find_missing_changes(["template/v3/v3.9/Dockerfile"], ALL_FILES) == []
    assert find_missing_changes(["template/v4/dirs/a.sh", "src/main.py"], ALL_FILES) == []


def test_main_reads_the_git_trees_and_honours_the_label(tmp_path, monkeypatch, capsys):
    def git(*args):
        command = ["git", "-c", "user.name=test", "-c", "user.email=test@example.com", *args]
        return subprocess.run(command, cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()

    git("init", "-q")
    for minor in (5, 6):
        (tmp_path / f"template/v4/v4.{minor}").mkdir(parents=True)
        (tmp_path / f"template/v4/v4.{minor}/a.sh").write_text("old\n")
    git("add", ".")
    git("commit", "-q", "-m", "base")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("BASE_SHA", git("rev-parse", "HEAD"))

    (tmp_path / "template/v4/v4.5/a.sh").write_text("new\n")
    git("commit", "-q", "-a", "-m", "4.5 only")
    monkeypatch.setenv("HEAD_SHA", git("rev-parse", "HEAD"))
    monkeypatch.setenv("SCOPED", "false")
    assert main() == 1
    assert "template/v4/v4.6/a.sh did not" in capsys.readouterr().out

    monkeypatch.setenv("SCOPED", "true")
    assert main() == 0

    (tmp_path / "template/v4/v4.6/a.sh").write_text("new\n")
    git("commit", "-q", "-a", "-m", "4.6 too")
    monkeypatch.setenv("HEAD_SHA", git("rev-parse", "HEAD"))
    monkeypatch.setenv("SCOPED", "false")
    assert main() == 0
