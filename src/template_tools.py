"""Helpers for the per-minor image templates under template/v{major}/v{major}.{minor}/.

This module only uses the standard library, so workflows can run it with a plain Python
interpreter instead of the sagemaker-distribution conda environment.

Commands:

    python src/template_tools.py check --base <sha> --head <sha> [--pr-body-file <path>]
        Check a pull request's template changes. See find_problems() for the rules.

Why the check exists: a new minor's template is a one-time copy of the previous minor's template.
Nothing carries later template changes forward, so a change merged to an older minor's template
after the copy skips the newer minor unless it is made there too (4.6.0 missed #1343 this way).
"""

import argparse
import os
import re
import subprocess
import sys

_MINOR_TEMPLATE_PATH = re.compile(r"^template/v(\d+)/v(\d+)\.(\d+)/(.+)$")
_LEGACY_TEMPLATE_PATH = re.compile(r"^template/v(\d+)/(.+)$")
_SCOPED_OPT_OUT = re.compile(r"^\s*template-propagation:\s*scoped\s*$", re.MULTILINE | re.IGNORECASE)
_DECLARED_DIVERGENCE = re.compile(r"^\s*template-divergence:\s*(\S+)\s*$", re.MULTILINE)


def minor_template_dir(major, minor):
    return f"template/v{major}/v{major}.{minor}"


def parse_minor_template_path(path):
    """Return (major, minor, path inside the template) for a per-minor template file, or None."""
    match = _MINOR_TEMPLATE_PATH.match(path)
    if not match or match.group(1) != match.group(2):
        return None
    return int(match.group(2)), int(match.group(3)), match.group(4)


def minors_by_major(paths):
    """Map each major version to the set of minors that have a template directory in `paths`."""
    minors = {}
    for path in paths:
        parsed = parse_minor_template_path(path)
        if parsed:
            minors.setdefault(parsed[0], set()).add(parsed[1])
    return minors


def find_propagation_problems(changed_paths, head_paths, scoped):
    """Rule 1: changing an older minor's template file must change the same file in the newest minor too.

    The newest minor template is a copy taken once, so nothing else carries the change forward.
    `scoped` (from `template-propagation: scoped` in the PR description) waives this for deliberate
    backports.
    """
    if scoped:
        return []
    newest = {major: max(minors) for major, minors in minors_by_major(head_paths).items()}
    changed = set(changed_paths)
    problems = []
    for path in sorted(changed):
        parsed = parse_minor_template_path(path)
        if not parsed:
            continue
        major, minor, inner = parsed
        if minor >= newest.get(major, minor):
            continue
        counterpart = f"{minor_template_dir(major, newest[major])}/{inner}"
        if counterpart not in changed:
            problems.append(f"{path} changed, but {counterpart} did not.")
    return problems


def find_copy_problems(base_paths, head_tree, declared):
    """Rule 2: a newly added minor template must match the previous minor's template file for file.

    `head_tree` maps path -> (mode, blob id). Files that are meant to differ in the new minor must be
    listed in the PR description as `template-divergence: <path>`. Run against the PR merged with the
    latest main, this also catches a change to the previous minor that landed after the copy was made.
    """
    added = minors_by_major(head_tree)
    existing = minors_by_major(base_paths)
    problems = []
    for major in sorted(added):
        for minor in sorted(added[major] - existing.get(major, set())):
            new_dir, previous_dir = minor_template_dir(major, minor), minor_template_dir(major, minor - 1)
            if minor == 0:
                continue
            if minor - 1 not in added[major]:
                problems.append(f"{new_dir}/ was added, but there is no {previous_dir}/ to copy it from.")
                continue
            new_files = {p[len(new_dir) + 1 :]: v for p, v in head_tree.items() if p.startswith(new_dir + "/")}
            old_files = {
                p[len(previous_dir) + 1 :]: v for p, v in head_tree.items() if p.startswith(previous_dir + "/")
            }
            for inner in sorted(set(new_files) | set(old_files)):
                if f"{new_dir}/{inner}" in declared:
                    continue
                if inner not in new_files:
                    problems.append(f"{previous_dir}/{inner} is missing from {new_dir}/.")
                elif inner not in old_files:
                    problems.append(f"{new_dir}/{inner} is not in {previous_dir}/ and is not declared.")
                elif new_files[inner] != old_files[inner]:
                    problems.append(f"{new_dir}/{inner} differs from {previous_dir}/{inner} and is not declared.")
    return problems


def find_legacy_path_problems(changed_paths, head_paths):
    """Rule 3: for majors that have per-minor templates, the build no longer reads template/vX/<other>."""
    majors = set(minors_by_major(head_paths))
    problems = []
    for path in sorted(set(changed_paths)):
        match = _LEGACY_TEMPLATE_PATH.match(path)
        if not match or parse_minor_template_path(path) or int(match.group(1)) not in majors:
            continue
        major = match.group(1)
        problems.append(
            f"{path} is not in a per-minor template; the build only reads template/v{major}/v{major}.<minor>/."
        )
    return problems


def find_problems(changed_paths, base_paths, head_tree, pr_body):
    """Apply all three rules. `head_tree` maps path -> (mode, blob id) for the tree being merged."""
    pr_body = pr_body or ""
    scoped = bool(_SCOPED_OPT_OUT.search(pr_body))
    declared = set(_DECLARED_DIVERGENCE.findall(pr_body))
    return (
        find_propagation_problems(changed_paths, head_tree, scoped)
        + find_copy_problems(base_paths, head_tree, declared)
        + find_legacy_path_problems(changed_paths, head_tree)
    )


def _git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def _template_tree(ref):
    """Map path -> (mode, blob id) for every file under template/ at `ref`."""
    tree = {}
    for line in _git("ls-tree", "-r", ref, "--", "template").splitlines():
        meta, path = line.split("\t", 1)
        mode, _, blob = meta.split()
        tree[path] = (mode, blob)
    return tree


def run_check(base, head, pr_body):
    changed = [p for p in _git("diff", "--name-only", f"{base}...{head}").splitlines() if p.startswith("template/")]
    if not changed:
        print("No template changes.")
        return 0
    problems = find_problems(changed, set(_template_tree(base)), _template_tree(head), pr_body)
    if not problems:
        print(f"Template changes look right ({len(changed)} files).")
        return 0
    for problem in problems:
        print(f"::error::{problem}")
    print(
        "\nSee CONTRIBUTING.md, 'Modifying the Dockerfile or dirs/'. A change meant only for older minors can add "
        "`template-propagation: scoped` to the PR description. A new minor's template can list intended "
        "differences as `template-divergence: <path>` lines."
    )
    return 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="Check a pull request's template changes.")
    check.add_argument("--base", required=True, help="Commit the pull request merges into.")
    check.add_argument("--head", required=True, help="The pull request merged with --base.")
    check.add_argument("--pr-body-file", help="File containing the pull request description.")
    args = parser.parse_args(argv)

    pr_body = ""
    if args.pr_body_file:
        with open(args.pr_body_file) as f:
            pr_body = f.read()
    return run_check(args.base, args.head, pr_body)


if __name__ == "__main__":
    sys.exit(main())
