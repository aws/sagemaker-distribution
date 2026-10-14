from __future__ import absolute_import

import filecmp
import importlib.util
import json
import os
import tempfile

import pytest

pytestmark = pytest.mark.unit

ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")

# merge-settings-util.py is duplicated identically across every supported
# v4.x template (see TestAllTemplateCopiesAreIdentical below); import the
# newest copy as the canonical module under test.
_SCRIPT_PATH = os.path.join(ROOT_DIR, "template", "v4", "v4.7", "dirs", "usr", "local", "bin", "merge-settings-util.py")
_SPEC = importlib.util.spec_from_file_location("merge_settings_util", _SCRIPT_PATH)
merge_settings_util = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(merge_settings_util)

SUPPORTED_V4_MINOR_VERSIONS = ["v4.1", "v4.2", "v4.3", "v4.4", "v4.5", "v4.6", "v4.7"]


def _write(content):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    f.write(content)
    f.close()
    return f.name


class TestStripJsonc:
    """Tests for _strip_jsonc, the comment/trailing-comma stripper."""

    def test_line_comment_removed(self):
        assert merge_settings_util._strip_jsonc('{\n  // comment\n  "a": 1\n}') == '{\n  \n  "a": 1\n}'

    def test_block_comment_removed(self):
        assert merge_settings_util._strip_jsonc('{ /* comment */ "a": 1 }') == '{  "a": 1 }'

    def test_trailing_comma_in_object_removed(self):
        # Asserts on the parsed value, not the exact stripped text: the
        # stripper may reposition whitespace around a dropped comma, which
        # is immaterial since json.loads doesn't care and the caller
        # re-serializes the result with json.dump anyway.
        stripped = merge_settings_util._strip_jsonc('{"a": 1, "b": 2,}')
        assert json.loads(stripped) == {"a": 1, "b": 2}

    def test_trailing_comma_in_array_removed(self):
        stripped = merge_settings_util._strip_jsonc("[1, 2, 3,]")
        assert json.loads(stripped) == [1, 2, 3]

    def test_url_value_with_double_slash_is_not_treated_as_comment(self):
        # Regression test: a naive "strip everything after //" approach
        # corrupts any setting whose *value* happens to contain "//",
        # e.g. "http.proxy": "http://proxy:8080" (very common in real
        # settings.json files: proxies, git remotes, extension URLs).
        text = '{"http.proxy": "http://proxy:8080"}'
        stripped = merge_settings_util._strip_jsonc(text)
        assert json.loads(stripped) == {"http.proxy": "http://proxy:8080"}

    def test_comma_inside_string_value_is_not_removed(self):
        text = '{"note": "a, b, c,"}'
        stripped = merge_settings_util._strip_jsonc(text)
        assert json.loads(stripped) == {"note": "a, b, c,"}

    def test_escaped_quote_does_not_confuse_string_tracking(self):
        text = '{"msg": "she said \\"hi // there\\", ok"}'
        stripped = merge_settings_util._strip_jsonc(text)
        assert json.loads(stripped) == {"msg": 'she said "hi // there", ok'}


class TestMain:
    """Tests for main(), the file1/file2 merge entrypoint."""

    def test_merge_overrides_file1_keys_with_file2(self):
        file1 = _write('{"a": 1, "b": 2}')
        file2 = _write('{"b": 3, "c": 4}')
        try:
            import sys

            sys.argv = ["merge-settings-util.py", file1, file2]
            merge_settings_util.main()
            with open(file1) as f:
                assert json.load(f) == {"a": 1, "b": 3, "c": 4}
        finally:
            os.unlink(file1)
            os.unlink(file2)

    def test_jsonc_trailing_comma_from_issue_repro_merges_successfully(self):
        # The exact repro from aws/amazon-sagemaker-feedback#255: a trailing
        # comma, valid in the VS Code UI, previously caused json.load() to
        # raise and (via `set -e` in start-code-editor) permanently broke
        # the Code Editor instance.
        file1 = _write(
            '{\n'
            '    "python.terminal.activateEnvironment": false,\n'
            '    "python.defaultInterpreterPath": "/opt/conda/bin/python",\n'
            "}\n"
        )
        file2 = _write('{"editor.fontSize": 14}')
        try:
            import sys

            sys.argv = ["merge-settings-util.py", file1, file2]
            merge_settings_util.main()
            with open(file1) as f:
                merged = json.load(f)
            assert merged == {
                "python.terminal.activateEnvironment": False,
                "python.defaultInterpreterPath": "/opt/conda/bin/python",
                "editor.fontSize": 14,
            }
        finally:
            os.unlink(file1)
            os.unlink(file2)

    def test_malformed_json_leaves_file1_unchanged_and_does_not_raise(self, capsys):
        original_content = '{"a": 1\n'
        file1 = _write(original_content)
        file2 = _write('{"b": 2}')
        try:
            import sys

            sys.argv = ["merge-settings-util.py", file1, file2]
            merge_settings_util.main()  # must not raise
            with open(file1) as f:
                assert f.read() == original_content
            assert "failed to merge settings" in capsys.readouterr().err
        finally:
            os.unlink(file1)
            os.unlink(file2)

    def test_missing_file2_leaves_file1_unchanged_and_does_not_raise(self, capsys):
        original_content = '{"a": 1}'
        file1 = _write(original_content)
        try:
            import sys

            sys.argv = ["merge-settings-util.py", file1, "/nonexistent/path/settings.json"]
            merge_settings_util.main()  # must not raise
            with open(file1) as f:
                assert f.read() == original_content
            assert "failed to merge settings" in capsys.readouterr().err
        finally:
            os.unlink(file1)


class TestAllTemplateCopiesAreIdentical:
    """merge-settings-util.py has no single canonical source location; it's
    duplicated verbatim into every supported v4.x template directory. Guard
    against the copies silently drifting apart in future changes."""

    def test_all_supported_v4_templates_match_v4_7(self):
        canonical = _SCRIPT_PATH
        for minor in SUPPORTED_V4_MINOR_VERSIONS:
            path = os.path.join(ROOT_DIR, "template", "v4", minor, "dirs", "usr", "local", "bin", "merge-settings-util.py")
            assert filecmp.cmp(canonical, path, shallow=False), f"{path} differs from {canonical}"
