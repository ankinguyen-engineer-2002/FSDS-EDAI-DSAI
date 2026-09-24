#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
CLI=/Users/MAC/.codex/skills/archify/bin/archify.mjs

python3 scripts/generate_archify_specs.py
mkdir -p archify/rendered archify/receipts

for spec in archify/specs/*.json; do
  type=$(node -p "require('./$spec').diagram_type")
  name=$(basename "$spec" .json)
  node "$CLI" validate "$type" "$spec" --quality showcase --json >/dev/null
  node "$CLI" deliver "$type" "$spec" "archify/rendered/$name.html" \
    --quality showcase --json > "archify/receipts/$name-deliver.json"
  printf 'delivered %s\n' "$name"
done

./scripts/validate.sh
