#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

PY=".venv/bin/python3"
if [[ ! -x "$PY" ]]; then
  PY="python3"
fi

DRY_RUN=0
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=1
  shift
fi

message=${1:-"Update FSDS Academy Hub content"}

"$PY" -B scripts/glossary_scanner.py
"$PY" -B scripts/build_hub.py
"$PY" -B scripts/validate.py

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "DRY_RUN PASS: Full backend pipeline (Glossary -> Build -> Validate) succeeded."
  exit 0
fi

git add README.md FSDS-EDAI-DSAI-syllabus.md Prompt.md .gitignore .github/workflows/pages.yml \
  index.html fsds-learning-hub.html \
  content/lessons/ content/lessons-data.json content/glossary-data.json content/pictograms.json content/ascii-art/ content/arena-blueprints.json \
  assets/masks/ \
  supabase/schema.sql \
  scripts/ascii_diagram.py scripts/ascii_engine/ scripts/build_hub.py scripts/glossary_scanner.py scripts/publish.sh scripts/qa_runtime.py scripts/validate.py \
  scripts/arena_blueprints.py scripts/arena_module.py scripts/qa_arena_e2e.py

if git diff --cached -- index.html fsds-learning-hub.html content/ scripts/ supabase/ | grep -qE "AQ\.Ab8|AIza[0-9A-Za-z_-]{35}|ghp_[0-9A-Za-z]{36}|sk-[A-Za-z0-9]{32,}"; then
  echo "ERROR: Raw secret detected in staged changes! Aborting." >&2
  exit 1
fi

if git diff --cached --quiet; then
  echo "Nothing new staged to publish."
  exit 0
fi

git commit -m "$message"
git push origin HEAD:dev
printf '\nPushed to origin/dev (Production main remains untouched until explicitly merged).\n'
