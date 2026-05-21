#!/usr/bin/env bash
# Package the netguardir.com site for upload.
#
# Produces:
#   build/netguardir-site.zip      ← drag this into Porkbun's static-hosting file manager
#   build/netguardir-site.tar.gz   ← if you prefer tar (SFTP / scp deploy)
#
# Run from the netguardir.com/ directory.

set -euo pipefail

cd "$(dirname "$0")"

mkdir -p build

# Include everything except dev artifacts
INCLUDE=(
    "index.html"
    "assets"
    "docs"
    "downloads"
)

EXCLUDE_OPTS=(
    --exclude='.git'
    --exclude='build'
    --exclude='*.swp'
    --exclude='.DS_Store'
)

echo "→ Packaging site …"
zip -r build/netguardir-site.zip "${INCLUDE[@]}" -x '.git/*' 'build/*' '*.swp' '.DS_Store' >/dev/null
tar -czf build/netguardir-site.tar.gz "${EXCLUDE_OPTS[@]}" "${INCLUDE[@]}"

echo
echo "  zip:    $(du -h build/netguardir-site.zip   | cut -f1)  ($(unzip -l build/netguardir-site.zip   | tail -1 | awk '{print $2}') files)"
echo "  tar.gz: $(du -h build/netguardir-site.tar.gz| cut -f1)"
echo
echo "Upload paths:"
echo "  1. Porkbun static hosting (web UI):"
echo "       Porkbun dashboard → netguardir.com → Static Hosting → upload netguardir-site.zip → Extract"
echo "  2. External hosting + Porkbun DNS:"
echo "       SCP build/netguardir-site.tar.gz to your web host, extract under the document root."
echo "       Use ./porkbun_dns.py to point the A/CNAME records via Porkbun's API."
