import subprocess

import pytest

pytestmark = pytest.mark.unit

from template_tools import (
    find_copy_problems,
    find_legacy_path_problems,
    find_problems,
    find_propagation_problems,
    parse_minor_template_path,
    run_check,
)

HEAD_PATHS = {
    "template/v3/v3.9/Dockerfile",
    "template/v4/v4.5/Dockerfile",
    "template/v4/v4.5/dirs/a.sh",
    "template/v4/v4.6/Dockerfile",
    "template/v4/v4.6/dirs/a.sh",
}


def _tree(files):
    """path -> blob id  =>  path -> (mode, blob id), as git ls-tree reports it."""
    return {path: ("100644", blob) for path, blob in files.items()}


def test_parse_minor_template_path():
    assert parse_minor_template_path("template/v4/v4.6/dirs/etc/x.sh") == (4, 6, "dirs/etc/x.sh")
    assert parse_minor_template_path("template/v4/v3.9/Dockerfile") is None
    assert parse_minor_template_path("template/v4/dirs/etc/x.sh") is None
    assert parse_minor_template_path("build_artifacts/v4/v4.6/v4.6.0/Dockerfile") is None


def test_older_minor_change_must_reach_newest_minor():
    assert find_propagation_problems(["template/v4/v4.5/dirs/a.sh"], HEAD_PATHS, scoped=False) == [
        "template/v4/v4.5/dirs/a.sh changed, but template/v4/v4.6/dirs/a.sh did not."
    ]
    both = ["template/v4/v4.5/dirs/a.sh", "template/v4/v4.6/dirs/a.sh"]
    assert find_propagation_problems(both, HEAD_PATHS, scoped=False) == []


def test_newest_minor_and_other_majors_need_nothing_else():
    assert find_propagation_problems(["template/v4/v4.6/dirs/a.sh"], HEAD_PATHS, scoped=False) == []
    assert find_propagation_problems(["template/v3/v3.9/Dockerfile"], HEAD_PATHS, scoped=False) == []


def test_scoped_backport_is_allowed():
    assert find_propagation_problems(["template/v4/v4.5/dirs/a.sh"], HEAD_PATHS, scoped=True) == []


def test_new_minor_must_match_previous_minor():
    base = {"template/v4/v4.6/Dockerfile", "template/v4/v4.6/dirs/a.sh"}
    same = _tree(
        {
            "template/v4/v4.6/Dockerfile": "d1",
            "template/v4/v4.6/dirs/a.sh": "a1",
            "template/v4/v4.7/Dockerfile": "d1",
            "template/v4/v4.7/dirs/a.sh": "a1",
        }
    )
    assert find_copy_problems(base, same, declared=set()) == []

    stale = dict(same, **_tree({"template/v4/v4.6/dirs/a.sh": "a2"}))
    assert find_copy_problems(base, stale, declared=set()) == [
        "template/v4/v4.7/dirs/a.sh differs from template/v4/v4.6/dirs/a.sh and is not declared."
    ]
    assert find_copy_problems(base, stale, declared={"template/v4/v4.7/dirs/a.sh"}) == []

    missing = {p: v for p, v in same.items() if p != "template/v4/v4.7/dirs/a.sh"}
    assert find_copy_problems(base, missing, declared=set()) == [
        "template/v4/v4.6/dirs/a.sh is missing from template/v4/v4.7/."
    ]

    lost_exec_bit = dict(same, **{"template/v4/v4.6/dirs/a.sh": ("100755", "a1")})
    assert len(find_copy_problems(base, lost_exec_bit, declared=set())) == 1


def test_new_minor_needs_the_minor_before_it():
    head = _tree({"template/v4/v4.6/Dockerfile": "d1", "template/v4/v4.8/Dockerfile": "d1"})
    assert find_copy_problems({"template/v4/v4.6/Dockerfile"}, head, declared=set()) == [
        "template/v4/v4.8/ was added, but there is no template/v4/v4.7/ to copy it from."
    ]


def test_minor_already_on_main_is_not_compared_again():
    head = _tree({"template/v4/v4.6/Dockerfile": "d1", "template/v4/v4.7/Dockerfile": "d2"})
    assert find_copy_problems(set(head), head, declared=set()) == []


def test_legacy_per_major_paths_are_rejected_once_a_major_has_minor_templates():
    assert find_legacy_path_problems(["template/v4/dirs/etc/x"], HEAD_PATHS) == [
        "template/v4/dirs/etc/x is not in a per-minor template; the build only reads template/v4/v4.<minor>/."
    ]
    assert find_legacy_path_problems(["template/v1/dirs/etc/x"], HEAD_PATHS) == []


def test_pr_description_opt_out():
    head = _tree({p: "x" for p in HEAD_PATHS})
    changed = ["template/v4/v4.5/dirs/a.sh"]
    assert find_problems(changed, set(head), head, "") != []
    assert find_problems(changed, set(head), head, "Backport only.\n\ntemplate-propagation: scoped\n") == []


def test_run_check_reads_the_git_trees(tmp_path, monkeypatch, capsys):
    def git(*args):
        result = subprocess.run(
            ["git", "-c", "user.name=test", "-c", "user.email=test@example.com", *args],
            cwd=tmp_path,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    git("init", "-q")
    for minor in (5, 6):
        (tmp_path / f"template/v4/v4.{minor}").mkdir(parents=True)
        (tmp_path / f"template/v4/v4.{minor}/a.sh").write_text("old\n")
    (tmp_path / "README.md").write_text("readme\n")
    git("add", ".")
    git("commit", "-q", "-m", "base")
    base = git("rev-parse", "HEAD")
    monkeypatch.chdir(tmp_path)

    (tmp_path / "README.md").write_text("readme v2\n")
    git("commit", "-q", "-a", "-m", "not a template change")
    assert run_check(base, git("rev-parse", "HEAD"), "") == 0

    (tmp_path / "template/v4/v4.5/a.sh").write_text("new\n")
    git("commit", "-q", "-a", "-m", "4.5 only")
    head = git("rev-parse", "HEAD")
    assert run_check(base, head, "") == 1
    assert "template/v4/v4.6/a.sh did not" in capsys.readouterr().out
    assert run_check(base, head, "template-propagation: scoped") == 0
