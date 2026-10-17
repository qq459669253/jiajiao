"""Two existing supplementary problems, with illustrated solutions.

GPL-3.0 for this independent arrangement and solution code; source components
retain their upstream licenses (see README). Run from the complete repository:
python materials/grade8_extra/build_extra.py
"""
from pathlib import Path
import sys,math,io,zipfile
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from docx.shared import Cm

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'grade8_selected'))
import build_selected_pack as base
from illustrated_teacher import Drawing,add,sub,mul,mid,rotate,meet,length
MM=base.MM;PAGE=(base.W,base.H);txt=base.txt
RED=(.72,.12,.14);BLUE=(.05,.32,.66);GREEN=(.08,.43,.31);GRAY=(.52,.55,.58)

MEDIUM='已知，在△ABC中，∠BAC=90°，∠ABC=45°，D为直线BC上的动点（不与B、C重合），以AD为边作正方形ADEF，连接CF。\n（1）如图1，当D在线段BC上时，求证：BC=CF+CD。\n（2）如图2，当D在线段BC的延长线上时，其他条件不变，请直接写出BC、CD、CF三条线段之间的数量关系。'
HARD='（1）如图a，在四边形ABCD中，AB=CD，E、F分别是BC、AD的中点。直线EF与BA、CD的延长线分别交于M、N。求证：∠BME=∠CNE。\n（2）如图b，在四边形ADBC中，AB=CD，E、F分别是BC、AD的中点。AB与CD交于O，直线EF与DC、AB分别交于M、N，M、N、O互不重合。判断△OMN的形状，并证明。\n（3）如图c，在△ABC中，AC>AB，D在AC上，且AB=CD。E、F分别为BC、AD的中点，直线EF与BA的延长线交于G。若∠EFC=60°，连接GD，判断△AGD的形状，并证明。'


def geometry(kind):
    if kind.startswith('m'):
        p={'A':(0.,4.),'B':(-4.,0.),'C':(4.,0.),'D':(-1.,0.) if kind=='m1' else (6.,0.)}
        p['F']=add(p['A'],rotate(sub(p['D'],p['A']),math.pi/2));p['E']=add(p['D'],sub(p['F'],p['A']))
    elif kind=='h1':
        u=(0.,-1.);v=(.6,-.8)
        p={'A':mul(u,2),'B':mul(u,4),'D':mul(v,3),'C':mul(v,5)}
        p['E']=mid(p['B'],p['C']);p['F']=mid(p['A'],p['D'])
        p['M']=meet(p['E'],p['F'],p['B'],p['A']);p['N']=meet(p['E'],p['F'],p['C'],p['D'])
        p['H']=sub(mul(p['F'],2),p['B'])
    elif kind=='h2':
        u=(.55,-math.sqrt(1-.55**2));v=(.95,math.sqrt(1-.95**2))
        p={'O':(0.,0.),'A':mul(u,-2),'B':mul(u,4),'C':mul(v,3),'D':mul(v,-3)}
        p['E']=mid(p['B'],p['C']);p['F']=mid(p['A'],p['D'])
        p['M']=meet(p['E'],p['F'],p['D'],p['C']);p['N']=meet(p['E'],p['F'],p['A'],p['B'])
        p['H']=sub(mul(p['F'],2),p['B'])
    else:
        p={'A':(0.,0.),'B':(-.5,math.sqrt(3)/2),'C':(4.,0.),'D':(3.,0.),'F':(1.5,0.),'G':(.75,-.75*math.sqrt(3)),'T':(-1.,0.)}
        p['E']=mid(p['B'],p['C'])
        angle=-math.atan2(p['C'][1]-p['B'][1],p['C'][0]-p['B'][0])
        p={k:(rotate(v,angle)[0],-rotate(v,angle)[1]) for k,v in p.items()}
    return p


