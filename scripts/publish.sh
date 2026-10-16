#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

message=${1:-"Update FSDS study hub content"}

python3 -B scripts/build_hub.py
python3 -B scripts/validate.py

git add README.md FSDS-EDAI-DSAI-syllabus.md prompt.md .gitignore .github/workflows/pages.yml fsds-learning-hub.html content/lessons-data.json content/glossary-data.json assets/visuals/ scripts/ascii_diagram.py scripts/build_hub.py scripts/glossary_scanner.py scripts/publish.sh scripts/validate.py scripts/verify_pictures.py
if git diff --cached --quiet; then
  echo "Nothing new staged to publish."
  exit 0
fi

git commit -m "$message"
git push origin main
printf '\nPushed to main. GitHub Pages deployment triggered.\n'
