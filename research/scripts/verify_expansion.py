"""Validate the expanded manuscript; count prose independently of TeX markup."""
from pathlib import Path
from collections import Counter
import re, json, hashlib, csv

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / 'china-capital-2026.tex').read_text()
body = source.split('\\mainmatter', 1)[1].split('\\appendix', 1)[0]

def cjk(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))

def without_command(text, name, count):
    pattern = re.compile(r'\\' + re.escape(name) + r'(?![A-Za-z])\*?')
    pos = 0
    pieces = []
    while match := pattern.search(text, pos):
        pieces.append(text[pos:match.start()])
        end = match.end()
        for _ in range(count):
            while end < len(text) and text[end].isspace():
                end += 1
            if end >= len(text) or text[end] != '{':
                raise ValueError('Missing argument for ' + name)
            depth = 1
            end += 1
            while end < len(text) and depth:
                char = text[end]
                escaped = end > 0 and text[end - 1] == '\\'
                if not escaped:
                    depth += (char == '{') - (char == '}')
                end += 1
            if depth:
                raise ValueError('Unbalanced argument for ' + name)
        pos = end
    pieces.append(text[pos:])
    return ''.join(pieces)

def narrative(text):
    text = re.sub(r'(?<!\\)%[^\n]*', '', text)
    for env in ('longtable', 'table', 'figure', 'tikzpicture', 'axis', 'tabular', 'verbatim'):
        text = re.sub(r'\\begin\{' + env + r'\}.*?\\end\{' + env + r'\}', '', text, flags=re.S)
    for name, argc in [('Chart',3),('addcontentsline',3),('chapter',1),('section',1),('subsection',1),
                       ('caption',1),('cite',1),('label',1),('ref',1),('pageref',1)]:
        text = without_command(text, name, argc)
    text = re.sub(r'\\\[.*?\\\]', '', text, flags=re.S)
    text = re.sub(r'(?<!\\)\$.*?(?<!\\)\$', '', text, flags=re.S)
    return text

prose = narrative(body)
refs = re.findall(r'\\bibitem\{([^}]+)\}', source)
used = {key for group in re.findall(r'\\cite\{([^}]+)\}', source) for key in group.split(',')}
figuse = re.findall(r'\\Chart\{([^}]+)\}', source)
figdef = re.findall(r'\\csname chart@([^ ]+)\\endcsname\{', source)
chapters = re.findall(r'\\chapter\{([^}]+)\}', body)
labels = re.findall(r'\\label\{([^}]+)\}', source)
crossrefs = re.findall(r'\\(?:ref|pageref)\{([^}]+)\}', source)
mapping = list(csv.DictReader((ROOT/'research/expansion/paragraph-map.csv').open(encoding='utf-8-sig')))
per_chapter = []
for match in re.finditer(r'\\chapter\*?\{([^}]+)\}(.*?)(?=\\chapter|\Z)', body, re.S):
    per_chapter.append({'chapter':match[1], 'narrative_CJK':cjk(narrative(match[2]))})
paragraphs = [re.sub(r'\s+', '', p) for p in prose.split('\n\n') if cjk(p) >= 100]
duplicates = [{'count':n,'preview':p[:100]} for p,n in Counter(paragraphs).items() if n > 1]
stack = []
for action, env in re.findall(r'\\(begin|end)\{([^}]+)\}', source):
    if action == 'begin':
        stack.append(env)
    else:
        assert stack and stack.pop() == env, ('environment mismatch', env)
assert not stack
report = {
    'body_CJK_characters':cjk(prose),
    'count_definition':'Narrative Han characters only; excludes headings, tables, figures/captions, labels, citations, math, code, frontmatter, appendices and bibliography.',
    'body_CJK_including_headings_tables_captions':cjk(re.sub(r'(?<!\\)%[^\n]*','',body)),
    'total_CJK_characters':cjk(source), 'numbered_main_chapters':len(chapters),
    'per_chapter':per_chapter, 'figure_count':len(figuse), 'figure_names':figuse,
    'cited_sources':len(used), 'bibliography_entries':len(refs),
    'missing_citations':sorted(used-set(refs)), 'uncited_entries':sorted(set(refs)-used),
    'missing_figures':sorted(set(figuse)-set(figdef)),
    'missing_crossrefs':sorted(set(crossrefs)-set(labels)),
    'duplicate_labels':sorted(k for k,n in Counter(labels).items() if n > 1),
    'duplicate_bibliography_keys':sorted(k for k,n in Counter(refs).items() if n > 1),
    'baseline_paragraphs':len(mapping),
    'mapped_paragraphs':sum(x['status'] in ('expanded','expanded_and_corrected') for x in mapping),
    'pending_paragraphs':[x['paragraph_id'] for x in mapping if not x['destination_label']],
    'duplicate_long_narrative_paragraphs':duplicates,
    'external_input_commands':re.findall(r'\\(?:input|include|includegraphics|bibliography)\b',source),
    'source_sha256':hashlib.sha256(source.encode()).hexdigest()
}
assert 100000 <= report['body_CJK_characters'] <= 150000, report['body_CJK_characters']
assert len(chapters) == 12
assert len(figuse) == len(set(figuse)) == 12
assert len(mapping) == report['mapped_paragraphs'] == 291
assert all(x['destination_label'] in labels for x in mapping)
assert all(int(x['new_CJK_characters']) >= 100 for x in mapping)
for key in ['missing_citations','missing_figures','missing_crossrefs','duplicate_labels',
            'duplicate_bibliography_keys','external_input_commands','pending_paragraphs',
            'duplicate_long_narrative_paragraphs']:
    assert not report[key], (key,report[key])
assert '\\Chart{wid}' not in source
assert 'pdfauthor={姚林翔宇}' in source
assert source.count('\\end{document}') == 1
(ROOT/'research/structural_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report, ensure_ascii=False, indent=2))