def diagram(c,key):
    kind=key.split('_')[0];p=geometry(kind)
    if key=='h2_result':p={k:p[k] for k in ['O','M','N']}
    if key in ['h3_agf','h3_result']:p={k:p[k] for k in ['A','D','F','G']}
    d=Drawing(c,p,txt)
    offsets={'A':(-12,8),'B':(-14,-12),'C':(5,-10),'D':(4,5),'E':(-4,-15),'F':(-12,4),'G':(-5,10),'M':(-13,7),'N':(5,3),'H':(5,5),'O':(-8,9),'T':(-15,5)}
    if kind.startswith('m'):
        d.edges([('A','B'),('B','C'),('C','A'),('A','D'),('D','E'),('E','F'),('F','A')])
        if kind=='m2':d.segment('C','D',GRAY,.8,True)
        d.segment('C','F',GREEN,1.7,True)
        d.triangle(['B','A','D'],RED);d.triangle(['C','A','F'],BLUE)
        d.tick('A','B');d.tick('A','C');d.tick('A','D',2);d.tick('A','F',2)
        d.angle('A','B','D','',RED,16);d.angle('A','C','F','',BLUE,28)
        offsets['F']=(6,5);offsets['D']=(5,-13)
    elif kind in ['h1','h2'] and key!='h2_result':
        edges=[('A','B'),('B','C'),('C','D'),('D','A')] if kind=='h1' else [('A','D'),('D','B'),('B','C'),('C','A'),('A','B'),('C','D')]
        d.edges(edges)
        d.segment('M','E',GRAY,.9);d.segment('N','E',GRAY,.9)
        d.edges([('B','H'),('D','H'),('H','C')],color=BLUE,width=1.3,dash=True)
        if key.endswith('sas'):
            d.triangle(['A','F','B'],RED);d.triangle(['D','F','H'],BLUE)
            d.tick('A','F');d.tick('F','D');d.tick('B','F',2);d.tick('F','H',2)
        else:
            d.triangle(['D','H','C'],BLUE);d.segment('F','E',RED,2)
            d.tick('D','H');d.tick('D','C');d.tick('B','E',2);d.tick('E','C',2)
            d.angle('H','D','C','',BLUE,15);d.angle('C','D','H','',BLUE,25)
        if kind=='h2':offsets.update(O=(3,7),M=(-18,-11),N=(7,-11),F=(-12,6),H=(-15,7),D=(-18,-5))
    elif key=='h2_result':
        d.triangle(['O','M','N'],RED);d.tick('O','M');d.tick('O','N')
        d.angle('M','O','N','',RED,20);d.angle('N','O','M','',RED,20)
        offsets.update(O=(-4,10),M=(-17,-10),N=(6,-10))
    else:
        if key not in ['h3_agf','h3_result']:
            d.edges([('A','B'),('B','C'),('C','A'),('A','D'),('G','B'),('G','E'),('G','D')])
            d.edges([('T','A'),('T','B'),('T','C')],color=BLUE,width=1.3,dash=True)
        else:
            d.edges([('A','D'),('A','G'),('G','F'),('G','D')])
        if key=='h3_mid':
            d.triangle(['T','B','C'],BLUE);d.segment('E','F',RED,2)
            d.tick('T','F');d.tick('F','C');d.tick('B','E',2);d.tick('E','C',2)
        elif key=='h3_tab':
            d.triangle(['T','A','B'],BLUE);d.tick('T','A');d.tick('A','B')
            d.segment('F','E',RED,2);d.angle('T','B','A','60°',BLUE,17)
        elif key=='h3_agf':
            d.triangle(['A','G','F'],RED);d.tick('A','G');d.tick('G','F');d.tick('A','F');d.tick('F','D')
            d.angle('A','G','F','60°',RED,16);d.angle('F','A','G','60°',RED,16)
        else:
            d.triangle(['G','F','D'],BLUE);d.segment('G','A',RED,1.6);d.segment('A','D',GRAY,.9)
            d.tick('G','F');d.tick('F','D');d.right('G','A','D',RED)
            d.angle('F','G','D','120°',BLUE,20);d.angle('D','F','G','30°',BLUE,25)
    d.labels(offsets)


def step(title,key,action,proof,result):return dict(title=title,key=key,action=action,proof=proof,result=result)
MEDIUM_STEPS=[
  step('（1）旋转全等，再把BD拆成两段','m1','连接CF，比较△BAD与△CAF。',
       '由∠BAC=90°、∠ABC=45°，得AB=AC。\n正方形给AD=AF、∠DAF=90°。\n∠BAD=90°-∠DAC=∠CAF。\n所以△BAD≌△CAF（SAS），BD=CF。\nD在B、C之间，BC=BD+DC。','BC=CF+CD。'),
  step('（2）同样全等，点的位置改用减法','m2','D移到BC越过C的延长线上，仍比较同一组三角形。',
       'AB=AC，AD=AF。\n此时∠BAD=90°+∠CAD，\n∠CAF=90°+∠CAD，两角仍相等。\n△BAD≌△CAF（SAS），BD=CF。\n现在B、C、D依次共线，BD=BC+CD。','BC=CF-CD。'),
 ]


def header(c,title,page):
    base.header(c,'初二数学补充题：中等题＋综合压轴',title,page,revision='2026-10-17')


def image_fit(c,path,x,y,w,h):
    image=ImageReader(str(path));iw,ih=image.getSize();s=min(w/iw,h/ih)
    c.drawImage(image,x+(w-iw*s)/2,y+(h-ih*s)/2,iw*s,ih*s,mask='auto')


def lines(c,y,n):
    c.setStrokeColorRGB(.77,.80,.81);c.setLineWidth(.3)
    for k in range(n):c.line(18*MM,y-k*9*MM,192*MM,y-k*9*MM)


