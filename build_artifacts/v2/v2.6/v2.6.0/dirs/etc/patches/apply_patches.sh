#!/bin/bash

set -eux

# Check if parameter is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 [smus|studio-ai]"
    exit 1
fi

# Validate parameter
case "$1" in
    "smus")
        PATCH_DIR="/etc/patches/smus"
        ;;
    "studio-ai")
        PATCH_DIR="/etc/patches/studio-ai"
        ;;
    *)
        echo "Error: Parameter must be either 'smus' or 'studio-ai'"
        exit 1
        ;;
esac

# Check if patch directory exists
if [ ! -d "$PATCH_DIR" ]; then
    echo "Error: Patch directory $PATCH_DIR does not exist"
    exit 1
fi

# Patch files can be generated via "diff -u /path/to/original_file /path/to/new_file > XXX_bad_package.patch"
# See https://www.thegeekstuff.com/2014/12/patch-command-examples/
for PATCHFILE in "$PATCH_DIR"/*.patch; do
    [ -f "$PATCHFILE" ] || continue
    echo "Applying $PATCHFILE"
    (cd "/opt/conda" && patch --strip=3 < "$PATCHFILE")
done
