#!/bin/bash
# Clones skills from repos listed in skills-manifest.json during Docker build.
set -eu

MANIFEST="${1:-/etc/sagemaker/skills/skills-manifest.json}"
DEST="${2:-/etc/sagemaker/skills}"
CLI_MANAGED_SKILL="aws-ai-ml"
CLI_METADATA_FILE=".aws-skill-metadata"

get_skill_metadata_version() {
    local skill_file="$1/SKILL.md"
    [ -f "$skill_file" ] || return 1

    awk '
        NR == 1 && $0 == "---" { in_frontmatter = 1; next }
        in_frontmatter && $0 == "---" { exit }
        in_frontmatter && /^metadata:[[:space:]]*$/ { in_metadata = 1; next }
        in_frontmatter && in_metadata && /^[^[:space:]]/ { in_metadata = 0 }
        in_frontmatter && in_metadata && /^[[:space:]]+version:[[:space:]]*/ {
            value = $0
            sub(/^[[:space:]]+version:[[:space:]]*/, "", value)
            gsub(/[[:space:]\"]/, "", value)
            print value
            exit
        }
    ' "$skill_file"
}

add_cli_metadata() {
    local skill_dir="$1"
    local skill_name="$2"
    local version

    # Only aws-ai-ml is currently backed by the Agent Toolkit catalog.
    if [ "$skill_name" != "$CLI_MANAGED_SKILL" ]; then
        return 0
    fi

    version=$(get_skill_metadata_version "$skill_dir") || true
    if [[ ! "$version" =~ ^[0-9]+$ ]]; then
        echo "Cannot add Agent Toolkit metadata for '$skill_name': valid numeric metadata.version not found" >&2
        return 1
    fi

    printf '{"version":"v%s"}\n' "$version" > "$skill_dir/$CLI_METADATA_FILE"
}

jq -c '.[]' "$MANIFEST" | while read -r entry; do
    repo=$(echo "$entry" | jq -r '.repo')
    spath=$(echo "$entry" | jq -r '.path')
    clone_dir=$(mktemp -d /tmp/sagemaker-skill-repo.XXXXXX)
    trap 'rm -rf "$clone_dir"' EXIT
    git clone --depth 1 "$repo" "$clone_dir"
    cp -r "$clone_dir/$spath"/* "$DEST"/
    rm -rf "$clone_dir"
    trap - EXIT
done

if [ -d "$DEST/$CLI_MANAGED_SKILL" ]; then
    add_cli_metadata "$DEST/$CLI_MANAGED_SKILL" "$CLI_MANAGED_SKILL"
fi
