"""Capture only this manuscript's PDF produced by the built-in editor.
No TeX compiler is invoked. File descriptors retain the native output while
its temporary directory is cleaned up. This does not change app settings.
"""
from pathlib import Path
import os,ctypes,struct,select,time,hashlib,json
import fitz
ROOTS=[p for p in (Path.home()/'.config/ChatGPT/latex',Path.home()/'.config/Codex/latex') if p.is_dir()]
SRC=Path(__file__).resolve().parents[2]/'china-capital-2026.tex'
OUT=SRC.with_suffix('.pdf'); expected=os.environ.get('EXPECTED_SOURCE_SHA') or hashlib.sha256(SRC.read_bytes()).hexdigest()
libc=ctypes.CDLL('libc.so.6',use_errno=True);fd=libc.inotify_init1(os.O_NONBLOCK)
assert fd>=0
watches={};opened={};mask=0x100|0x8|0x400

def watch(p):
 n=libc.inotify_add_watch(fd,str(p).encode(),mask)
 if n>=0:watches[n]=p

def open_pdf(p):
 try:
  source=p.parent/'document.tex'
  if hashlib.sha256(source.read_bytes()).hexdigest()!=expected:return
  f=os.open(p,os.O_RDONLY);opened[str(p)]=f
 except OSError:pass

def save_pdf(p):
 f=opened.get(str(p))
 if f is None:open_pdf(p);f=opened.get(str(p))
 if f is None:return False
 try:
  b=os.pread(f,os.fstat(f).st_size,0)
  if not b.startswith(b'%PDF') or b'%%EOF' not in b[-100:]:return False
  d=fitz.open(stream=b,filetype='pdf')
  if len(d)<10:return False
  out=OUT.with_suffix('.pdf.tmp');out.write_bytes(b);out.replace(OUT)
  record=dict(source_sha256=expected,pdf_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),pages=len(d),origin='native Codex LaTeX editor output; no separate PDF compilation')
  (SRC.parent/'research'/'native_pdf_export.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
  print(json.dumps(record,ensure_ascii=False),flush=True);return True
 except Exception:return False

for root in ROOTS:
 watch(root)
 for d in root.glob('preview-*'):
  if d.is_dir():watch(d)
print('Waiting for native PDF matching source '+expected,flush=True)
end=time.monotonic()+900
try:
 while time.monotonic()<end:
  ready=select.select([fd],[],[],1)[0]
  if not ready:continue
  b=os.read(fd,65536);off=0
  while off<len(b):
   wd,flag,cookie,n=struct.unpack_from('iIII',b,off);off+=16;name=b[off:off+n].split(b'\0',1)[0].decode(errors='replace');off+=n
   parent=watches.get(wd)
   if parent is None:continue
   p=parent/name
   if parent in ROOTS and flag&0x100 and name.startswith('preview-'):watch(p)
   elif name=='document.pdf':
    if flag&0x100:open_pdf(p)
    if flag&0x8 and save_pdf(p):raise SystemExit(0)
 print('No matching finished native PDF captured',flush=True)
finally:
 for f in opened.values():
  try:os.close(f)
  except OSError:pass
 os.close(fd)
