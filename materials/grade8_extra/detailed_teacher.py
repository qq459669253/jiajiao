"""GPL-3.0. Expanded, self-contained teaching explanation for the capstone."""
import io
import math
import zipfile
from pathlib import Path

import fitz
from docx.shared import Cm, Pt
from reportlab.pdfgen import canvas

import build_selected_pack as base
from illustrated_teacher import Drawing, add, sub, mul, mid, length

MM = base.MM
RED = (.72, .12, .14)
BLUE = (.05, .32, .66)
GREEN = (.08, .43, .31)
GRAY = (.55, .58, .61)


def step(group, title, key, why, action, proof, result, check):
    return dict(group=group, title=title, key=key, why=why, action=action,
                proof=proof, result=result, check=check)


LESSONS = [
    step('先备知识', '引理第1步：把中点条件变成全等条件', 'lemma_sas',
         '后三问都要用“连接两边中点的线段平行于第三边”。若尚未学过，先用全等证明；本页和下一页合起来就是完整证明。',
         '在△TUV中，X、Y分别为TU、TV中点。延长XY过Y至Z，使YZ=YX；连接VZ、UZ。',
         '① TY=YV（Y是TV中点），YX=YZ（作图）。\n② ∠TYX=∠VYZ（对顶角）。\n③ 所以△TYX≌△VYZ（SAS）。\n④ 对应边相等，得TX=VZ；又TX=XU，故XU=VZ。\n⑤ 对应角∠TXY=∠VZY；它们是内错角，故TX∥VZ。\n⑥ T、X、U共线，因此XU∥VZ。',
         '得到一组平行且相等的线段：XU∥VZ，XU=VZ。',
         '本页只做准备：还没有证明XY∥UV，要继续看第二次全等。'),
    step('先备知识', '引理第2步：再用一次SAS，得到平行', 'lemma_parallel',
         '上页已把XU与VZ变成平行且相等的一组边。连接UZ后，再比较共用UZ的两个三角形。',
         '突出△XUZ、△VZU；UZ是公共边。',
         '① XU=VZ（上页），UZ=ZU（公共边）。\n② XU∥VZ，故∠XUZ=∠VZU（内错角）。\n③ 所以△XUZ≌△VZU（SAS）。\n④ 得∠XZU=∠VUZ（对应角）。\n⑤ 这两个角是直线XZ、UV被UZ所截的内错角，故XZ∥UV。\n⑥ X、Y、Z共线，所以XY∥UV。',
         '三角形两边中点的连线平行于第三边；下文简称“中点连线性质”。',
         '对应到后文：先找到一个三角形，再说明两个点分别是哪两条边的中点。'),
    step('第（1）问', '第1步：为什么要倍长BF？', 'h1_sas',
         'AB=CD，但这两条边还没在同一个三角形里。想把AB复制到D处；F又是AD中点，所以尝试以F为中心作一组全等三角形。',
         '连接BF，延长BF过F至H，使FH=FB；连接DH、CH。',
         '① AF=DF（F是AD中点），BF=FH（作图）。\n② A、F、D共线，B、F、H共线，故∠AFB=∠DFH。\n③ △AFB≌△DFH（SAS），对应为A↔D、F↔F、B↔H。\n④ 所以DH=AB；结合AB=CD，得DH=CD。\n⑤ 还得到∠ABF=∠DHF（对应角）。\n⑥ 这是一组内错角，故AB∥DH。',
         'DH=CD，AB∥DH；同时B、F、H共线且BF=FH。',
         '辅助点H做了两件事：复制AB，并让F成为BH的中点。'),
    step('第（1）问', '第2步：两个中点落在哪个三角形里？', 'h1_mid',
         'E原本就是BC中点；上一步又得到F是BH中点。两条线段BC、BH共同属于△BHC，所以应当看这个大三角形。',
         '突出△BHC及其中的EF；另用蓝色突出等腰△DHC。',
         '① 在△BHC中，BE=EC，故E是BC中点。\n② B、F、H共线且BF=FH，故F是BH中点。\n③ 由中点连线性质，EF∥CH。\n④ 由上页DH=CD，△DHC是等腰三角形，底边为HC。\n⑤ 因而两个底角相等：∠DHC=∠DCH。\n⑥ 现在已知AB∥DH、EF∥CH，下一步把目标角对应过来。',
         '先在等腰△DHC中得到∠DHC=∠DCH，再去找原题的角。',
         '等腰三角形的顶点是D，两个相等的角在H、C。'),
    step('第（1）问', '第3步：把两组对应角分别画出来', 'h1_angles',
         '“两组线分别平行”本身还不够，角也可能互补。要检查组成角的两条射线是同向还是反向；两条射线同时反向，角度保持不变。',
         '上排对照M、H处的角；下排对照N、C处的角。箭头表示射线方向，同色弧表示待比较的角。',
         '① 在图a的位置中，射线MB与HD平行且同向，ME与HC也平行且同向。\n   所以∠BME=∠DHC（上排两个角）。\n② 射线NC与CD平行且反向，NE与CH也平行且反向。\n   相当于把整个角转过180°，所以∠CNE=∠DCH（下排两个角）。\n③ 上页已证∠DHC=∠DCH。\n④ 连起来：∠BME=∠DHC=∠DCH=∠CNE。',
         '∠BME=∠CNE，第（1）问得证。',
         '不能把“CD与NC共线”直接写成同向；这里它们实际反向。'),
    step('第（2）问', '第1步：位置变了，哪些结论仍成立？', 'h2_sas',
         '第（1）问的构造只用到中点和全等，换成图b仍可使用。先重新列出理由，再辨认目标三角形的位置。',
         '仍延长BF过F至H，使FH=FB；连接DH、CH。',
         '① AF=DF、BF=FH，且∠AFB=∠DFH。\n② △AFB≌△DFH（SAS），得DH=AB=CD。\n③ ∠ABF=∠DHF（对应角），内错角相等，故AB∥DH。\n④ 在△BHC中，E是BC中点，F是BH中点，故EF∥CH。\n⑤ M、N、E、F共线，所以MN∥CH。\n⑥ DH=CD，所以∠DHC=∠DCH。',
         '仍有等腰△DHC、MN∥CH、AB∥DH。',
         'O是AB与CD交点；M、N是EF分别与CD、AB的交点。不要把交点认反。'),
    step('第（2）问', '第2步：小三角形的底角对应哪里？', 'h2_angles',
         '原图的△OMN很小，容易看错。这里把M、N处的角拆开画，并与等腰△DHC的两个底角分别比较。',
         '上排比较∠OMN与∠DCH；下排比较∠ONM与∠DHC。',
         '① 射线MO与CD平行且反向，MN与CH也平行且反向。\n   两条射线同时反向，故∠OMN=∠DCH。\n② 射线NO与HD平行且反向，NM与HC也平行且反向。\n   两条射线同时反向，故∠ONM=∠DHC。\n③ 等腰△DHC给出∠DCH=∠DHC。\n④ 所以∠OMN=∠ONM，即△OMN的M、N两角相等。',
         '相等的是M、N处的两个角；下一页由等角判断等边。',
         '这些射线方向按图b所示位置判断；角的拆图保留了原图的方向。'),
    step('第（2）问', '第3步：由两个相等角，写出形状', 'h2_result',
         '已经得到M、N处角相等，形状判断只需再用“等角对等边”。此时应单独看△OMN。',
         '放大△OMN，标出相等的底角及其所对的边。',
         '① ∠OMN=∠ONM（上页）。\n② ∠OMN所对的边是ON，∠ONM所对的边是OM。\n③ 在同一个三角形中，等角对等边，所以ON=OM。\n④ 故△OMN是以O为顶点、MN为底边的等腰三角形。',
         '△OMN是等腰三角形，OM=ON。',
         '条件不能确定O处角度；这里没有理由进一步断言它是直角三角形。'),
    step('第（3）问', '第1步：倍长AE，先把AB复制到CH', 'ae_sas',
         '沿用“倍长中线、构造全等”的方法。E是BC中点；连接AE并倍长后，能把AB复制到C处，与原有的CD比较。',
         '连接AE，延长AE过E至H，使EH=EA；连接CH、DH。本问H按这个作法重新定义。',
         '① AE=EH（作图），BE=EC（E是BC中点）。\n② A、E、H共线，B、E、C共线，故∠AEB=∠HEC（对顶角）。\n③ 所以△AEB≌△HEC（SAS），对应为A↔H、E↔E、B↔C。\n④ 得CH=AB；结合AB=CD，得CH=CD。\n⑤ 还得∠ABE=∠HCE（对应角）。\n⑥ 这两个角是一组内错角，故AB∥CH。',
         'CH=CD，AB∥CH；E既是BC中点，也是AH中点。',
         '本问H在AE的延长线上，与前两问BF延长线上的H分别定义，不能混用。'),
    step('第（3）问', '第2步：在哪个三角形里得到EF∥DH？', 'ae_mid',
         'F是AD中点；倍长AE又让E成为AH中点。于是这两个中点落在△ADH的两条边上，正好能把EF与DH联系起来。',
         '突出△ADH：E在AH上、F在AD上，连接两个中点得到EF。',
         '① 在△ADH中，AF=FD，所以F是AD中点。\n② A、E、H共线且AE=EH，所以E是AH中点。\n③ 由中点连线性质，EF∥DH。\n④ 又G、F、E共线，因此GF∥DH。\n⑤ 连同上页AB∥CH及G、A、B共线，还得到AG∥CH。',
         '两组关键平行：GF∥DH，AG∥CH。它们正是通向△AGD的桥梁。',
         '这里使用的是△ADH的中点连线，不是△ABC的中点连线。'),
    step('第（3）问', '第3步：严格证明你找到的△DHC等边', 'ae_equilateral',
         '上面已经得到CH=CD。再把∠EFC=60°移到D处，就能确定等腰△DHC的两个底角，从而得到等边。',
         '突出△DHC，并比较F处∠EFC与D处∠CDH。',
         '① EF∥DH，且FC与DC在同一直线上、方向相同。\n② ∠CDH与∠EFC是同位角，所以∠CDH=60°。\n③ CH=CD，因此△DHC是等腰三角形，底边是DH。\n④ ∠DHC=∠CDH=60°（等边对等角）。\n⑤ ∠HCD=180°-60°-60°=60°，故△DHC是等边三角形。',
         '△DHC等边。相等边CH、CD的公共顶点是C，底角在D、H。',
         '这里已确认你的构造可行；下一步不直接判断△AGD，先转看△AGF。'),
    step('第（3）问', '第4步：从△DHC转到△AGF，是关键的一步', 'ae_agf',
         '△AGD暂时缺少边长关系。但F是AD中点，只要先证明△AGF等边，就能得到GF=AF=FD，再使用等腰△GFD。',
         '上方突出△AGF，下方突出△DHC；A、F、D、C共线，两组斜边分别平行。',
         '① AG∥CH；AG与CH反向，AF与CD也反向。\n   两条射线同时反向，所以∠GAF=∠HCD=60°。\n② GF∥DH；FA与DC反向，FG与DH也反向。\n   所以∠AFG=∠CDH=60°。\n③ △AGF的第三个角∠AGF=180°-60°-60°=60°。\n④ 因而△AGF等边，得到AG=GF=AF。\n⑤ 原题AF=FD，所以GF=FD。',
         '由等边△DHC的角，得到等边△AGF，再得到GF=FD。',
         '直接连接两种结构的不是GD，而是GF：它既在等边△AGF中，又在等腰△GFD中。'),
    step('第（3）问', '第5步：为什么会出现120°和30°？', 'h3_gfd',
         'F在AD上，FA与FD方向相反。因此等边△AGF的60°旁边，恰好是一个120°；再利用GF=FD求出两个底角。',
         '单独放大△GFD，保留A以便看清FA、FD是两条反向射线。',
         '① A、F、D依次共线，故∠GFA+∠GFD=180°（平角）。\n② △AGF等边，∠GFA=60°，所以∠GFD=120°。\n③ 上页GF=FD，故△GFD是等腰三角形，顶点为F。\n④ ∠FGD=∠FDG=(180°-120°)÷2=30°。\n⑤ A、F均在D的同侧，且三点共线，所以射线DF与DA重合，\n   因而∠ADG=∠FDG=30°。',
         '△GFD中：F处120°，G、D处各30°；△AGD在D处也是30°。',
         '相等边GF、FD的公共端点是F，所以120°是顶角，两个30°是底角。'),
    step('第（3）问', '第6步：哪个角是直角？把它拼出来', 'h3_final',
         '要求判断的是△AGD。前面得到的等边△AGF、等腰△GFD只是中间结构，最后必须回到G点把相邻的两个角相加。',
         '突出整个△AGD，用GF把G处的角分成60°与30°两部分，再标出总直角。',
         '① 在△AGF中，∠AGF=60°；在△GFD中，∠FGD=30°。\n② F在线段AD上，所以射线GF在∠AGD内部。\n③ ∠AGD=∠AGF+∠FGD=60°+30°=90°。\n④ 因而△AGD是直角三角形，直角顶点为G。\n⑤ 另有∠ADG=30°、∠GAD=60°。\n⑥ 还可由AD=AF+FD=2AF=2AG，得到AD=2AG。',
         '最终答案：△AGD是直角三角形，∠AGD=90°，∠ADG=30°。',
         '不要把两个中间结论混起来：△AGF等边、△GFD等腰、△AGD直角。'),
]


