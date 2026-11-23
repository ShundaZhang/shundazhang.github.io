"""Local integrity checks and synthetic pulse-inspector tests. No hardware access."""
from pathlib import Path
from html.parser import HTMLParser
import importlib.util
import xml.etree.ElementTree as ET
import tempfile
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
SITE = ROOT.parent
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.urls=[];self.images=[];self.sections=[]
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if 'id' in d:self.ids.append(d['id'])
  if tag=='a' and 'href' in d:self.urls.append(d['href'])
  if tag=='img':
   assert d.get('alt'), 'image missing alt'
   self.urls.append(d['src']);self.images.append(d['src'])
  if tag=='section':self.sections.append(d.get('id'))
for name in ('index.html','index.zh.html'):
 page=Page();page.feed((ROOT/name).read_text())
 assert len(page.ids)==len(set(page.ids)), 'duplicate IDs'
 assert len(page.sections)==12
 assert len(page.images)==19
 for url in page.urls:
  if url.startswith(('https://','http://','mailto:')):continue
  path,_,anchor=url.partition('#')
  if path.startswith('/'):target=SITE/path.lstrip('/')
  else:target=(ROOT/path).resolve()
  if target.is_dir():target=target/'index.html'
  assert target.exists(), (name,url)
  if anchor and not path:assert anchor in page.ids,(name,anchor)
 print(name,'12 chapters, 19 images, local links and anchors PASS')
for f in (ROOT/'assets').glob('*.svg'):ET.parse(f)
print('SVG XML integrity PASS')
# Regression coverage for the overview's cramped NFC card and short connector.
for filename in ('map.svg','map.zh.svg'):
 tree=ET.parse(ROOT/'assets'/filename);ns={'s':'http://www.w3.org/2000/svg'}
 texts=tree.findall('.//s:text',ns)
 titles=[x for x in texts if x.text=='NFC / LF RFID']
 assert len(titles)==1, 'NFC title must remain on one line'
 details=[x for x in texts if x.text in ('13.56 MHz / 125 kHz','13.56 MHz /','125 kHz')]
 assert details and min(float(x.attrib['y']) for x in details)-float(titles[0].attrib['y'])>=35
 lines=[x for x in tree.findall('.//s:g/s:path',ns) if 'marker-end' in x.attrib]
 assert len(lines)==6
 import re,math
 for line in lines:
  x1,y1,x2,y2=map(float,re.findall(r'-?\d+(?:\.\d+)?',line.attrib['d']))
  assert math.hypot(x2-x1,y2-y1)>=50, 'connector needs visible shaft and arrowhead'
  assert all(0<v<1000 for v in (x1,x2)) and all(0<v<610 for v in (y1,y2))
print('Overview title spacing and six full connectors PASS')

with zipfile.ZipFile(ROOT/'downloads/bit-lab-source.zip') as z:
 assert z.testzip() is None
 for f in ('application.fam','bit_lab.c','README.md'):
  assert z.read('bit_lab/'+f)==(ROOT/'downloads/bit_lab'/f).read_bytes()
print('Download ZIP matches source PASS')
spec=importlib.util.spec_from_file_location('pulse',ROOT/'downloads/pulse_inspect.py')
pulse=importlib.util.module_from_spec(spec);spec.loader.exec_module(pulse)
r,pulses=pulse.inspect(ROOT/'downloads/synthetic.sub')
assert r['pulse_count']==24 and r['candidate_gaps']==3
assert r['total_duration_us']==37495
assert r['histogram_100us']=={300:9,900:12}
with tempfile.TemporaryDirectory() as tmp:
 out=Path(tmp)/'pulses.svg';pulse.svg(pulses,out);ET.parse(out)
 bad=Path(tmp)/'bad.sub';bad.write_text('Filetype: other\nProtocol: RAW\nRAW_Data: 300 -900')
 p=subprocess.run([sys.executable,str(ROOT/'downloads/pulse_inspect.py'),str(bad)],capture_output=True,text=True)
 assert p.returncode==2 and 'Expected Flipper' in p.stderr
 try:pulse.inspect(ROOT/'downloads/synthetic.sub',0)
 except ValueError:pass
 else:raise AssertionError('invalid threshold accepted')
print('Synthetic pulse stats, SVG output and rejection paths PASS')
for name in ('index.html','index.zh.html'):
 page=Page();page.feed((SITE/name).read_text())
 links=[x for x in page.urls if '/flipper-zero-lab/' in x]
 assert len(links)==1
 assert '<span class="entry-number">18</span>' in (SITE/name).read_text()
print('Bilingual homepage entry PASS')
