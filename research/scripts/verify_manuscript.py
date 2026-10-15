from pathlib import Path
import re,json,hashlib
P=Path(__file__).resolve().parents[2];s=(P/'china-capital-2026.tex').read_text()
body=s.split('\\mainmatter',1)[1].split('\\appendix',1)[0]
body=re.sub(r'(?<!\\)%[^\n]*','',body)
refs=set(re.findall(r'\\bibitem\{([^}]+)\}',s));used=set()
for x in re.findall(r'\\cite\{([^}]+)\}',s):used.update(x.split(','))
figuse=re.findall(r'\\Chart\{([^}]+)\}',s)
figdef=re.findall(r'\\csname chart@([^ ]+)\\endcsname\{',s)
chapters=re.findall(r'\\chapter\{([^}]+)\}',body)
report={'body_CJK_characters':sum('\u4e00'<=x<='\u9fff' for x in body),'total_CJK_characters':sum('\u4e00'<=x<='\u9fff' for x in s),'numbered_main_chapters':len(chapters),'chapter_names':chapters,'figure_count':len(figuse),'figure_names':figuse,'cited_sources':len(used),'missing_citations':sorted(used-refs),'missing_figures':sorted(set(figuse)-set(figdef)),'external_input_commands':re.findall(r'\\(?:input|include|includegraphics|bibliography)\b',s),'end_document_count':s.count('\\end{document}'),'source_sha256':hashlib.sha256(s.encode()).hexdigest()}
assert report['body_CJK_characters']>=30000,report
assert len(chapters)==12
assert len(figuse)==12 and len(set(figuse))==12
assert not report['missing_citations'] and not report['missing_figures']
assert not report['external_input_commands'] and report['end_document_count']==1
(P/'research'/'structural_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
