#!/bin/bash
# Syncs pre-packaged SageMaker skills from image to user's EBS.
set -eu

IMAGE_SKILLS_DIR="${1:-/etc/sagemaker/skills}"
EBS_SKILLS_DIR="$HOME/.agent/skills"
LOCK_FILE="$EBS_SKILLS_DIR/.sagemaker-lock"

# Agent targets to symlink skills into (add new agents here)
AGENT_SKILLS_DIRS=("$HOME/.kiro/skills" "$HOME/.claude/skills")

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

# Migration to the unified agent-toolkit-for-aws skills.
TOOLKIT_SOURCE="agent-toolkit-for-aws"

get_lock_source() {
    [ -f "$LOCK_FILE" ] || return 0
    jq -r '.source // empty' "$LOCK_FILE" 2>/dev/null || true
}

set_lock_source() {
    [ -f "$LOCK_FILE" ] || echo '{"skills":{}}' > "$LOCK_FILE"
    jq --arg v "$1" '.source = $v' "$LOCK_FILE" > "$LOCK_FILE.tmp"
    mv "$LOCK_FILE.tmp" "$LOCK_FILE"
}

# List skill names recorded in the lock (the old agent-plugins skills).
list_locked_skills() {
    [ -f "$LOCK_FILE" ] || return 0
    jq -r '.skills | keys[]' "$LOCK_FILE" 2>/dev/null || true
}

# Remove a agent-plugins skill from EBS, its agent symlinks, and the lock entry.
remove_managed_skill() {
    local name="$1"
    local ebs_skill="$EBS_SKILLS_DIR/$name"
    for agent_dir in "${AGENT_SKILLS_DIRS[@]}"; do
        local link="$agent_dir/$name"
        # Only remove the symlink if it still points at the EBS copy we manage,
        # so a symlink the user re-pointed elsewhere is left alone.
        if [ -L "$link" ] && [ "$(readlink "$link")" = "$ebs_skill" ]; then
            rm -f "$link"
        fi
    done
    rm -rf "$ebs_skill"
    if [ -f "$LOCK_FILE" ]; then
        jq --arg s "$name" 'del(.skills[$s])' "$LOCK_FILE" > "$LOCK_FILE.tmp"
        mv "$LOCK_FILE.tmp" "$LOCK_FILE"
    fi
}

# Returns 0 (clean) if every lock-named skill still matches its recorded
# checksum (a missing EBS folder counts as clean); 1 if any was modified.
managed_skills_are_clean() {
    local name recorded current
    while IFS= read -r name; do
        [ -n "$name" ] || continue
        local ebs_skill="$EBS_SKILLS_DIR/$name"
        [ -d "$ebs_skill" ] || continue          # missing == not user-modified
        recorded=$(get_locked_checksum "$name")
        current=$(compute_checksum "$ebs_skill")
        [ "$current" = "$recorded" ] || return 1
    done < <(list_locked_skills)
    return 0
}

# Run the one-time migration. Sets MIGRATION_BLOCKS_SYNC=1 when the normal sync
# loop must be skipped, leaves it 0 otherwise.
MIGRATION_BLOCKS_SYNC=0
STAMP_SOURCE_AFTER_SYNC=0
run_migration() {
    local current_source
    current_source=$(get_lock_source)

    # Already migrated; normal loop maintains the unified skill.
    if [ "$current_source" = "$TOOLKIT_SOURCE" ]; then
        return 0
    fi

    # No managed skills recorded (or nothing to migrate).
    # Fall through to the normal loop to install the unified skill, and stamp
    # source afterwards so future runs short-circuit.
    if [ -z "$(list_locked_skills)" ]; then
        STAMP_SOURCE_AFTER_SYNC=1
        return 0
    fi

    # Existing legacy user: gate on whether they modified any managed skill.
    if managed_skills_are_clean; then
        local name
        while IFS= read -r name; do
            [ -n "$name" ] || continue
            remove_managed_skill "$name"
            echo "Migration: removed old skill '$name'"
        done < <(list_locked_skills)
        STAMP_SOURCE_AFTER_SYNC=1
    else
        echo "Migration: user-modified skills detected; keeping existing skills, skipping unified skills."
        MIGRATION_BLOCKS_SYNC=1
    fi
    return 0
}

mkdir -p "$EBS_SKILLS_DIR"
for dir in "${AGENT_SKILLS_DIRS[@]}"; do mkdir -p "$dir"; done

if [ ! -d "$IMAGE_SKILLS_DIR" ]; then
    echo "No bundled skills found at $IMAGE_SKILLS_DIR, skipping."
    exit 0
fi

run_migration
if [ "$MIGRATION_BLOCKS_SYNC" -eq 1 ]; then
    echo "Skills sync complete."
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

if [ "$STAMP_SOURCE_AFTER_SYNC" -eq 1 ]; then
    set_lock_source "$TOOLKIT_SOURCE"
    echo "Migration: stamped source=$TOOLKIT_SOURCE"
fi

echo "Skills sync complete."
