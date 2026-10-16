"""Render the actual interactive SVG into an animated GIF.

Optional development dependencies: playwright, pillow, Chromium.
No dependencies are needed to open the finished HTML file.
"""
from pathlib import Path
from io import BytesIO
import shutil
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parent


def render():
    frames=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1150,'height':1000})
        page.set_content((ROOT/'index.html').read_text(encoding='utf-8'))
        for angle in range(0,360,5):
            page.evaluate('angle=>mathMotion.setValue(angle)',angle)
            frames.append(Image.open(BytesIO(page.locator('#scene').screenshot())).convert('RGB'))
        browser.close()
    palette=frames[0].quantize(colors=96)
    frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    frames[0].save(ROOT/'question4_rotation.gif',save_all=True,append_images=frames[1:],duration=140,loop=0,optimize=True,disposal=2)
    print('Rendered',len(frames),'frames:',ROOT/'question4_rotation.gif')


if __name__=='__main__':render()
