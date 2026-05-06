#!/bin/bash
# Syncs pre-packaged SageMaker skills from image to user's EBS.
set -eu

IMAGE_SKILLS_DIR="/etc/sagemaker/skills"
EBS_SKILLS_DIR="$HOME/.agent/skills"
LOCK_FILE="$EBS_SKILLS_DIR/.sagemaker-lock"

# Agent targets to symlink skills into (add new agents here)
AGENT_SKILLS_DIRS=("$HOME/.kiro/skills")

compute_checksum() {
    (cd "$1" && find . -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum | awk '{print $1}')
}

get_locked_checksum() {
    [ -f "$LOCK_FILE" ] && jq -r --arg s "$1" '.skills[$s].checksum // empty' "$LOCK_FILE" 2>/dev/null
}

set_locked_checksum() {
    [ -f "$LOCK_FILE" ] || echo '{"skills":{}}' > "$LOCK_FILE"
    jq --arg s "$1" --arg c "$2" '.skills[$s].checksum = $c' "$LOCK_FILE" > "$LOCK_FILE.tmp"
    mv "$LOCK_FILE.tmp" "$LOCK_FILE"
}

mkdir -p "$EBS_SKILLS_DIR"
for dir in "${AGENT_SKILLS_DIRS[@]}"; do mkdir -p "$dir"; done

if [ ! -d "$IMAGE_SKILLS_DIR" ]; then
    echo "No bundled skills found at $IMAGE_SKILLS_DIR, skipping."
    exit 0
fi

for skill_path in "$IMAGE_SKILLS_DIR"/*/; do
    [ -d "$skill_path" ] || continue
    skill_name=$(basename "$skill_path")
    ebs_skill="$EBS_SKILLS_DIR/$skill_name"
    image_checksum=$(compute_checksum "$skill_path")

    if [ ! -d "$ebs_skill" ]; then
        cp -r "$skill_path" "$ebs_skill"
        set_locked_checksum "$skill_name" "$image_checksum"
        echo "Installed skill '$skill_name'"
    else
        recorded_checksum=$(get_locked_checksum "$skill_name")
        current_checksum=$(compute_checksum "$ebs_skill")

        if [ "$current_checksum" = "$recorded_checksum" ]; then
            if [ "$image_checksum" != "$recorded_checksum" ]; then
                rm -rf "$ebs_skill"
                cp -r "$skill_path" "$ebs_skill"
                set_locked_checksum "$skill_name" "$image_checksum"
                echo "Updated skill '$skill_name'"
            else
                echo "Skill '$skill_name' already current, skipping"
            fi
        else
            echo "Skipping skill '$skill_name' — user modified"
        fi
    fi

    # Create symlinks for all agent targets
    for agent_dir in "${AGENT_SKILLS_DIRS[@]}"; do
        link="$agent_dir/$skill_name"
        if [ ! -e "$link" ]; then
            ln -s "$ebs_skill" "$link"
            echo "Created symlink $link -> $ebs_skill"
        fi
    done
done

echo "Skills sync complete."