def arrow(c, p, q, color, width=1.25):
    c.saveState()
    c.setStrokeColorRGB(*color)
    c.setLineWidth(width)
    c.line(*p, *q)
    v = mul(sub(q, p), 1 / length(sub(q, p)))
    n = (-v[1], v[0])
    for sign in [-1, 1]:
        z = add(sub(q, mul(v, 5)), mul(n, sign * 2.4))
        c.line(*q, *z)
    c.restoreState()


def angle_comparisons(c, b, kind):
    p = b.geometry(kind)
    pairs = ([('M', 'B', 'E'), ('H', 'D', 'C'),
              ('N', 'C', 'E'), ('C', 'D', 'H')] if kind == 'h1' else
             [('M', 'O', 'N'), ('C', 'D', 'H'),
              ('N', 'O', 'M'), ('H', 'D', 'C')])
    for i, (v, a, z) in enumerate(pairs):
        color = RED if i < 2 else BLUE
        directions = [mul(sub(p[name], p[v]), 49 / length(sub(p[name], p[v]))) for name in [a,z]]
        # Give each angle its own bounding box. Upward and downward rays
        # have different vertex heights, so titles and endpoints never collide.
        ends = [mul(u,1.17) for u in directions]+[(0,0)]
        lo,hi = (125,185) if i<2 else (15,75)
        center = ((25+143*(i%2)+116+143*(i%2)-min(x for x,y in ends)-max(x for x,y in ends))/2,
                  (lo+hi-min(y for x,y in ends)-max(y for x,y in ends))/2)
        for name in [a, z]:
            u = sub(p[name], p[v]); u = mul(u, 49 / length(u))
            end = add(center, u)
            arrow(c, center, end, color)
            loc = add(center, mul(u, 1.17))
            base.txt(c, name, loc[0] - 3, loc[1] - 3, width=20, size=9, lead=10)
        u, w = directions
        start = math.degrees(math.atan2(u[1], u[0]))
        end = math.degrees(math.atan2(w[1], w[0]))
        extent = (end - start + 180) % 360 - 180
        c.setStrokeColorRGB(*color)
        c.arc(center[0]-17, center[1]-17, center[0]+17, center[1]+17, start, extent)
        away=mul(add(u,w),-1/length(add(u,w)))
        vl=add(center,mul(away,10))
        base.txt(c, v, vl[0]-3, vl[1]-3, width=20, size=9, lead=10)
        base.txt(c, f'∠{a}{v}{z}', 20+143*(i % 2), 204-109*(i//2), width=100, size=10, lead=12)
    c.setStrokeColorRGB(*GRAY);c.setLineWidth(.5);c.line(8,110,252,110)


def ae_geometry(b):
    p=b.geometry('h3')
    p.pop('T')
    p['H']=sub(mul(p['E'],2),p['A'])
    return p


def ae_figure(c,key,b):
    p=ae_geometry(b)
    keep={'ae_sas':['A','B','C','D','E','F','H'],
          'ae_mid':['A','D','E','F','H','C'],
          'ae_equilateral':['A','B','C','D','E','F','H'],
          'ae_agf':['A','D','C','F','G','H']}[key]
    d=Drawing(c,{k:p[k] for k in keep},base.txt)
    offsets={'A':(-14,5),'B':(-14,-10),'C':(5,3),'D':(2,8),
             'E':(-4,-14),'F':(-12,6),'G':(-4,8),'H':(2,-14)}
    if key=='ae_sas':
        d.edges([('A','B'),('B','C'),('C','A'),('A','H'),('D','H'),('C','H'),('F','E')])
        d.triangle(['A','E','B'],RED);d.triangle(['H','E','C'],BLUE)
        for a,z in [('A','E'),('E','H')]:d.tick(a,z)
        for a,z in [('B','E'),('E','C')]:d.tick(a,z,2)
    elif key=='ae_mid':
        d.edges([('A','C'),('A','H'),('D','H')])
        d.triangle(['A','D','H'],BLUE);d.segment('E','F',RED,2)
        for a,z in [('A','E'),('E','H')]:d.tick(a,z)
        for a,z in [('A','F'),('F','D')]:d.tick(a,z,2)
    elif key=='ae_equilateral':
        d.edges([('A','B'),('B','C'),('A','C'),('A','H'),('F','E')])
        d.triangle(['D','H','C'],BLUE)
        d.segment('D','H',RED,1.8);d.segment('F','E',RED,1.8)
        d.tick('C','H');d.tick('C','D')
        d.angle('F','E','C','60°',RED,17);d.angle('D','C','H','60°',RED,17)
    else:
        offsets['F']=(5,-13)
        d.edges([('A','C')]);d.triangle(['A','G','F'],RED);d.triangle(['D','H','C'],BLUE)
        d.segment('A','G',BLUE,1.8);d.segment('C','H',BLUE,1.8)
        d.segment('F','G',GREEN,1.8);d.segment('D','H',GREEN,1.8)
        d.angle('A','G','F','60°',RED,15);d.angle('F','A','G','60°',RED,15)
        d.angle('C','H','D','60°',BLUE,7);d.angle('D','C','H','60°',BLUE,7)
    d.labels(offsets)


def figure(c, key, b):
    if key.startswith('ae_'):
        ae_figure(c,key,b);return
    if key in ['h1_angles', 'h2_angles']:
        angle_comparisons(c, b, key[:2]);return
    if key.startswith('lemma'):
        p = {'T':(0,3), 'U':(-3,0), 'V':(3,0), 'X':(-1.5,1.5), 'Y':(1.5,1.5), 'Z':(4.5,1.5)}
        d = Drawing(c, p, base.txt)
        d.edges([('T','U'),('U','V'),('V','T'),('X','Z'),('V','Z'),('U','Z')])
        if key == 'lemma_sas':
            d.triangle(['T','Y','X'], RED);d.triangle(['V','Y','Z'], BLUE)
            for a,z in [('T','Y'),('Y','V')]:d.tick(a,z)
            for a,z in [('X','Y'),('Y','Z')]:d.tick(a,z,2)
        else:
            d.triangle(['X','U','Z'], RED);d.triangle(['V','Z','U'], BLUE)
            d.tick('X','U');d.tick('V','Z');d.segment('U','Z',GREEN,2)
            d.segment('X','Y',RED,2);d.segment('U','V',BLUE,2)
        d.labels({'T':(-4,8),'U':(-13,-12),'V':(3,-12),'X':(-15,7),'Y':(-4,8),'Z':(4,4)})
        return
    if key in ['h1_sas', 'h2_sas', 'h2_result', 'm1', 'm2']:
        b.diagram(c,key);return
    p = b.geometry(key.split('_')[0])
    if key == 'h1_mid':
        d = Drawing(c,p,base.txt)
        d.edges([('A','B'),('B','C'),('C','D'),('D','A'),('B','H'),('D','H'),('C','H'),('M','E'),('N','E')])
        d.triangle(['B','H','C'],GREEN);d.triangle(['D','H','C'],BLUE)
        d.segment('E','F',RED,2)
        for a,z in [('B','E'),('E','C')]:d.tick(a,z,2)
        for a,z in [('B','F'),('F','H')]:d.tick(a,z)
        d.tick('D','H',3);d.tick('D','C',3)
        d.labels({'M':(-14,5),'N':(-16,4),'A':(-15,0),'B':(-14,-12),'C':(5,-10),'D':(6,-4),'E':(-3,-15),'F':(-13,6),'H':(5,5)})
        return
    if key == 'h3_construct':
        # Length diagram, with four deliberately separated subsegments.
        d = Drawing(c,{k:p[k] for k in ['T','A','F','D','C']},base.txt)
        d.segment('T','C',GRAY,1.2)
        d.segment('T','A',BLUE,2);d.segment('D','C',BLUE,2)
        d.segment('A','F',RED,2);d.segment('F','D',RED,2)
        d.tick('T','A',2);d.tick('D','C',2)
        d.tick('A','F');d.tick('F','D')
        d.labels({k:(-3,10 if k in ['A','D'] else -16) for k in p})
        base.txt(c,'蓝色：TA=DC；红色：AF=FD',28,40,width=230,size=10,lead=13)
        return
    keep = {'h3_tab':['T','A','B','C','E','F','G'],
            'h3_at_a':['T','A','B','F','G'],
            'h3_at_f':['T','A','B','F','G'],
            'h3_gfd':['A','F','D','G'],
            'h3_final':['A','F','D','G']}[key]
    p = {k:p[k] for k in keep};d=Drawing(c,p,base.txt)
    offsets={'T':(-15,5),'A':(-14,-3),'B':(-15,-12),'C':(4,-12),'E':(-3,-15),'F':(6,-8),'G':(-3,8),'D':(5,-8)}
    if key == 'h3_tab':
        d.edges([('T','C'),('B','C'),('A','B'),('G','B'),('G','E')])
        d.triangle(['T','A','B'],BLUE)
        d.segment('T','B',RED,1.7);d.segment('F','E',RED,1.7)
        d.tick('T','A');d.tick('A','B')
        d.angle('T','B','A','60°',RED,16);d.angle('F','E','C','60°',RED,16)
    elif key == 'h3_at_a':
        d.edges([('T','F'),('G','B')]);d.segment('T','B',GRAY,.8,True)
        d.angle('A','T','B','60°',BLUE,17);d.angle('A','G','F','60°',RED,17)
    elif key == 'h3_at_f':
        d.edges([('T','F'),('G','B')]);d.segment('T','B',BLUE,1.7);d.segment('F','G',RED,1.7)
        d.triangle(['A','G','F'],RED)
        d.angle('T','B','A','60°',BLUE,16);d.angle('F','A','G','60°',RED,16)
        d.tick('A','G');d.tick('G','F');d.tick('A','F')
    else:
        d.edges([('A','D'),('A','G'),('G','D'),('G','F')])
        if key == 'h3_gfd':
            d.triangle(['G','F','D'],BLUE);d.tick('G','F');d.tick('F','D')
            d.angle('F','G','D','120°',BLUE,20)
            d.angle('G','F','D','30°',BLUE,21);d.angle('D','F','G','30°',BLUE,26)
        else:
            d.triangle(['A','G','D'],RED);d.segment('G','F',BLUE,1.5)
            d.angle('G','A','F','60°',RED,17);d.angle('G','F','D','30°',BLUE,33)
            d.right('G','A','D',GREEN)
    d.labels(offsets)


def render_figures(b):
    for s in LESSONS:
        buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(260,220));figure(c,s['key'],b);c.save()
        pdf=buf.getvalue();path=b.ROOT/'teaching_figures'/s['key']
        path.with_suffix('.pdf').write_bytes(pdf)
        doc=fitz.open(stream=pdf,filetype='pdf')
        doc[0].get_pixmap(matrix=fitz.Matrix(3,3)).save(path.with_suffix('.png'))


def heading(c,subtitle,page):
    base.header(c,'全等与中点：逐步配图教师详解',subtitle,page,revision='2026-10-17 · 详解修订版')


def lesson_page(c,s,page,b):
    heading(c,s['group']+'｜一页一个关键结论',page)
    y=base.txt(c,s['title'],18*MM,254*MM,size=12.5,lead=18)
    y=base.txt(c,'为什么这样想：'+s['why'],18*MM,y-6,size=10.5,lead=16)
    if y<225*MM:raise ValueError('Motivation overflow: '+s['key'])
    c.saveState();c.translate(49*MM,132*MM);c.scale(112*MM/260,94.77*MM/220);figure(c,s['key'],b);c.restoreState()
    y=base.txt(c,'看图／作图：'+s['action'],18*MM,126*MM,size=9.5,lead=14)
    y=base.txt(c,s['proof'],18*MM,min(y-7,111*MM),size=10.5,lead=17)
    if y<43*MM:raise ValueError('Proof overflow: '+s['key'])
    c.setStrokeColorRGB(*BLUE);c.setLineWidth(.6);c.line(18*MM,42*MM,192*MM,42*MM)
    y=base.txt(c,'本页结论：'+s['result'],18*MM,35*MM,size=10.5,lead=16)
    y=base.txt(c,'讲解提醒：'+s['check'],18*MM,y-4,size=9.5,lead=14)
    if y<16*MM:raise ValueError('Conclusion overflow: '+s['key'])
    c.showPage()


def overview(c,page,b):
    heading(c,'三问压轴题｜先核对题面与读图顺序',page)
    y=base.txt(c,'本版怎样阅读',18*MM,252*MM,size=12,lead=18)
    y=base.txt(c,'每一步都分成“为什么这样想—图上怎样看—逐条证明—本页结论”。先备引理可按学生进度选择讲解；三问均给出完整理由，不默认孩子会从复杂图中自行认出对应角。',18*MM,y-5,size=10.5,lead=16)
    y=base.txt(c,'原题（原图所示位置）',18*MM,y-10,size=11,lead=17)
    y=base.txt(c,b.HARD,18*MM,y-4,size=10,lead=17)
    b.image_fit(c,b.ROOT/'sources/challenge_630.png',18*MM,86*MM,174*MM,52*MM)
    base.txt(c,'读图先记住：\n图a：M、N是延长线上的交点；图b：O=AB与CD的交点。\n图c：G—A—B共线，A—F—D—C共线；本问延长AE至H，使EH=EA。\n各问辅助点H分别定义。图b按原图补充的交点定义及出处见README。',18*MM,76*MM,size=10,lead=17)
    c.showPage()


RECAP = [
    ('第（1）问：从全等到等角',
     '倍长BF至H → △AFB≌△DFH → DH=CD且AB∥DH → 在△BHC中得EF∥CH → △DHC等腰 → 分别对应M、N处的角 → ∠BME=∠CNE。'),
    ('第（2）问：同一构造，重新辨认角',
     '仍倍长BF至H → DH=CD、AB∥DH、MN∥CH → ∠OMN=∠DCH、∠ONM=∠DHC → M、N两角相等 → OM=ON。只能确定等腰。'),
    ('第（3）问：三个三角形，各有不同作用',
     '延长AE至H，使EH=EA → △AEB≌△HEC → CH=CD且CH∥AB → △ADH中EF∥DH → △DHC等边 → 两组平行把60°转到△AGF，使它等边 → GF=AF=FD → △GFD等腰，得两个30° → 在G处相加60°+30°，所以△AGD直角。'),
    ('教师追问及可核对的回答',
     '问：△DHC怎样连到△AGD？答：先通过AG∥CH、GF∥DH，把60°转到△AGF，得到GF=AF=FD。\n问：能否得到△DHC等边就直接说△AGD直角？答：不能，必须补上△AGF等边及△GFD等腰的推理。\n问：GF=FD从哪来？答：△AGF等边给GF=AF，原中点给AF=FD。\n问：直角在哪里？答：G处，因为∠AGD=∠AGF+∠FGD=60°+30°。'),
    ('讲课时的用法',
     '先让学生在原图上指出对应的三角形、边、角，再展示下一页。讲后遮住详解，要求学生重新倍长中线作H，并复述每一个等号的理由。第三问也可取T走另一条路线，但T不是必须的辅助点。'),
]


def recap(c,page):
    heading(c,'讲完后的复盘｜用同一题检查是否真正理解',page)
    y=252*MM
    for title,body in RECAP:
        y=base.txt(c,title,18*MM,y,size=11.5,lead=18)
        y=base.txt(c,body,18*MM,y-5,size=10.5,lead=17)-13
    if y<22*MM:raise ValueError('Recap overflow')
    c.showPage()


INTRO = [
    ('本次修订了什么', '三问共12个图文步骤，另附两页中点引理。第三问现采用用户提出的倍长AE法，完整证明△DHC等边，再借△AGF连到△AGD。原T点法是另一种选法，原先“必须另取T”的说法过于绝对，现已纠正。学生题面与分值保持一致。'),
    ('两题的定位与安排', '题1是中等题，建议10—12分钟；题2是综合压轴题，建议25—35分钟。两题独立完成约40—45分钟，再用约45分钟讲解，余下时间用于批改、追问和遮住答案后重建辅助线。'),
    ('先备知识', '全等SAS、平行线与角、等腰和等边三角形、中点。若中点连线性质尚未学，先看本版两页引理；证明只用两次SAS，无需相似、勾股定理或根式。'),
    ('答案与评分', '题1：（1）BC=CF+CD；（2）BC=CF-CD，各6分。题2：（1）∠BME=∠CNE，6分；（2）OM=ON，6分；（3）△AGD直角，直角在G，12分。第三问建议：倍长AE及全等4分、△DHC等边2分、△AGF等边2分、等腰角度与直角结论4分。'),
    ('来源与文件', '原题、原图与固定版本出处保留在README及sources。本版图形为独立教学重绘。除这份完整教师版，另提供只含三问压轴题的challenge_detailed.pdf、Word和在线图文版，便于手机阅读。'),
]


def word_and_markdown(b,challenge_only):
    name='challenge_detailed' if challenge_only else 'extra_teacher'
    title='三问压轴题：一页一步教师详解' if challenge_only else '两道补充题：逐步配图教师详解'
    doc=base.word_base(title)
    doc.sections[0].footer.paragraphs[0].text='详解修订版｜2026-10-17｜出处与编排说明见README'
    normal=doc.styles['Normal'];normal.paragraph_format.space_after=Pt(4)
    normal.paragraph_format.line_spacing=1.12
    parts=['# '+title,'题目来源与编排说明见[README](README.md)。']
    doc.add_heading(title,0)
    if not challenge_only:
        for title,body in INTRO:
            doc.add_heading(title,2);doc.add_paragraph(body);parts.extend(['## '+title,body])
        for s in b.MEDIUM_STEPS:
            doc.add_page_break();doc.add_heading('题1｜'+s['title'],1)
            doc.add_paragraph(s['action']);doc.add_picture(str(b.ROOT/'teaching_figures'/f"{s['key']}.png"),width=Cm(10.5))
            doc.add_paragraph(s['proof']);doc.add_paragraph('结论：'+s['result'])
            parts.extend(['## 题1｜'+s['title'],f"![步骤图](teaching_figures/{s['key']}.png)",s['proof'],'**结论：** '+s['result']])
        doc.add_page_break()
    doc.add_heading('三问压轴题｜题面与读图',1);doc.add_paragraph(b.HARD)
    doc.add_picture(str(b.ROOT/'sources/challenge_630.png'),width=Cm(16))
    parts.extend(['## 三问压轴题｜完整题面',b.HARD,'![原题三图](sources/challenge_630.png)',
                  '阅读顺序：未学中点连线性质先看两页引理；已学可直接从第（1）问开始。原题保持不变，下面重写完整解释。'])
    for s in LESSONS:
        doc.add_page_break();doc.add_heading(s['group']+'｜'+s['title'],1)
        doc.add_paragraph('为什么这样想：'+s['why']);doc.add_picture(str(b.ROOT/'teaching_figures'/f"{s['key']}.png"),width=Cm(10.8))
        doc.add_paragraph('看图／作图：'+s['action'])
        doc.add_paragraph(s['proof']);doc.add_paragraph('本页结论：'+s['result']);doc.add_paragraph('讲解提醒：'+s['check'])
        parts.extend(['## '+s['group']+'｜'+s['title'],'**为什么这样想：** '+s['why'],
                      f"![本步放大图](teaching_figures/{s['key']}.png)",'**看图／作图：** '+s['action'],
                      s['proof'].replace('\n','\n\n'),'**本页结论：** '+s['result'],'**讲解提醒：** '+s['check']])
    doc.add_page_break();doc.add_heading('三问复盘与教师追问',1)
    parts.append('## 三问复盘与教师追问')
    for title,body in RECAP:
        doc.add_heading(title,2);doc.add_paragraph(body);parts.extend(['### '+title,body.replace('\n','\n\n')])
    doc.save(b.ROOT/(name+'.docx'))
    (b.ROOT/(name+'.md')).write_text('\n\n'.join(parts)+'\n',encoding='utf-8')


def build(b):
    render_figures(b)
    for challenge_only in [False,True]:
        path=b.ROOT/('challenge_detailed.pdf' if challenge_only else 'extra_teacher.pdf')
        c=canvas.Canvas(str(path),pagesize=b.PAGE);page=1
        if not challenge_only:
            heading(c,'教师版｜本次修订与课堂安排',page);y=252*MM
            for title,body in INTRO:
                y=base.txt(c,title,18*MM,y,size=11.5,lead=18)
                y=base.txt(c,body,18*MM,y-5,size=10.5,lead=17)-12
            if y<24*MM:raise ValueError('Intro overflow')
            c.showPage();page+=1
            heading(c,'题1：中等题｜原解保留',page)
            b.block(c,b.MEDIUM_STEPS[0],250);b.block(c,b.MEDIUM_STEPS[1],140)
            c.showPage();page+=1
        overview(c,page,b);page+=1
        for s in LESSONS:
            lesson_page(c,s,page,b);page+=1
        recap(c,page);c.save()
        word_and_markdown(b,challenge_only)
    # Short, directly shareable extract of the user's AE construction.
    c=canvas.Canvas(str(b.ROOT/'third_ae_solution.pdf'),pagesize=b.PAGE)
    parts=['# 第（3）问：倍长AE法',
           '这条辅助线思路由用户提出。延长AE过E至H，使EH=EA；H按本问重新定义。T点法仍可使用，但不是必须的选法。',
           b.HARD.split('（3）',1)[1],
           '连接△DHC与△AGD的关键中间结构是△AGF：先证它等边，得到GF=AF=FD，再利用等腰△GFD。']
    for page,s in enumerate([s for s in LESSONS if s['group']=='第（3）问'],1):
        lesson_page(c,s,page,b)
        parts.extend(['## '+s['title'],'**为什么这样想：** '+s['why'],
                      f"![本步图](teaching_figures/{s['key']}.png)",'**作图／看图：** '+s['action'],
                      s['proof'].replace('\n','\n\n'),'**结论：** '+s['result']])
    c.save()
    (b.ROOT/'third_ae_solution.md').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