def student():
    c=canvas.Canvas(str(ROOT/'extra_student.pdf'),pagesize=PAGE)
    header(c,'学生版｜建议40—45分钟｜满分36分｜姓名：____________',1)
    y=txt(c,'题1｜中等：直角旋转与线段和差（12分，建议10—12分钟）',18*MM,254*MM,size=12,lead=19)
    y=txt(c,'来源：公开题库T22-A01-08，节选第（1）（2）问。',18*MM,y-3,size=8.5,lead=14)
    y=txt(c,MEDIUM,18*MM,y-8,size=11,lead=18)
    image_fit(c,ROOT/'sources/medium_01.png',18*MM,146*MM,80*MM,61*MM)
    image_fit(c,ROOT/'sources/medium_02.png',111*MM,146*MM,80*MM,61*MM)
    txt(c,'本次作答要求：两问均写出理由，各6分。',18*MM,136*MM,size=9.5,lead=15)
    lines(c,126*MM,12);c.showPage()
    header(c,'学生版｜题2完整题面｜证明可写在下一页',2)
    y=txt(c,'题2｜综合压轴：中点、等腰与特殊三角形（24分）',18*MM,254*MM,size=12,lead=19)
    y=txt(c,'来源：《初中数学总复习讲义》习题6.25.11，印刷页79／PDF第84页。',18*MM,y-3,size=8.5,lead=14)
    y=txt(c,HARD,18*MM,y-8,size=10.8,lead=18)
    image_fit(c,ROOT/'sources/challenge_630.png',18*MM,122*MM,174*MM,54*MM)
    txt(c,'本次分值：（1）6分；（2）6分；（3）12分，均需完整证明。\n若尚未学中点连线性质，可先由教师说明：连接三角形两边中点的线段平行于第三边。',18*MM,113*MM,size=9,lead=15)
    lines(c,92*MM,8);c.showPage()
    header(c,'学生版｜题2证明续页（请写明小问）',3);lines(c,252*MM,25);c.save()
    d=base.word_base('初二数学补充题：一道中等题与一道综合压轴题')
    d.sections[0].footer.paragraphs[0].text='现有题选编｜出处与编排说明见README｜2026-10-17'
    d.add_heading('题1｜中等：直角旋转与线段和差',0);d.add_paragraph(MEDIUM)
    for n in ['01','02']:d.add_picture(str(ROOT/f'sources/medium_{n}.png'),width=Cm(7))
    d.add_paragraph('第（1）（2）问均写理由，各6分。');d.add_page_break()
    d.add_heading('题2｜综合压轴：中点、等腰与特殊三角形',0);d.add_paragraph(HARD)
    d.add_picture(str(ROOT/'sources/challenge_630.png'),width=Cm(17))
    d.add_paragraph('（1）6分；（2）6分；（3）12分。若中点连线性质未学，可由教师先说明。')
    d.add_page_break();d.add_heading('证明续页',1)
    for _ in range(20):d.add_paragraph('________________________________________________________________')
    d.save(ROOT/'extra_student.docx')
    (ROOT/'extra_student.md').write_text('# 两道补充题（学生题面）\n\n## 题1：中等\n\n'+MEDIUM+'\n\n![图1](sources/medium_01.png) ![图2](sources/medium_02.png)\n\n## 题2：综合压轴\n\n'+HARD+'\n\n![图a、b、c](sources/challenge_630.png)\n',encoding='utf-8')


def render_figures():
    for item in MEDIUM_STEPS:
        buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(260,220));diagram(c,item['key']);c.save()
        pdf=buf.getvalue();path=ROOT/'teaching_figures'/item['key']
        path.with_suffix('.pdf').write_bytes(pdf)
        doc=fitz.open(stream=pdf,filetype='pdf')
        doc[0].get_pixmap(matrix=fitz.Matrix(3,3)).save(path.with_suffix('.png'))


def block(c,s,top):
    txt(c,s['title'],18*MM,top*MM,size=11.5,lead=16)
    c.saveState();c.translate(18*MM,(top-81)*MM);c.scale(82*MM/260,69*MM/220);diagram(c,s['key']);c.restoreState()
    end=txt(c,'作图：'+s['action']+'\n\n'+s['proof'],107*MM,(top-11)*MM,width=85*MM,size=10,lead=14)
    if end<(top-85)*MM:raise ValueError('Block overflow: '+s['key'])
    c.setStrokeColorRGB(*BLUE);c.setLineWidth(.6);c.line(18*MM,(top-87)*MM,192*MM,(top-87)*MM)
    txt(c,'本步结论：'+s['result'],18*MM,(top-94)*MM,size=10.5,lead=15)


def teacher():
    import detailed_teacher
    detailed_teacher.build(sys.modules[__name__])


def bundle():
    path=ROOT/'extra_two_problems.zip'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(ROOT.rglob('*')):
            if p.is_file() and p!=path and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT))


if __name__=='__main__':
    render_figures();student();teacher();bundle()
    print('Built supplementary student/teacher PDFs, Word files, illustrated Markdown and ZIP.')
