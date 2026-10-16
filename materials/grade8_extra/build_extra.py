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
STEPS=[
 ('题1：中等题',[
  step('（1）旋转全等，再把BD拆成两段','m1','连接CF，比较△BAD与△CAF。',
       '由∠BAC=90°、∠ABC=45°，得AB=AC。\n正方形给AD=AF、∠DAF=90°。\n∠BAD=90°-∠DAC=∠CAF。\n所以△BAD≌△CAF（SAS），BD=CF。\nD在B、C之间，BC=BD+DC。','BC=CF+CD。'),
  step('（2）同样全等，点的位置改用减法','m2','D移到BC越过C的延长线上，仍比较同一组三角形。',
       'AB=AC，AD=AF。\n此时∠BAD=90°+∠CAD，\n∠CAF=90°+∠CAD，两角仍相等。\n△BAD≌△CAF（SAS），BD=CF。\n现在B、C、D依次共线，BD=BC+CD。','BC=CF-CD。'),
 ]),
 ('题2（1）：中点制造等腰三角形',[
  step('第1步：延长BF，把F变成第二条线段的中点','h1_sas','延长BF过F到H，使FH=FB；连接DH、CH。',
       'AF=DF（原有中点）。\nBF=FH（新构造）。\n∠AFB=∠DFH（对顶角）。\n所以△AFB≌△DFH（SAS）。\n得到DH=AB，且由对应角得DH∥AB。','DH=AB=CD，DH∥AB；F是BH中点。'),
  step('第2步：中点给平行，等腰给等角','h1_iso','单独突出△BHC的中点连线EF和等腰△DHC。',
       '在△BHC中，E是BC中点，F是BH中点，故EF∥CH。\nDH=CD，所以△DHC为等腰三角形，∠DHC=∠DCH。\nAB∥DH，EF∥CH，且C、D、N共线。\n因此∠BME=∠DHC，∠CNE=∠DCH。','∠BME=∠CNE。'),
 ]),
 ('题2（2）：换位置，重新识别对应角',[
  step('第1步：把第（1）问的辅助构造迁移过来','h2_sas','仍延长BF至H，使FH=FB；连接DH、CH。',
       '原图位置变了，但AF=DF、BF=FH及对顶角仍成立。\n所以△AFB≌△DFH（SAS），DH=AB=CD，DH∥AB。\nE是BC中点，F是BH中点，仍有EF∥CH。','△DHC等腰，且MN∥HC，AB∥DH。'),
  step('第2步：先找大三角形里的两个相等角','h2_iso','突出△DHC，并把MN所在直线与CH作对照。',
       'DH=DC，所以∠DHC=∠DCH。\n图b中O、N在直线AB上，O、M在直线CD上。\n利用AB∥DH、MN∥HC，可将△OMN的两个底角分别对应到△DHC的两个底角。','∠OMN=∠DCH，∠ONM=∠DHC。'),
  step('第3步：放大看△OMN，写出形状','h2_result','放大△OMN，标出M、N处的相等角。',
       '∠OMN=∠DCH，\n∠ONM=∠DHC。\n而∠DCH=∠DHC，\n所以∠OMN=∠ONM。\n等角对等边，得到OM=ON。','△OMN是等腰三角形，OM=ON；顶角度数不固定。'),
 ]),
 ('题2（3）：末问需要新的辅助点',[
  step('第1步：在CA延长线上复制CD','h3_mid','延长CA过A到T，使AT=CD（=AB），连接TB。',
       'A、F、D、C依次共线，AF=FD。\nTF=TA+AF；FC=FD+DC。\n因为TA=DC，所以TF=FC，F恰为TC中点。\nE是BC中点，于是△TBC中EF是中点连线，EF∥TB。','新的辅助点T使EF∥TB，且AT=AB。'),
  step('第2步：60°条件使△TAB变为等边','h3_tab','突出△TAB，用EF∥TB把60°搬到T。',
       'EF∥TB，TA与FC同向共线，\n所以∠BTA=∠EFC=60°。\n又AT=AB，△TAB的两个底角相等，故∠TBA=60°。\n第三个角∠TAB也为60°。','△TAB为等边三角形，∠TAB=60°。'),
  step('第3步：放大看△AGF，证明它是等边','h3_agf','放大△AGF；沿用上一步G、A、B共线，T、A、F共线的关系。',
       '∠GAF与∠TAB为对顶角，所以∠GAF=60°。\nFG∥TB，射线FA与TA反向、射线FG与TB反向，故∠AFG=∠BTA=60°。\n因此△AGF为等边三角形。\nAF=FD（原有中点），于是GF=AF=FD。','AG=GF=AF=FD，∠AGF=60°。'),
  step('第4步：用120°与30°拼出直角','h3_result','放大△AGD，突出等腰△GFD，在G处标直角。',
       'FA、FD反向共线，\n∠GFD=180°-∠GFA=120°。\nGF=FD，所以∠FGD=∠FDG=30°。\nF在AD上，故∠AGD=∠AGF+∠FGD=60°+30°=90°。','△AGD为直角三角形，∠AGD=90°，∠ADG=30°。'),
 ]),
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
    for _,steps in STEPS:
        for s in steps:
            buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(260,220));diagram(c,s['key']);c.save()
            pdf=buf.getvalue();(ROOT/'teaching_figures'/f"{s['key']}.pdf").write_bytes(pdf)
            d=fitz.open(stream=pdf,filetype='pdf');d[0].get_pixmap(matrix=fitz.Matrix(3,3)).save(ROOT/'teaching_figures'/f"{s['key']}.png")


