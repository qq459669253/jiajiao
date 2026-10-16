# 补充两题：一道中等题，一道综合压轴题

按“初二上、已学全等，常规证明较稳，主要失分在原卷24、25题后问”的情况，补充两道**现成题**。本包包含学生卷、逐步配图答案和原始出处。

- [学生版 PDF（3页，含证明续页）](extra_student.pdf) / [可编辑Word](extra_student.docx)
- [教师版 PDF（8页，11张步骤图）](extra_teacher.pdf) / [可编辑Word](extra_teacher.docx)
- [在线逐步看图与答案](extra_teacher.md)
- [整套下载ZIP](extra_two_problems.zip)

GitHub文件页面点击 **Download raw file／下载原始文件** 即可下载。新增两题暂配静态步骤图，不属于原四题的交互页面。

## 这两题怎样分档

| 题目 | 难度定位 | 核心要求 | 建议独立用时 |
|---|---|---|---|
| 题1：直角旋转与线段和差，2问 | 中等 | 找出一次SAS全等，将CF变成BD，按点的顺序作加减 | 10—12分钟 |
| 题2：中点、等腰与特殊三角形，3问 | 综合压轴档 | 前两问倍长BF、利用中点制造平行与等腰；末问重新取辅助点T，连续得到等边与等腰结构，再拼出直角 | 25—35分钟 |

题2按辅助线层数、位置变化及末问独立构造的要求，与原卷24题的中点构造、25题的特殊三角形综合要求相近。它侧重证明与迁移，不包含最短路径问。

两题均无需勾股定理、根式运算、相似、圆或函数。题2用到三角形中点连线的平行性质；如果尚未学，先给出该性质，再观察能否主动构造可用的中点。教师版末页说明两次SAS证明，完整引理配图也可参考[原教师版第17—18页](../grade8_selected/selected_teacher.pdf)。

本次编排满分36分：题1两问各6分；题2三问分别6、6、12分。分值与建议时间为本次安排，不是原资料标注。若放进两小时家教，建议用两题替换原卷的一部分，不把六道综合题同时塞进原50分钟摸底。

## 答案速查（学生可先不看）

题1：（1）BC=CF+CD；（2）BC=CF-CD。

题2：（1）∠BME=∠CNE；（2）OM=ON，△OMN为等腰三角形；（3）△AGD为直角三角形，∠AGD=90°、∠ADG=30°，且AD=2AG。每一步的辅助线和理由见教师版。

## 可核对的来源

题1节选自[higyg/middleschoolmath-ebook](https://github.com/higyg/middleschoolmath-ebook)，版本 `3b4b7cd8463f4a5bb4ce727911d3c818dc17f1bc`：

- [原题T22-A01-08及原答案](https://github.com/higyg/middleschoolmath-ebook/blob/3b4b7cd8463f4a5bb4ce727911d3c818dc17f1bc/ItemBankBody/T22-01.tex)。本次仅选第（1）（2）问，不包含其第（3）问。
- 原图为 `ItemBankFigures/T22-A01-08-01.pdf`、`T22-A01-08-02.pdf`，本包在 `sources/medium_01.pdf`、`sources/medium_02.pdf` 保留原文件。原答案明确给出BD=CF以及第（2）问BC=CF-CD。
- 上游未为此题标注具体考试，不另编学校、年份或“真题”身份。

题2来自[Onion12138/math](https://github.com/Onion12138/math)，版本 `5b13610d78b8dd9b47a69846e0086484f1fff94d`：

- 《初中数学总复习讲义》1.5.1，**习题6.25.11**，印刷页79／PDF第84页。
- [完整原讲义PDF](https://github.com/Onion12138/math/blob/5b13610d78b8dd9b47a69846e0086484f1fff94d/初中数学总复习讲义.pdf) / [原始TeX](https://github.com/Onion12138/math/blob/5b13610d78b8dd9b47a69846e0086484f1fff94d/test.tex#L1995)。
- 原图为 `picture/630.png`，本包保存为 `sources/challenge_630.png`。
- 原讲义此题未附完整答案；本包独立推导并核对三问证明，不将本包答案说成上游原解。

## 编排改动与许可

2026-10-17：题1选取原题前两问；题2保留原三问。重新编号和排版，增加本次分值、用时、教学安排及独立推导的分步答案。题1第（2）问原要求直接写结论，本次为诊断要求同时写理由。题2图b按原图补写O为AB与CD交点，并明确M、N、O互异，避免把退化点组当作三角形；其余几何条件不变。题面的原图保持原文件内容，教学步骤图独立重绘。

原题TeX摘录见 `sources/original_problems.tex`。题1的上游许可GPL v3、题2的上游许可LPPL 1.3c，全文保留于sources。摘录与原图保留各自来源及许可；本次独立编排、题解和生成脚本以GPL-3.0提供。原作者不负责本选编的错误或支持。

重建请使用完整仓库（脚本复用上一套资料的绘图与排版工具）：

```bash
python -m pip install reportlab python-docx pymupdf
python materials/grade8_extra/build_extra.py
```
