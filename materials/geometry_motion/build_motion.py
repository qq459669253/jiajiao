"""Build a single offline HTML file, without external scripts or styles."""
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parent
text=(ROOT/'template.html').read_text(encoding='utf-8')
for marker,name in [('/*__GEOMETRY__*/','geometry.js'),('/*__APP__*/','app.js')]:
    text=text.replace(marker,(ROOT/name).read_text(encoding='utf-8'))
(ROOT/'index.html').write_text(text,encoding='utf-8')
with zipfile.ZipFile(ROOT/'geometry_motion.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['index.html','README.md','geometry.js','app.js','template.html','build_motion.py','verify_motion.py','render_preview.py','LICENSE','question4_rotation.gif']:
        p=ROOT/name
        if p.exists():z.write(p,p.name)
print('Built index.html and geometry_motion.zip')
