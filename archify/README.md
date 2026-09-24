# Archify visual labs — 35/35

## Source of truth

- `specs/*.json`: 35 editable diagram specifications — source of truth.
- `rendered/*.html`: 35 deterministic artifacts produced by Archify `deliver`.
- `receipts/*-deliver.json`: SHA-256 and validation receipts.
- `receipts/*-visual-check.json`: failed packaged browser-check attempts retained for transparency; failure reason was Chrome `SIGABRT` in the execution environment.
- `receipts/MANUAL-BROWSER-QA.md`: supplementary Playwright/browser and perceptual QA.

## Rebuild one artifact

```bash
TYPE=architecture
NAME=linux-command-architecture
node /Users/MAC/.codex/skills/archify/bin/archify.mjs validate "$TYPE" "archify/specs/$NAME.json" --quality showcase --json
node /Users/MAC/.codex/skills/archify/bin/archify.mjs deliver "$TYPE" "archify/specs/$NAME.json" "archify/rendered/$NAME.html" --quality showcase --json
```

Do not hand-edit `rendered/*.html`. Edit the JSON spec, validate, then deliver again.

## Rebuild toàn bộ catalog

```bash
./scripts/rebuild-archify.sh
```

Generator `scripts/generate_archify_specs.py` quản lý 26 spec bổ sung; chín spec ban đầu vẫn là hand-authored source. Sau generate, mọi spec đều phải pass `showcase` validation và được deliver lại trước khi commit.

## Brand marks

Các mark `python`, `postgresql` và `fastapi` dùng catalogue vector được Archify bundle/pin nên artifact không fetch logo khi mở. Catalogue hiện chưa có canonical Linux/Tux mark; không dùng icon không rõ nguồn để thay thế.
