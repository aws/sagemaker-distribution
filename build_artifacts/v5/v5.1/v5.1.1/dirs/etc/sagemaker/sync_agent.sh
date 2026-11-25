#!/bin/bash
# Syncs agent config (subagent, default agent settings) for SMAI spaces.
set -eu

KIRO_AGENT_CONFIG_SRC="/etc/sagemaker/sagemaker-default-agent.json"
KIRO_AGENT_CONFIG_DST="$HOME/.kiro/agents/sagemaker-default-agent.json"
KIRO_CLI_SETTINGS="$HOME/.kiro/settings/cli.json"
CLAUDE_AGENT_CONFIG_SRC="/etc/sagemaker/claude-sagemaker-default-agent.md"
CLAUDE_AGENT_CONFIG_DST="$HOME/.claude/agents/sagemaker-default-agent.md"
CLAUDE_CODE_SETTINGS="$HOME/.claude/settings.json"

# Install agent configs (always overwrite)
mkdir -p "$HOME/.kiro/agents" "$HOME/.claude/agents"
cp "$KIRO_AGENT_CONFIG_SRC" "$KIRO_AGENT_CONFIG_DST"
echo "Installed agent config to $KIRO_AGENT_CONFIG_DST"
cp "$CLAUDE_AGENT_CONFIG_SRC" "$CLAUDE_AGENT_CONFIG_DST"
echo "Installed agent config to $CLAUDE_AGENT_CONFIG_DST"

# Set the Kiro default agent only if the user hasn't configured one
mkdir -p "$HOME/.kiro/settings"
if [ ! -f "$KIRO_CLI_SETTINGS" ]; then
    echo '{"chat.defaultAgent":"sagemaker_default"}' > "$KIRO_CLI_SETTINGS"
    echo "Created default agent settings"
elif ! jq -e '."chat.defaultAgent"' "$KIRO_CLI_SETTINGS" >/dev/null 2>&1; then
    jq '. + {"chat.defaultAgent":"sagemaker_default"}' "$KIRO_CLI_SETTINGS" > "$KIRO_CLI_SETTINGS.tmp"
    mv "$KIRO_CLI_SETTINGS.tmp" "$KIRO_CLI_SETTINGS"
    echo "Added default agent to existing settings"
fi

# Set the Claude Code default agent only if the user hasn't configured one
mkdir -p "$HOME/.claude"
if [ ! -f "$CLAUDE_CODE_SETTINGS" ]; then
    echo '{"agent":"sagemaker_default"}' > "$CLAUDE_CODE_SETTINGS"
    echo "Created Claude Code default agent settings"
elif ! jq -e '.agent' "$CLAUDE_CODE_SETTINGS" >/dev/null 2>&1; then
    jq '. + {"agent":"sagemaker_default"}' "$CLAUDE_CODE_SETTINGS" > "$CLAUDE_CODE_SETTINGS.tmp"
    mv "$CLAUDE_CODE_SETTINGS.tmp" "$CLAUDE_CODE_SETTINGS"
    echo "Added Claude Code default agent to existing settings"
fi
