"""Fail a pull request that changes an older minor's template without changing the newest minor's.

Each minor version has its own template, template/vX/vX.Y/. A new minor's template is a one-time copy of
the previous minor's, and nothing carries later changes forward. So a change made only to an older minor's
template never reaches future minor versions. 4.6.0 missed #1343 this way.

Run by .github/workflows/check-template-propagation.yml, which passes its inputs as environment variables:
    BASE_SHA  the commit the pull request merges into
    HEAD_SHA  the pull request merged with BASE_SHA
    SCOPED    "true" when the pull request has the template-propagation-scoped label

See "Deciding where to make your change" in CONTRIBUTING.md.
"""

import os
import re
import subprocess
import sys

# template/v4/v4.6/dirs/etc/x.sh -> major 4, minor 6, path inside the template "dirs/etc/x.sh"
TEMPLATE_FILE = re.compile(r"^template/v(\d+)/v\1\.(\d+)/(.+)$")
SCOPED_LABEL = "template-propagation-scoped"


def parse_template_path(path):
    """Return (major, minor, path inside the template) for a per-minor template file, or None."""
    match = TEMPLATE_FILE.match(path)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), match.group(3)


def find_missing_changes(changed_files, all_files):
    """Return (changed file, newest-minor counterpart) for each older-minor change the newest minor lacks.

    changed_files: template files the pull request changes.
    all_files: every template file after the pull request merges; used to find each major's newest minor.
    """
    newest = {}
    for path in all_files:
        parsed = parse_template_path(path)
        if parsed:
            major, minor, _ = parsed
            newest[major] = max(newest.get(major, minor), minor)

    changed = set(changed_files)
    missing = []
    for path in sorted(changed):
        parsed = parse_template_path(path)
        if not parsed:
            continue
        major, minor, inner_path = parsed
        newest_minor = newest.get(major, minor)
        if minor == newest_minor:
            continue
        counterpart = f"template/v{major}/v{major}.{newest_minor}/{inner_path}"
        if counterpart not in changed:
            missing.append((path, counterpart))
    return missing


def git_lines(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.splitlines()


def main():
    if os.environ.get("SCOPED") == "true":
        print(f"Skipped: the pull request has the {SCOPED_LABEL} label.")
        return 0

    base, head = os.environ["BASE_SHA"], os.environ["HEAD_SHA"]
    changed = git_lines("diff", "--name-only", f"{base}...{head}", "--", "template")
    all_files = git_lines("ls-tree", "-r", "--name-only", head, "--", "template")
    missing = find_missing_changes(changed, all_files)

    if not missing:
        print(f"OK: {len(changed)} template file(s) changed, none missing from the newest minor's template.")
        return 0

    for path, counterpart in missing:
        print(f"::error file={path}::{path} changed, but {counterpart} did not.")
    print(
        "\nA change to an older minor's template only reaches future minor versions if it is also made in "
        "the newest minor's template. Make the same change in the files listed above. If this change is "
        f"deliberately only for older minors, ask a maintainer to add the {SCOPED_LABEL} label. "
        "See 'Deciding where to make your change' in CONTRIBUTING.md."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
