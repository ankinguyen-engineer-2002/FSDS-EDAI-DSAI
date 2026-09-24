#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

message=${1:-"Update learning hub"}
./scripts/validate.sh

git add -A
if git diff --cached --quiet; then
  echo "Nothing to publish."
  exit 0
fi

git commit -m "$message"
git push origin main
printf '\nPushed to main. GitHub Pages deployment now follows automatically.\n'
