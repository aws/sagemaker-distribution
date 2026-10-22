#!/bin/bash
# Clones skills from repos listed in skills-manifest.json during Docker build.
set -eu

MANIFEST="/etc/sagemaker/skills/skills-manifest.json"
DEST="/etc/sagemaker/skills"

jq -c '.[]' "$MANIFEST" | while read -r entry; do
    repo=$(echo "$entry" | jq -r '.repo')
    spath=$(echo "$entry" | jq -r '.path')
    git clone --depth 1 "$repo" /tmp/skill-repo
    cp -r "/tmp/skill-repo/$spath"/* "$DEST"/
    rm -rf /tmp/skill-repo
done
