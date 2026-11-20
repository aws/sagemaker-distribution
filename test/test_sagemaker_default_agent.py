from __future__ import annotations

import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_VERSIONS = (
    "v4.3",
    "v4.4",
    "v4.5",
    "v4.6",
    "v4.7",
    "v4.8",
    "v5.0",
    "v5.1",
)
LEGACY_SKILL_TEMPLATE_VERSIONS = ("v4.3", "v4.4")
SKILL_UPDATE_TEMPLATE_VERSIONS = ("v4.5", "v4.6", "v4.7", "v4.8", "v5.0", "v5.1")
AGENT_CONFIGS = tuple(
    ROOT / "template" / version.split(".")[0] / version / "dirs" / "etc" / "sagemaker" / "sagemaker-default-agent.json"
    for version in SKILL_UPDATE_TEMPLATE_VERSIONS
)
LEGACY_AGENT_CONFIGS = tuple(
    ROOT / "template" / version.split(".")[0] / version / "dirs" / "etc" / "sagemaker" / "sagemaker-default-agent.json"
    for version in LEGACY_SKILL_TEMPLATE_VERSIONS
)
ALL_CLAUDE_AGENT_CONFIGS = tuple(
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
CLAUDE_AGENT_CONFIGS = tuple(
    ROOT
    / "template"
    / version.split(".")[0]
    / version
    / "dirs"
    / "etc"
    / "sagemaker"
    / "claude-sagemaker-default-agent.md"
    for version in SKILL_UPDATE_TEMPLATE_VERSIONS
)
SYNC_AGENT_SCRIPTS = tuple(
    ROOT / "template" / version.split(".")[0] / version / "dirs" / "etc" / "sagemaker" / "sync_agent.sh"
    for version in TEMPLATE_VERSIONS
)
DOCKERFILES = tuple(ROOT / "template" / version.split(".")[0] / version / "Dockerfile" for version in TEMPLATE_VERSIONS)
SYNC_SKILLS_SCRIPTS = tuple(
    ROOT / "template" / version.split(".")[0] / version / "dirs" / "etc" / "sagemaker" / "skills" / "sync_skills.sh"
    for version in TEMPLATE_VERSIONS
)
JUPYTER_CONFIGS = tuple(
    ROOT / "template" / version.split(".")[0] / version / "dirs" / "etc" / "jupyter" / "jupyter_server_config.py"
    for version in TEMPLATE_VERSIONS
)
SMUS_TEMPLATE_VERSIONS = ("v4.5", "v4.6", "v4.7", "v4.8", "v5.0", "v5.1")
SMUS_JUPYTER_CONFIGS = tuple(
    ROOT
    / "template"
    / version.split(".")[0]
    / version
    / "dirs"
    / "etc"
    / "sagemaker-ui"
    / "jupyter"
    / "server"
    / "jupyter_server_config.py"
    for version in SMUS_TEMPLATE_VERSIONS
)
CODEX_TEMPLATE_VERSIONS = TEMPLATE_VERSIONS
ALL_CODEX_CONFIGS = tuple(
    ROOT / "template" / version.split(".")[0] / version / "dirs" / "etc" / "codex" / "config.toml"
    for version in CODEX_TEMPLATE_VERSIONS
)
CODEX_CONFIGS = tuple(
    ROOT / "template" / version.split(".")[0] / version / "dirs" / "etc" / "codex" / "config.toml"
    for version in SKILL_UPDATE_TEMPLATE_VERSIONS
)
UPDATE_SYNC_SKILLS_SCRIPTS = tuple(
    ROOT / "template" / version.split(".")[0] / version / "dirs" / "etc" / "sagemaker" / "skills" / "sync_skills.sh"
    for version in SKILL_UPDATE_TEMPLATE_VERSIONS
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


@pytest.fixture(params=AGENT_CONFIGS, ids=SKILL_UPDATE_TEMPLATE_VERSIONS)
def agent_config(request: pytest.FixtureRequest) -> dict:
    return json.loads(request.param.read_text(encoding="utf-8"))


@pytest.fixture(params=CLAUDE_AGENT_CONFIGS, ids=SKILL_UPDATE_TEMPLATE_VERSIONS)
def claude_agent_config(request: pytest.FixtureRequest) -> tuple[str, str]:
    return _read_claude_agent(request.param)


@pytest.fixture(params=CODEX_CONFIGS, ids=SKILL_UPDATE_TEMPLATE_VERSIONS)
def codex_config(request: pytest.FixtureRequest) -> tuple[str, str]:
    return _read_codex_developer_instructions(request.param)


def test_legacy_skill_templates_do_not_add_update_instructions():
    for version, kiro_path in zip(LEGACY_SKILL_TEMPLATE_VERSIONS, LEGACY_AGENT_CONFIGS):
        template_root = ROOT / "template" / version.split(".")[0] / version
        prompts = (
            json.loads(kiro_path.read_text(encoding="utf-8"))["prompt"],
            _read_claude_agent(template_root / "dirs" / "etc" / "sagemaker" / "claude-sagemaker-default-agent.md")[1],
            _read_codex_developer_instructions(template_root / "dirs" / "etc" / "codex" / "config.toml")[1],
        )
        for prompt in prompts:
            assert "aws-ai-ml" not in prompt
            assert "agent-toolkit" not in prompt
            assert "update-skill" not in prompt


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
    assert "Kiro, Claude Code, and Codex share this Skill" in prompt
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


@pytest.mark.parametrize("agent_path", ALL_CLAUDE_AGENT_CONFIGS, ids=TEMPLATE_VERSIONS)
def test_claude_agent_has_sagemaker_default_identity(agent_path):
    frontmatter, _ = _read_claude_agent(agent_path)

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
    assert "Kiro, Claude Code, and Codex share this Skill" in prompt
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


@pytest.mark.parametrize("config_path", ALL_CODEX_CONFIGS, ids=CODEX_TEMPLATE_VERSIONS)
def test_codex_config_selects_bedrock_and_adds_sagemaker_instructions(config_path):
    config, prompt = _read_codex_developer_instructions(config_path)

    assert 'model_provider = "amazon-bedrock"' in config
    assert 'model = "openai.gpt-5.4"' in config
    assert "You are a specialized AI assistant for Amazon SageMaker Studio" in prompt


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
    configs = [path.read_text(encoding="utf-8") for path in CODEX_CONFIGS]

    assert len(set(configs)) == 1


@pytest.mark.parametrize("dockerfile", DOCKERFILES, ids=TEMPLATE_VERSIONS)
def test_dockerfiles_install_claude_and_codex_runtimes(dockerfile):
    content = dockerfile.read_text(encoding="utf-8")

    assert content.count("# Install agent CLIs and JupyterLab ACP adapters") == 1
    assert content.count("@anthropic-ai/claude-code@2.1.322") == 1
    assert content.count("@openai/codex@0.170.0") == 1
    assert content.count("@agentclientprotocol/claude-agent-acp@0.109.0") == 1
    assert content.count("@agentclientprotocol/codex-acp@2.8.0") == 1
    assert content.count("ENV CLAUDE_CODE_USE_BEDROCK=1") == 1
    assert content.count("ENV DISABLE_AUTOUPDATER=1") == 1


@pytest.mark.parametrize("sync_script", SYNC_SKILLS_SCRIPTS, ids=TEMPLATE_VERSIONS)
def test_sync_skills_adds_codex_discovery(sync_script):
    script = sync_script.read_text(encoding="utf-8")

    assert '"$HOME/.agents/skills"' in script


@pytest.mark.parametrize("sync_script", UPDATE_SYNC_SKILLS_SCRIPTS, ids=SKILL_UPDATE_TEMPLATE_VERSIONS)
def test_skill_update_templates_enable_codex_toolkit_detection(sync_script):
    script = sync_script.read_text(encoding="utf-8")

    assert 'mkdir -p "$HOME/.codex"' in script


@pytest.mark.parametrize("jupyter_config", JUPYTER_CONFIGS, ids=TEMPLATE_VERSIONS)
def test_jupyter_defaults_to_claude(jupyter_config):
    config = jupyter_config.read_text(encoding="utf-8")

    assert "jupyter_ai_acp_client::ClaudeAcpPersona" in config
    assert "jupyter_ai_acp_client::KiroAcpPersona" not in config


@pytest.mark.parametrize("jupyter_config", SMUS_JUPYTER_CONFIGS, ids=SMUS_TEMPLATE_VERSIONS)
def test_smus_jupyter_keeps_kiro_default(jupyter_config):
    config = jupyter_config.read_text(encoding="utf-8")

    assert "jupyter_ai_acp_client::KiroAcpPersona" in config
    assert "jupyter_ai_acp_client::ClaudeAcpPersona" not in config


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
