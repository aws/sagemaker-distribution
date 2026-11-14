from __future__ import annotations

import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[1]
AGENT_CONFIGS = tuple(
    ROOT / "template" / "v5" / minor / "dirs" / "etc" / "sagemaker" / "sagemaker-default-agent.json"
    for minor in ("v5.0", "v5.1")
)


@pytest.fixture(params=AGENT_CONFIGS, ids=("v5.0", "v5.1"))
def agent_config(request: pytest.FixtureRequest) -> dict:
    return json.loads(request.param.read_text(encoding="utf-8"))


def test_agent_checks_aws_ai_ml_updates_once_per_conversation(agent_config):
    prompt = agent_config["prompt"]

    assert "Before using the aws-ai-ml Skill" in prompt
    assert "for the first time in each conversation" in prompt
    assert "$HOME/.kiro/skills/aws-ai-ml/.aws-skill-metadata" in prompt
    assert "aws agent-toolkit check-skill-updates" in prompt
    assert "--agent kiro" in prompt
    assert "read only the aws-ai-ml result" in prompt


def test_agent_silently_skips_unmanaged_or_current_skills(agent_config):
    prompt = agent_config["prompt"]

    assert "If $HOME/.kiro/skills/aws-ai-ml/.aws-skill-metadata is absent" in prompt
    assert "silently continue with the installed Skill" in prompt
    assert "If no update exists, silently continue" in prompt
    assert "If the check fails, briefly report the error" in prompt


def test_agent_warns_and_waits_before_overwriting(agent_config):
    prompt = agent_config["prompt"]

    assert "updating replaces the complete installed Skill instead of merging changes" in prompt
    assert "local changes may be lost" in prompt
    assert "Kiro and Claude Code share this Skill" in prompt
    assert "Ask whether to update now, then stop and wait" in prompt
    assert "Only after explicit approval" in prompt


def test_agent_calls_toolkit_update_directly(agent_config):
    prompt = agent_config["prompt"]

    assert "export AWS_SDK_UA_APP_ID=AWSSkill-SageMaker" in prompt
    assert "aws agent-toolkit update-skill" in prompt
    assert "--skill-name aws-ai-ml" in prompt
    assert "start a new conversation" in prompt
    assert "If it fails, report the error and stop" in prompt
    assert "backup" not in prompt.lower()
    assert "rollback" not in prompt.lower()


def test_v5_agent_configs_remain_identical():
    configs = [json.loads(path.read_text(encoding="utf-8")) for path in AGENT_CONFIGS]

    assert configs[0] == configs[1]
