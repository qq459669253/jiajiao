"""Build a single offline HTML file, without external scripts or styles."""
from pathlib import Path
import zipfile
import base64
import re

ROOT=Path(__file__).resolve().parent
text=(ROOT/'template.html').read_text(encoding='utf-8')
poster=base64.b64encode((ROOT/'static_preview.png').read_bytes()).decode('ascii')
text=text.replace('__STATIC_PREVIEW__','data:image/png;base64,'+poster)
text=re.sub(r'<(button|input|select)\b',r'<\1 disabled data-runtime-control',text)
for marker,name in [('/*__GEOMETRY__*/','geometry.js'),('/*__APP__*/','app.js')]:
    text=text.replace(marker,(ROOT/name).read_text(encoding='utf-8'))
(ROOT/'index.html').write_text(text,encoding='utf-8')
with zipfile.ZipFile(ROOT/'geometry_motion.zip','w',zipfile.ZIP_DEFLATED) as z:
    # This is the ready-to-open package; source files remain in the repository.
    # Do not include template.html, which is not a working standalone app.
    for name in ['index.html','README.md','LICENSE','question4_rotation.gif']:
        p=ROOT/name
        if p.exists():z.write(p,p.name)
print('Built index.html and geometry_motion.zip')
