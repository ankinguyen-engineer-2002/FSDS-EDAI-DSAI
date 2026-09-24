#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python3 scripts/embed_beginner_content.py --check
python3 - <<'PY'
import json
from pathlib import Path
guides = json.loads(Path('content/beginner-guides.json').read_text())
examples = json.loads(Path('content/term-examples.json').read_text())
expected = {'F01': 5, 'F02': 5, 'F03': 9}
required = {'question','plain','analogy','analogyLimit','why','place','flow','visualLook','sayBack','job','bridge','stress','response'}
hero_required = {'kicker','title','dek','scenario','analogy','outcomes','path','metaphorWorld','metaphorMap'}
map_required = {'technical','physical','role'}
for code, count in expected.items():
    lesson = guides.get(code)
    if not lesson or len(lesson.get('chapters', {})) != count:
        raise SystemExit(f'Beginner guide chapter mismatch: {code}')
    hero = lesson.get('hero', {})
    missing_hero = hero_required - hero.keys()
    if missing_hero:
        raise SystemExit(f'Missing pain/metaphor fields: {code}: {sorted(missing_hero)}')
    if len(hero.get('metaphorMap', [])) < 5:
        raise SystemExit(f'Living metaphor needs at least 5 core mappings: {code}')
    technical_names = set()
    for index, item in enumerate(hero['metaphorMap'], 1):
        missing_map = map_required - item.keys()
        if missing_map or any(not str(item.get(key, '')).strip() for key in map_required):
            raise SystemExit(f'Incomplete metaphor mapping: {code}/row-{index}')
        if item['technical'] in technical_names:
            raise SystemExit(f'Duplicate metaphor technical term: {code}/{item["technical"]}')
        technical_names.add(item['technical'])
    final = lesson.get('final', {})
    if not str(final.get('golden', '')).strip():
        raise SystemExit(f'Missing one-line golden takeaway: {code}')
    if len(final.get('checks', [])) != 5:
        raise SystemExit(f'Expected exactly 5 final self-checks: {code}')
    for chapter_id, chapter in lesson['chapters'].items():
        missing = required - chapter.keys()
        if missing:
            raise SystemExit(f'Missing beginner guide fields: {code}/{chapter_id}: {sorted(missing)}')
        if any(not str(chapter.get(key, '')).strip() for key in required):
            raise SystemExit(f'Empty beginner guide field: {code}/{chapter_id}')
        if not str(chapter.get('heading', '')).strip() or not str(chapter.get('headingLead', '')).strip():
            raise SystemExit(f'Missing plain-first chapter heading: {code}/{chapter_id}')
        for item in chapter.get('terms', []):
            if item['term'] not in examples:
                raise SystemExit(f'Missing term example: {item["term"]}')
mechanisms = json.loads(Path('content/lesson-mechanisms.json').read_text())
scene_count = sum(len(chapter.get('scenes', [])) for lesson in mechanisms.values() for chapter in lesson['chapters'])
if scene_count != 27:
    raise SystemExit(f'Expected 27 mechanism scenes, found {scene_count}')
core_count = 0
for code, lesson in guides.items():
    mechanism_chapters = {chapter['id']: chapter for chapter in mechanisms[code]['chapters']}
    for chapter_id, guide in lesson['chapters'].items():
        scenes = mechanism_chapters[chapter_id].get('scenes', [])
        glossary_items = {
            item['term']: item
            for scene in scenes
            for item in (scene.get('glossary') or [])
        }
        for term in guide.get('coreTerms', []):
            core_count += 1
            if term not in glossary_items:
                raise SystemExit(f'Core term has no glossary definition: {code}/{chapter_id}/{term}')
            if term not in examples:
                raise SystemExit(f'Core term has no practical example: {code}/{chapter_id}/{term}')
            needle = term.lower().split(' / ')[0]
            has_step_mechanism = any(
                needle in f"{step.get('term', '')} {step.get('say', '')} {step.get('mechanism', '')}".lower()
                for scene in scenes
                for step in scene.get('steps', [])
            )
            has_explicit_purpose = bool(str(glossary_items[term].get('purpose', '')).strip())
            if not has_step_mechanism and not has_explicit_purpose:
                raise SystemExit(f'Core term has no explicit mechanism: {code}/{chapter_id}/{term}')
if core_count != 107:
    raise SystemExit(f'Expected 107 deliberately selected core term cards, found {core_count}')
if len(examples) < 182:
    raise SystemExit(f'Expected at least 182 practical term examples, found {len(examples)}')
method = Path('LEARNING-DESIGN-METHOD.md')
if not method.exists():
    raise SystemExit('Missing the single learning-design rule.')
renderer = Path('content/beginner-renderer.js').read_text()
for label in ('I · Cơn đau nguyên bản', 'II · Bản đồ quy đổi ẩn dụ', 'III · ', 'IV · Bản chất 1 dòng'):
    if label not in renderer:
        raise SystemExit(f'Missing required four-part learning structure: {label}')
print(f'PASS: four-part learning rule, 27 scenes, 19 chapters, 3 living metaphors, 19 stress tests, {core_count} core term cards with explicit mechanisms, 3 golden takeaways and {len(examples)} example-bank entries.')
PY

python3 - <<'PY'
from pathlib import Path
s = Path('fsds-learning-hub.html').read_text()
Path('/tmp/fsds-learning-hub.js').write_text(s.split('<script>', 1)[1].rsplit('</script>', 1)[0])
PY
node --check /tmp/fsds-learning-hub.js

printf '%s  %s\n' \
  '9bfb70bf96004ac694b4ed902e634d029df9cc3b0ca50ce06d0608d29afa6d37' \
  'archify/brand-assets/linux-kernel-org.png' | shasum -a 256 -c -

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
