# 初二全等与旋转：现有题进阶摸底

本套按学生在原卷选择第10题、填空第16题及第24、25题的失分，选择**现有公开资料中的题目**。保留原条件、数值和原图，重新组卷；不再以自编题作为本次主卷。建议独立做题50分钟，再在两小时家教内选择两个重点讲解。

- [学生版 PDF（5页，含证明续页）](selected_student.pdf)
- [教师版 PDF（19页，逐步配图、辅助线、分条证明与两小时安排）](selected_teacher.pdf)
- [第4题单独图解 PDF（6页，11个步骤）](question4_step_by_step.pdf) / [Word](question4_step_by_step.docx) / [在线逐步看图](question4_step_by_step.md)
- [学生版 Word](selected_student.docx) / [教师版 Word](selected_teacher.docx)
- [全部资料 ZIP](selected_existing_problems.zip)
- [在线阅读答案与教案](selected_teacher.md)
- [新增两题：一道中等题＋一道综合压轴题，含逐步配图答案](https://github.com/qq459669253/jiajiao/tree/main/materials/grade8_extra)
- [四题交互动态图：拖动点、调滑块、自动播放](https://github.com/qq459669253/jiajiao/tree/main/materials/geometry_motion)

GitHub打开文件后，可点击 **Download raw file / 下载原始文件**；ZIP页面也可这样下载。不依赖原来的电脑在线。

2026-10-13更新：四题及中点连线引理共增加30张独立重绘的教学图，每一步均附作图指令、对应的步骤证明和结论。第4题将“PM与PN分别属于哪两个三角形”“BD与CE为什么垂直”“面积怎样达到最大值”分别展开。教师PDF第11—16页是第4题，也可直接读上面的单独文件。所有教学图均提供于 [teaching_figures](teaching_figures)，Word已嵌入图片，在线答案也能逐步看图。

## 选题与失分的对应

| 本卷 | 现有题来源 | 主要诊断 | 建议时间 |
|---|---|---|---|
| 第1题，8分 | 《初中数学总复习讲义》例6.17.2 | 旋转搬移三段长度、固定下界、等号位置；对应原卷选择末题的最值思维 | 10分钟 |
| 第2题，10分 | 同讲义习题6.25.12 | 等边动点、补固定三角形、证明中点轨迹；对应填空末题及大题的辅助线意识 | 10分钟 |
| 第3题，20分 | 同讲义习题6.16.3 | 半角、两次SAS、从基本图到一般图及延长线加减；对应后两道大题的推广与变式 | 15分钟 |
| 第4题，22分 | 公开题库所标2017年河南中考，T22-A01-10 | 直角旋转、中点、面积最值、合法取等；对应原卷第24题 | 15分钟 |

共60分。新增作答要求用于诊断推理，评分不是原试题分值。第1题几何最小值可用CE表示；根式计算需要勾股定理，不计本次60分。第2、4题用到中点连线性质，教师版附两次SAS证明，若学生未学，应补齐后再判断方法掌握情况。

## 可核对的出处

第1—3题来自 [Onion12138/math](https://github.com/Onion12138/math)，版本为 `5b13610d78b8dd9b47a69846e0086484f1fff94d`：

- [完整原讲义 PDF（1.5.1）](https://github.com/Onion12138/math/blob/5b13610d78b8dd9b47a69846e0086484f1fff94d/初中数学总复习讲义.pdf)：第1题印刷页57 / PDF第62页；第2题印刷页79 / PDF第84页；第3题印刷页56 / PDF第61页。
- [原始 TeX](https://github.com/Onion12138/math/blob/5b13610d78b8dd9b47a69846e0086484f1fff94d/test.tex)：题目段落分别位于1405、2005、1354行附近。准确定位请优先用上述例题、习题号。
- 原图文件为 `picture/612.png`、`picture/632.png`、`picture/6107.jpg`，本目录保存为 `sources/figures/onion_*`。

第4题来自 [higyg/middleschoolmath-ebook](https://github.com/higyg/middleschoolmath-ebook)，版本为 `3b4b7cd8463f4a5bb4ce727911d3c818dc17f1bc`：

- [题库原文及原答案 T22-A01-10](https://github.com/higyg/middleschoolmath-ebook/blob/3b4b7cd8463f4a5bb4ce727911d3c818dc17f1bc/ItemBankBody/T22-01.tex#L365)。原题库标注“2017年河南中考”，本次未取得官方试卷对照，因此出处表述保留为“公开题库所标”。
- [原图1](https://github.com/higyg/middleschoolmath-ebook/blob/3b4b7cd8463f4a5bb4ce727911d3c818dc17f1bc/ItemBankFigures/T22-A01-10-01.pdf) / [原图2](https://github.com/higyg/middleschoolmath-ebook/blob/3b4b7cd8463f4a5bb4ce727911d3c818dc17f1bc/ItemBankFigures/T22-A01-10-02.pdf)，本目录保存了原PDF及用于排版的PNG。

这两份资料是公开讲义与题库；不将讲义模板所用校名或标志当作考试学校来源。所有解题链独立核对，第4题最终答案同时与上游原答案一致。

## 编排改动、许可和重建

2026-10-11编排改动：抽取四道题、重新编号、中文和数学符号排版、缩放原图；新增本次分值、建议用时、说明理由的要求、答案证明、教学安排及即时回练。条件、数值与原图几何内容未改。即时回练是遮住答案后重做所选题的关键步骤，不能充当另一套陌生题迁移测试。

2026-10-13编排改动：教师证明改为逐步配图；独立重绘合法位置的教学示意图并增加辅助线、刻痕、角度标注。第4题图2的垂直关系新增角度证明：设x=∠ABD=∠ACE，在△BCT中以45°-x和45°+x求出直角；自由旋转部分另用同向90°旋转说明结论仍成立。新增第4题独立PDF、Word和Markdown；原学生卷保持不变。重绘图是本次解答的教学示意图，不冒充原始试题图。

原题目TeX摘录见 [sources/original_problems.tex](sources/original_problems.tex)。上游讲义附LPPL 1.3c，上游题库附GPL v3，许可全文随包保留于 `sources/LICENSE-Onion-LPPL.txt` 与 `sources/LICENSE-Ebook-GPL.txt`；相应摘录与原图保留上游来源及许可。本次独立编排、解答文本和生成脚本以GPL-3.0提供，无保证。原作者不负责本选编的错误或支持。本选编不是上游原讲义的更新版本。

PDF、Word和ZIP均可用本目录的源文件重建：

```bash
python -m pip install reportlab python-docx pymupdf
python build_selected_pack.py
```

仅更新教师资料、保留现有学生文件：`python build_selected_pack.py --teacher-only`。新增的 `illustrated_teacher.py` 和 `teaching_figures` 随包提供，可重建全部步骤图。

教师版另有在线Markdown，学生题面另有Markdown文本，便于修改和核对。
