#!/bin/bash
set -e

USER_SETTINGS_FILE="/home/sagemaker-user/sagemaker-code-editor-server-data/data/User/settings.json"
COLOR_THEME_KEY="workbench.colorTheme"
COLOR_THEME_VALUE="Default Dark Modern"

# Check if the settings file exists
if [ ! -f "$USER_SETTINGS_FILE" ]; then
    echo "Code Editor user settings file not found. Creating..."
    mkdir -p "$(dirname "$USER_SETTINGS_FILE")"
    echo "{}" > "$USER_SETTINGS_FILE"
fi

EXISTING_COLOR_THEME_VALUE=$(jq -r --arg key "$COLOR_THEME_KEY" '.[$key] // empty' "$USER_SETTINGS_FILE")

if [[ -n "$EXISTING_COLOR_THEME_VALUE" ]]; then
    echo "Theme is already set in user settings as '$EXISTING_COLOR_THEME_VALUE'. No changes made."
else
    # Set theme
    jq --arg key "$COLOR_THEME_KEY" --arg value "$COLOR_THEME_VALUE" '.[$key] = $value' "$USER_SETTINGS_FILE" > "${USER_SETTINGS_FILE}.tmp" && mv "${USER_SETTINGS_FILE}.tmp" "$USER_SETTINGS_FILE"
    echo "Successfully set Code Editor theme to '$COLOR_THEME_VALUE'."
fi
