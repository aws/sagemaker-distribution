from __future__ import annotations

import json
from pathlib import Path

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
AGENT_CONFIGS = tuple(
    ROOT / "template" / version.split(".")[0] / version / "dirs" / "etc" / "sagemaker" / "sagemaker-default-agent.json"
    for version in TEMPLATE_VERSIONS
)
CLAUDE_AGENT_CONFIGS = tuple(
    ROOT
    / "template"
    / version.split(".")[0]
    / version
    / "dirs"
    / "etc"
    / "sagemaker"
    / "claude-sagemaker-default-agent.md"
    for version in TEMPLATE_VERSIONS
)
SYNC_AGENT_SCRIPTS = tuple(
    ROOT / "template" / version.split(".")[0] / version / "dirs" / "etc" / "sagemaker" / "sync_agent.sh"
    for version in TEMPLATE_VERSIONS
)
CODEX_TEMPLATE_VERSIONS = ("v5.0", "v5.1")
CODEX_CONFIGS = tuple(
    ROOT / "template" / "v5" / version / "dirs" / "etc" / "codex" / "config.toml" for version in CODEX_TEMPLATE_VERSIONS
)


def _read_claude_agent(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    frontmatter_marker, frontmatter, prompt = text.split("---", maxsplit=2)
    assert frontmatter_marker == ""
    return frontmatter, prompt.strip()


def _read_codex_developer_instructions(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    prefix = 'developer_instructions = """'
    before, prompt = text.split(prefix, maxsplit=1)
    prompt, trailing = prompt.rsplit('"""', maxsplit=1)
    assert not trailing.strip()
    return before, prompt.strip()


@pytest.fixture(params=AGENT_CONFIGS, ids=TEMPLATE_VERSIONS)
def agent_config(request: pytest.FixtureRequest) -> dict:
    return json.loads(request.param.read_text(encoding="utf-8"))


@pytest.fixture(params=CLAUDE_AGENT_CONFIGS, ids=TEMPLATE_VERSIONS)
def claude_agent_config(request: pytest.FixtureRequest) -> tuple[str, str]:
    return _read_claude_agent(request.param)


@pytest.fixture(params=CODEX_CONFIGS, ids=CODEX_TEMPLATE_VERSIONS)
def codex_config(request: pytest.FixtureRequest) -> tuple[str, str]:
    return _read_codex_developer_instructions(request.param)


def test_agent_checks_aws_ai_ml_updates_once_per_conversation(agent_config):
    prompt = agent_config["prompt"]

    assert "Before using the aws-ai-ml Skill" in prompt
    assert "for the first time in each conversation" in prompt
    assert "aws agent-toolkit check-skill-updates" in prompt
    assert "--agent kiro" in prompt
    assert "read only the aws-ai-ml result" in prompt


def test_agent_relies_on_toolkit_result(agent_config):
    prompt = agent_config["prompt"]

    assert ".aws-skill-metadata" not in prompt
    assert "If the command returns no aws-ai-ml result or no update exists" in prompt
    assert "silently continue with the installed Skill" in prompt
    assert "If the check fails, briefly report the error" in prompt


def test_agent_uses_default_cli_timeouts(agent_config):
    prompt = agent_config["prompt"]

    assert "--cli-connect-timeout" not in prompt
    assert "--cli-read-timeout" not in prompt


def test_agent_warns_and_waits_before_overwriting(agent_config):
    prompt = agent_config["prompt"]

    assert "updating replaces the complete installed Skill instead of merging changes" in prompt
    assert "local changes may be lost" in prompt
    assert "Kiro and Claude Code share this Skill" in prompt
    assert "Ask whether to update now, then stop and wait" in prompt
    assert "Only after explicit approval" in prompt


def test_agent_calls_toolkit_update_and_reloads_skill(agent_config):
    prompt = agent_config["prompt"]

    assert "export AWS_SDK_UA_APP_ID=AWSSkill-SageMaker" in prompt
    assert "aws agent-toolkit update-skill" in prompt
    assert "--skill-name aws-ai-ml" in prompt
    assert ("immediately read the complete updated " "$HOME/.kiro/skills/aws-ai-ml/SKILL.md from disk") in prompt
    assert "updated instructions are added to this conversation" in prompt
    assert "disregard the previously loaded Skill instructions" in prompt
    assert "continue the original workflow using the updated Skill" in prompt
    assert "start a new conversation" not in prompt
    assert "If it fails, report the error and stop" in prompt
    assert "backup" not in prompt.lower()
    assert "rollback" not in prompt.lower()


def test_agent_prompts_remain_identical_across_templates():
    prompts = [json.loads(path.read_text(encoding="utf-8"))["prompt"] for path in AGENT_CONFIGS]

    assert len(set(prompts)) == 1


def test_claude_agent_has_sagemaker_default_identity(claude_agent_config):
    frontmatter, _ = claude_agent_config

    assert "name: sagemaker_default" in frontmatter
    assert "description: SageMaker AI assistant" in frontmatter
    assert "skills:" not in frontmatter
    assert "tools:" not in frontmatter


def test_claude_agent_checks_and_updates_aws_ai_ml(claude_agent_config):
    _, prompt = claude_agent_config

    assert "Before using the aws-ai-ml Skill" in prompt
    assert "for the first time in each conversation" in prompt
    assert "aws agent-toolkit check-skill-updates" in prompt
    assert "aws agent-toolkit update-skill" in prompt
    assert "--skill-name aws-ai-ml" in prompt
    assert "--agent claude-code" in prompt
    assert "--agent kiro" not in prompt


def test_claude_agent_warns_and_reloads_updated_skill(claude_agent_config):
    _, prompt = claude_agent_config

    assert "updating replaces the complete installed Skill instead of merging changes" in prompt
    assert "local changes may be lost" in prompt
    assert "Ask whether to update now, then stop and wait" in prompt
    assert "Only after explicit approval" in prompt
    assert "$HOME/.claude/skills/aws-ai-ml/SKILL.md" in prompt
    assert "updated instructions are added to this conversation" in prompt
    assert "continue the original workflow using the updated Skill" in prompt
    assert "start a new conversation" not in prompt
    assert "backup" not in prompt.lower()
    assert "rollback" not in prompt.lower()


def test_claude_agent_prompts_remain_identical_across_templates():
    prompts = [_read_claude_agent(path)[1] for path in CLAUDE_AGENT_CONFIGS]

    assert len(set(prompts)) == 1


def test_codex_config_selects_bedrock_and_adds_sagemaker_instructions(codex_config):
    config, prompt = codex_config

    assert 'model_provider = "amazon-bedrock"' in config
    assert "You are a specialized AI assistant for Amazon SageMaker Studio" in prompt
    assert "Before using the aws-ai-ml Skill" in prompt
    assert "for the first time in each conversation" in prompt


def test_codex_checks_aws_ai_ml_updates_with_toolkit(codex_config):
    _, prompt = codex_config

    assert "export AWS_SDK_UA_APP_ID=AWSSkill-SageMaker" in prompt
    assert "aws agent-toolkit check-skill-updates" in prompt
    assert "read only the aws-ai-ml result" in prompt
    assert "--agent codex" in prompt
    assert "--agent kiro" not in prompt
    assert "--agent claude-code" not in prompt
    assert ".aws-skill-metadata" not in prompt
    assert "--cli-connect-timeout" not in prompt
    assert "--cli-read-timeout" not in prompt
    assert "If the command returns no aws-ai-ml result or no update exists" in prompt
    assert "If the check fails, briefly report the error" in prompt


def test_codex_warns_updates_and_reloads_shared_skill(codex_config):
    _, prompt = codex_config

    assert "updating replaces the complete installed Skill instead of merging changes" in prompt
    assert "local changes may be lost" in prompt
    assert "Kiro, Claude Code, and Codex share this Skill" in prompt
    assert "Ask whether to update now, then stop and wait" in prompt
    assert "Only after explicit approval" in prompt
    assert "aws agent-toolkit update-skill" in prompt
    assert "--skill-name aws-ai-ml" in prompt
    assert "$HOME/.agents/skills/aws-ai-ml/SKILL.md" in prompt
    assert "updated instructions are added to this conversation" in prompt
    assert "disregard the previously loaded Skill instructions" in prompt
    assert "continue the original workflow using the updated Skill" in prompt
    assert "If it fails, report the error and stop" in prompt
    assert "start a new conversation" not in prompt
    assert "backup" not in prompt.lower()
    assert "rollback" not in prompt.lower()


def test_codex_prompts_remain_identical_across_templates():
    prompts = [_read_codex_developer_instructions(path)[1] for path in CODEX_CONFIGS]

    assert len(set(prompts)) == 1


@pytest.mark.parametrize("sync_script", SYNC_AGENT_SCRIPTS, ids=TEMPLATE_VERSIONS)
def test_sync_agent_installs_claude_agent_and_preserves_user_default(sync_script):
    script = sync_script.read_text(encoding="utf-8")

    assert 'CLAUDE_AGENT_CONFIG_SRC="/etc/sagemaker/claude-sagemaker-default-agent.md"' in script
    assert 'CLAUDE_AGENT_CONFIG_DST="$HOME/.claude/agents/sagemaker-default-agent.md"' in script
    assert 'cp "$CLAUDE_AGENT_CONFIG_SRC" "$CLAUDE_AGENT_CONFIG_DST"' in script
    assert 'CLAUDE_CODE_SETTINGS="$HOME/.claude/settings.json"' in script
    assert '\'{"agent":"sagemaker_default"}\'' in script
    assert "elif ! jq -e '.agent'" in script
    assert 'jq \'. + {"agent":"sagemaker_default"}\'' in script


def test_sync_agent_scripts_remain_identical_across_templates():
    scripts = [path.read_text(encoding="utf-8") for path in SYNC_AGENT_SCRIPTS]

    assert len(set(scripts)) == 1
