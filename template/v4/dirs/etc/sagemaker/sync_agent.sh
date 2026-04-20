#!/bin/bash
# Syncs agent config (subagent, default agent settings) for SMAI spaces.
set -eu

AGENT_CONFIG_SRC="/etc/sagemaker/sagemaker-default-agent.json"
AGENT_CONFIG_DST="$HOME/.kiro/agents/sagemaker-default-agent.json"
KIRO_CLI_SETTINGS="$HOME/.kiro/settings/cli.json"

# Install subagent config (always overwrite)
mkdir -p "$HOME/.kiro/agents"
cp "$AGENT_CONFIG_SRC" "$AGENT_CONFIG_DST"
echo "Installed agent config to $AGENT_CONFIG_DST"

# Set default agent only if user hasn't configured one
mkdir -p "$HOME/.kiro/settings"
if [ ! -f "$KIRO_CLI_SETTINGS" ]; then
    echo '{"chat.defaultAgent":"sagemaker_default"}' > "$KIRO_CLI_SETTINGS"
    echo "Created default agent settings"
elif ! jq -e '."chat.defaultAgent"' "$KIRO_CLI_SETTINGS" >/dev/null 2>&1; then
    jq '. + {"chat.defaultAgent":"sagemaker_default"}' "$KIRO_CLI_SETTINGS" > "$KIRO_CLI_SETTINGS.tmp"
    mv "$KIRO_CLI_SETTINGS.tmp" "$KIRO_CLI_SETTINGS"
    echo "Added default agent to existing settings"
fi
