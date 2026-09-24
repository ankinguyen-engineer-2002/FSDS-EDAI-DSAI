# Archify visual labs — 44/44

## Source of truth

- `specs/*.json`: 44 editable diagram specifications — source of truth.
- `rendered/*.html`: 44 deterministic artifacts produced by Archify `deliver`.
- `receipts/*-deliver.json`: SHA-256 and validation receipts.
- `receipts/*-visual-check.json`: packaged browser evidence for containment, readability, theme and viewer chrome; current F04 artifacts pass.
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

- `python`, `postgresql` và `fastapi` dùng canonical vector trong catalogue Archify.
- Linux/Tux được capture từ website chính thức `kernel.org`, khóa bằng SHA-256 trong spec, rồi embed vào artifact; bản PNG audit nằm tại `brand-assets/linux-kernel-org.png`.
- GraphQL và gRPC trong F04 được capture từ website chính thức `graphql.org` và `grpc.io`, pin SHA-256 trực tiếp trong `api-contract-styles-architecture.json`.
- Artifact đã deliver không fetch logo khi người học mở bài. Không dùng icon gần giống, logo không rõ nguồn hoặc URL chưa pin digest.