def block(c,s,top):
    txt(c,s['title'],18*MM,top*MM,size=11.5,lead=16)
    c.saveState();c.translate(18*MM,(top-81)*MM);c.scale(82*MM/260,69*MM/220);diagram(c,s['key']);c.restoreState()
    end=txt(c,'作图：'+s['action']+'\n\n'+s['proof'],107*MM,(top-11)*MM,width=85*MM,size=10,lead=14)
    if end<(top-85)*MM:raise ValueError('Block overflow: '+s['key'])
    c.setStrokeColorRGB(*BLUE);c.setLineWidth(.6);c.line(18*MM,(top-87)*MM,192*MM,(top-87)*MM)
    txt(c,'本步结论：'+s['result'],18*MM,(top-94)*MM,size=10.5,lead=15)


def teacher():
    c=canvas.Canvas(str(ROOT/'extra_teacher.pdf'),pagesize=PAGE);page=1
    header(c,'教师版｜难度定位、先备知识与课堂安排',page)
    intro=[
      ('为什么这两题分档','题1只需一次SAS识别BD=CF，再按D的位置作加减，作为中等题。题2前两问需要主动倍长BF，把AD的中点转换为BH的中点，再用中点连线和平行线找到等腰结构；第三问要放弃机械沿用H，另构造T，并连续识别两个等边三角形和一个等腰三角形。按辅助线层数和末问迁移要求，题2与原卷24题的中点构造、25题的特殊三角形综合要求相近。'),
      ('知识范围','全等SAS、等腰与等边三角形、平行线角关系、中点性质。两题均不需要勾股定理、根式运算、相似、圆或函数。中点连线的平行性质若尚未学，可先给出，并用附录的两次SAS补证；不要将未学过性质直接判为能力不足。'),
      ('两小时的一种安排','独立完成两题40—45分钟；批改与追问10分钟；重点讲解40—45分钟；遮住原解重建关键辅助线15分钟；最后5分钟复述。若与前四题混用，应替换其中一部分，不能把六道综合题都按原50分钟塞进去。'),
      ('本次答案与评分','题1：（1）BC=CF+CD；（2）BC=CF-CD。各6分：全等条件3分、CF=BD及结论3分。\n题2：（1）∠BME=∠CNE；（2）OM=ON，△OMN为等腰三角形；（3）∠AGD=90°，∠ADG=30°。第（1）（2）问各6分；末问12分，建议构造T并得到F为TC中点4分、证明△TAB等边2分、证明△AGF等边2分、等腰△GFD角度与直角结论4分。'),
      ('出处说明','题1取公开题库T22-A01-08的前两问，题2取公开讲义习题6.25.11完整三问。原图、原文摘录、固定版本链接与许可随包保存；图b中O已在原图标出，本次按原图补写交点定义，并明确M、N、O互异，保持原图所示的非退化三角形情形。下面各步骤图是独立重绘的教学图。'),
    ]
    y=252*MM
    for title,body in intro:
        y=txt(c,title,18*MM,y,size=11,lead=17)
        y=txt(c,body,18*MM,y-2,size=10,lead=15)-9
    if y<24*MM:raise ValueError('Intro overflow')
    c.showPage();page+=1
    for title,steps in STEPS:
        for start in range(0,len(steps),2):
            header(c,'教师版｜'+title,page)
            block(c,steps[start],250)
            if start+1<len(steps):block(c,steps[start+1],140)
            c.showPage();page+=1
    header(c,'教师版｜中点引理与即时回练',page)
    append=[
      ('中点连线平行性质：只用两次SAS','△TUV中，X、Y分别为TU、TV中点。延长XY至Z，使YZ=YX。由TY=YV、YX=YZ和对顶角，△TYX≌△VYZ（SAS），所以VZ=TX=UX，VZ∥UX。连接UZ。由UX=VZ、UZ公共和内错角，△XUZ≌△VZU（SAS），得XZ=VU，XZ∥VU，进而XY∥UV。所配逐步图见原教师图解附录（链接在README），可在课前补讲。'),
      ('末问必须讲透的四个问题','①为什么在CA越过A的方向取T，而不是在AC越过C的方向？\n②怎样从AT=CD和AF=FD推出TF=FC？\n③哪一步用到了∠EFC=60°？\n④为什么最后答案是G处直角，而不是把△AGD直接认成等边？'),
      ('即时回练，不另编题','遮住教师答案，让学生只看图c，重新构造T、证明F是TC中点，并口述从平行线到60°、120°、30°、90°的完整链条。若讲解后能重建，记录为即时掌握；下一课还需陌生同型题检查迁移。'),
      ('提示等级与记录','题1独立用时____分钟，____/12；题2____分钟，____/24。\n辅助线：□独立想到 □口头方向 □给出辅助点 □完整示范。\n中点性质：□已掌握 □需补讲。\n末问卡在：□构造T □证明中点 □角度迁移 □特殊三角形 □合并角度。'),
    ]
    y=252*MM
    for title,body in append:
        y=txt(c,title,18*MM,y,size=11,lead=17);y=txt(c,body,18*MM,y-2,size=10,lead=15)-10
    c.showPage();c.save()
    d=base.word_base('补充两题：逐步配图教师答案')
    d.sections[0].footer.paragraphs[0].text='逐步配图教师答案｜2026-10-17｜出处与编排说明见README'
    d.add_heading('中等题与综合压轴题：教师说明',0)
    text='# 两道补充题：逐步配图教师答案\n\n题目来源与编排说明见[README](README.md)。\n\n'
    for title,body in intro:
        d.add_heading(title,2);d.add_paragraph(body);text+=f'## {title}\n\n{body}\n\n'
    for title,steps in STEPS:
        for s in steps:
            d.add_page_break();d.add_heading(title,0);d.add_heading(s['title'],1)
            d.add_paragraph('作图：'+s['action']);d.add_picture(str(ROOT/'teaching_figures'/f"{s['key']}.png"),width=Cm(10.5))
            d.add_paragraph(s['proof']);d.add_paragraph('本步结论：'+s['result'])
            text+=f"## {title}｜{s['title']}\n\n![本步辅助线图](teaching_figures/{s['key']}.png)\n\n**作图：** {s['action']}\n\n"+s['proof'].replace('\n','\n\n')+f"\n\n**结论：** {s['result']}\n\n"
    d.add_page_break();d.add_heading('中点引理与回练',0)
    for title,body in append:d.add_heading(title,2);d.add_paragraph(body);text+=f'## {title}\n\n{body}\n\n'
    d.save(ROOT/'extra_teacher.docx');(ROOT/'extra_teacher.md').write_text(text.rstrip()+'\n',encoding='utf-8')


def bundle():
    path=ROOT/'extra_two_problems.zip'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(ROOT.rglob('*')):
            if p.is_file() and p!=path and '__pycache__' not in p.parts:z.write(p,p.relative_to(ROOT))


if __name__=='__main__':
    render_figures();student();teacher();bundle()
    print('Built supplementary student/teacher PDFs, Word files, illustrated Markdown and ZIP.')
