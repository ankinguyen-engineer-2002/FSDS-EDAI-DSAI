#!/usr/bin/env python3
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / 'fsds-learning-hub.html'
CSS = ROOT / 'content/beginner-layout.css'
GUIDES = ROOT / 'content/beginner-guides.json'
TERMS = ROOT / 'content/term-examples.json'
RENDERER = ROOT / 'content/beginner-renderer.js'
MECHANISMS = ROOT / 'content/lesson-mechanisms.json'
CSS_START = '    /* BEGIN BEGINNER_LAYOUT */'
CSS_END = '    /* END BEGINNER_LAYOUT */'
LESSONS_START = '/* BEGIN LESSON_MECHANISMS */'
LESSONS_END = '/* END LESSON_MECHANISMS */'
JS_START = '/* BEGIN BEGINNER_CONTENT */'
JS_END = '/* END BEGINNER_CONTENT */'

def replace_block(source: str, start: str, end: str, block: str, insertion: str) -> str:
    if start in source:
        before, rest = source.split(start, 1)
        _, after = rest.split(end, 1)
        return before + block + after
    if insertion not in source:
        raise SystemExit(f'Insertion marker not found: {insertion!r}')
    return source.replace(insertion, block + '\n' + insertion, 1)

def build() -> str:
    source = HTML.read_text()
    css = CSS.read_text().rstrip()
    css_block = f'{CSS_START}\n' + '\n'.join('    ' + line if line else '' for line in css.splitlines()) + f'\n{CSS_END}'
    source = replace_block(source, CSS_START, CSS_END, css_block, '  </style>')

    if 'function renderLegacyPlainStudyNote(topic)' not in source:
        source = source.replace('function renderPlainStudyNote(topic) {', 'function renderLegacyPlainStudyNote(topic) {', 1)
    source = source.replace("else if (topic.code === 'F03') renderDatabaseArticle(topic);", "else if (topic.code === 'F03') renderPlainStudyNote(topic);")

    mechanisms = json.dumps(json.loads(MECHANISMS.read_text()), ensure_ascii=False, indent=2)
    lessons_block = f'{LESSONS_START}\nconst lessons = {mechanisms};\n{LESSONS_END}'
    if LESSONS_START in source:
        source = replace_block(source, LESSONS_START, LESSONS_END, lessons_block, 'function visualTemplate(topic) {')
    else:
        start = source.index('const lessons = {')
        end = source.index('\n};\n\nfunction visualTemplate(topic) {', start) + 3
        source = source[:start] + lessons_block + source[end:]

    guides = json.dumps(json.loads(GUIDES.read_text()), ensure_ascii=False, indent=2)
    terms = json.dumps(json.loads(TERMS.read_text()), ensure_ascii=False, indent=2)
    renderer = RENDERER.read_text().rstrip()
    js_block = f'{JS_START}\nconst beginnerGuides = {guides};\nconst termExamples = {terms};\n\n{renderer}\n{JS_END}'
    source = replace_block(source, JS_START, JS_END, js_block, 'function renderLegacyPlainStudyNote(topic) {')
    return source

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    built = build()
    current = HTML.read_text()
    if args.check:
        if built != current:
            raise SystemExit('Embedded beginner content is stale. Run scripts/embed_beginner_content.py')
        print('PASS: beginner guides, glossary examples, renderer and CSS are embedded.')
    else:
        HTML.write_text(built)
        print('Embedded beginner-first content into fsds-learning-hub.html')

if __name__ == '__main__':
    main()
