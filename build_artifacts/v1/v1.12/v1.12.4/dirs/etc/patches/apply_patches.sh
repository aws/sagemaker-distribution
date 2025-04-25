set -eux

# Patch files can be generated via "diff -u /path/to/original_file /path/to/new_file > XXX_bad_package.patch"
# See https://www.thegeekstuff.com/2014/12/patch-command-examples/
for PATCHFILE in /etc/patches/*.patch; do
    [ -f "$PATCHFILE" ] || continue
    echo "Applying $PATCHFILE"
    (cd "/opt/conda" && patch --strip=3 < "$PATCHFILE")
done
