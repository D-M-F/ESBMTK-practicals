from pathlib import Path
import subprocess
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
import pdfplumber
import json

root = Path(__file__).resolve().parents[3]
out = root / 'output/pdf/instructor_review'
renders = Path(__file__).parent / 'final_rendered'
renders.mkdir(exist_ok=True)
pdfs = sorted(out.glob('0[0-4]_*.pdf'))
def render(pdf):
    result = subprocess.run(['pdftoppm', '-scale-to', '1100', '-png', str(pdf), str(renders/pdf.stem)],capture_output=True,text=True)
    assert result.returncode == 0, result.stderr
with ThreadPoolExecutor(3) as pool:
    list(pool.map(render,pdfs))
report = []
for pdf in pdfs:
    with pdfplumber.open(pdf) as document:
        bad = []
        for i,page in enumerate(document.pages):
            for c in page.chars:
                if c['x0'] < 15 or c['x1'] > page.width-15 or c['top'] < 10 or c['bottom'] > page.height-10:
                    bad.append({'page':i+1,'text':c['text'],'x0':c['x0'],'x1':c['x1'],'top':c['top'],'bottom':c['bottom']})
        report.append({'pdf':pdf.name, 'pages':len(document.pages), 'out_of_page_chars':bad})
files = sorted(renders.glob('0*.png'))
for k in range(0,len(files),8):
    canvas=Image.new('RGB',(1000,4*740),'#dce3e8')
    draw=ImageDraw.Draw(canvas)
    for j,p in enumerate(files[k:k+8]):
        im=Image.open(p)
        im.thumbnail((480,704))
        x=(j%2)*500+10
        y=(j//2)*740+25
        canvas.paste(im,(x,y))
        draw.text((x,y-20),p.name,fill='black')
    canvas.save(renders/f'contact-{k//8+1:02}.jpg')
(Path(__file__).parent/'final-page-qa.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
