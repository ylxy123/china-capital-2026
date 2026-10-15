from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];p=R.parent/'china-capital-2026.tex'
s=p.read_text();registry={x['id']:x for x in json.loads((R/'sources/source_index.json').read_text())}
keys=[]
for group in re.findall(r'\\cite\{([^}]+)\}',s):
 for k in group.split(','):
  if k not in keys:keys.append(k)
missing=set(keys)-registry.keys();assert not missing,missing
def escape(v):
 for a,b in [('&',r'\&'),('%',r'\%'),('_',r'\_'),('#',r'\#')]:v=v.replace(a,b)
 return v
lines=[r'\backmatter',r'\renewcommand{\bibname}{参考文献与数据来源}',r'\cleardoublepage\phantomsection',r'\addcontentsline{toc}{chapter}{参考文献与数据来源}',r'\begin{thebibliography}{99}',r'\small\sloppy']
for k in keys:
 z=registry[k]
 lines.append(r'\bibitem{'+k+'} '+escape(z['author'])+'. '+escape(z['title'])+'. '+str(z['year'])+'. '+escape(z['locator'])+r'。\href{\detokenize{'+z['url']+r'}}{原始来源}。访问：2026-10-14。')
lines.append(r'\end{thebibliography}')
block='% BIBLIOGRAPHY_BEGIN\n'+'\n\n'.join(lines)+'\n% BIBLIOGRAPHY_END\n'
if '% BIBLIOGRAPHY_BEGIN' in s:s=re.sub(r'% BIBLIOGRAPHY_BEGIN.*?% BIBLIOGRAPHY_END\n',lambda m:block,s,flags=re.S)
else:s=s.rsplit('\\end{document}',1)[0]+block+'\n\\end{document}\n'
p.write_text(s);print('Citations resolved:',len(keys))
