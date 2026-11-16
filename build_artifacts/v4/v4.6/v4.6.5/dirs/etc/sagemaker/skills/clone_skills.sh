#!/bin/bash
# Clones skills from repos listed in skills-manifest.json during Docker build.
set -eu

MANIFEST="/etc/sagemaker/skills/skills-manifest.json"
DEST="/etc/sagemaker/skills"

jq -c '.[]' "$MANIFEST" | while read -r entry; do
    repo=$(echo "$entry" | jq -r '.repo')
    spath=$(echo "$entry" | jq -r '.path')
    skill_name=$(basename "$spath")
    git clone --depth 1 "$repo" /tmp/skill-repo
    # Copy the skill directory itself into DEST. Clear any pre-existing target
    # first so a repeat copy can't nest it as DEST/<skill>/<skill>.
    rm -rf "${DEST:?}/$skill_name"
    cp -r "/tmp/skill-repo/$spath" "$DEST/"
    rm -rf /tmp/skill-repo
done
