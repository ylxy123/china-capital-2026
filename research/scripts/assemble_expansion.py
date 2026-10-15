from pathlib import Path
import re,json,csv,hashlib
ROOT=Path(__file__).resolve().parents[2]; R=ROOT/'research'/'expansion'
s=(R/'baseline-source.txt').read_text(); baseline=json.loads((R/'baseline-paragraphs.json').read_text()); additions={}
for f in sorted(R.glob('notes-*.txt')):
 for m in re.finditer(r'^@@(P\d{3})\s*\n(.*?)(?=^@@P\d{3}|\Z)',f.read_text(),re.M|re.S):
  if m[1] in additions:raise ValueError('Duplicate '+m[1])
  additions[m[1]]=m[2].strip()
fixes=json.loads((R/'paragraph-corrections.json').read_text()) if (R/'paragraph-corrections.json').exists() else {}
maprows=[]
for row in baseline:
 old=row['original']; anchor=row['id']; body=fixes.get(anchor,old)
 assert s.count(old)==1,anchor
 extra=additions.get(anchor,'')
 replacement=body+'\n\n% ARGUMENT '+anchor+'\n\\phantomsection\\label{arg:'+anchor+'}\n'+extra if extra else body
 s=s.replace(old,replacement,1)
 maprows.append({'paragraph_id':anchor,'chapter':row['chapter'],'section':row['section'],'original_sha256':row['source_sha256'],'destination_label':'arg:'+anchor if extra else '', 'new_CJK_characters':len(re.findall(r'[\u4e00-\u9fff]',extra)),'status':'expanded_and_corrected' if extra and anchor in fixes else 'expanded' if extra else 'pending','original_text':old})
refs=json.loads((R/'added-sources.json').read_text()) if (R/'added-sources.json').exists() else []
items=[]
for r in refs:
 esc=lambda x:str(x).replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
 items.append(r'\bibitem{'+r['id']+'} '+esc(r['author'])+'. '+esc(r['title'])+'. '+esc(r['year'])+'. '+esc(r['locator'])+r'。\href{\detokenize{'+r['url']+r'}}{原始来源}。复核：'+r.get('checked','2026-10-15')+'。')
s=s.replace('\\end{thebibliography}','\n'.join(items)+'\n\\end{thebibliography}')
s=s.replace('原创研究专论\\quad 第一版','原创研究专论\\quad 扩充修订版')
if (R/'extra-appendix.txt').exists():s=s.replace('% BIBLIOGRAPHY_BEGIN',(R/'extra-appendix.txt').read_text()+'\n% BIBLIOGRAPHY_BEGIN')
if (R/'global-replacements.json').exists():
 for a,b in json.loads((R/'global-replacements.json').read_text()):
  if a not in s:raise ValueError('Replacement missing: '+a[:80])
  s=s.replace(a,b)
(ROOT/'china-capital-2026.tex').write_text(s)
for r in maprows:
 marker='\\label{'+r['destination_label']+'}'
 r['destination_line']=s[:s.index(marker)].count('\n')+1 if r['destination_label'] else ''
with (R/'paragraph-map.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(maprows[0]));w.writeheader();w.writerows(maprows)
b=s.split('\\mainmatter',1)[1].split('\\appendix',1)[0]
b=re.sub(r'(?m)^%[^\n]*','',b)
report={'source_sha256':hashlib.sha256(s.encode()).hexdigest(),'baseline_paragraphs':len(baseline),'expanded_paragraphs':len(additions),'pending':[r['paragraph_id'] for r in maprows if r['status']=='pending'],'body_CJK_including_headings_and_captions':len(re.findall(r'[\u4e00-\u9fff]',b))}
(R/'progress.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='pending'},ensure_ascii=False))
