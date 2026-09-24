#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - <<'PY'
from pathlib import Path
s = Path('fsds-learning-hub.html').read_text()
Path('/tmp/fsds-learning-hub.js').write_text(s.split('<script>', 1)[1].rsplit('</script>', 1)[0])
PY
node --check /tmp/fsds-learning-hub.js

python3 - <<'PY'
import hashlib, json, subprocess, sys
from pathlib import Path
cli = '/Users/MAC/.codex/skills/archify/bin/archify.mjs'
specs = sorted(Path('archify/specs').glob('*.json'))
if len(specs) != 35:
    raise SystemExit(f'Expected 35 Archify specs, found {len(specs)}')
for path in specs:
    spec = json.loads(path.read_text())
    cp = subprocess.run(
        ['node', cli, 'validate', spec['diagram_type'], str(path), '--quality', 'showcase', '--json'],
        capture_output=True, text=True
    )
    if cp.returncode:
        print(cp.stdout or cp.stderr)
        raise SystemExit(f'Archify validation failed: {path}')
    name = path.stem
    artifact = Path('archify/rendered') / f'{name}.html'
    receipt_path = Path('archify/receipts') / f'{name}-deliver.json'
    if not artifact.exists() or not receipt_path.exists():
        raise SystemExit(f'Missing delivered artifact/receipt for {name}')
    receipt = json.loads(receipt_path.read_text())
    actual_spec = hashlib.sha256(path.read_bytes()).hexdigest()
    actual_artifact = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if receipt['specification']['sha256'] != actual_spec:
        raise SystemExit(f'Spec changed after delivery: {name}')
    if receipt['artifact']['sha256'] != actual_artifact:
        raise SystemExit(f'Artifact hash mismatch: {name}')
print('PASS: JS syntax, 35/35 showcase specs, receipts and artifact hashes.')
PY
