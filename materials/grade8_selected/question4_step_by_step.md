# 第4题：逐步配图与步骤答案

2026-10-13更新。原题出处与原图见[README](README.md)。教学图为独立重绘，辅助线与结论按步骤呈现。

## 第4题：逐步图解

### （1）第1步：PM是哪一个三角形的中点连线？

![该步的图形与辅助线](teaching_figures/q4a1.png)

**作图：** 先只突出△DCE，PM用红色画出。

题目说P是DC中点，M是DE中点。

所以DP=PC，DM=ME。

PM连接△DCE的两边中点。

由中点连线性质：

PM∥CE，PM=CE/2。

若学生未学此性质，先讲附录配图证明。

**本步结论：** 第一条关系：PM∥CE，PM=CE/2。

### （1）第2步：PN属于另一个三角形

![该步的图形与辅助线](teaching_figures/q4a2.png)

**作图：** 现在改为突出△DCB，PN用红色画出。

P仍是DC中点，但N是BC中点。

所以DP=PC，BN=NC。

PN连接△DCB的两边中点。

因此PN∥DB，PN=DB/2。

注意：PM与PN分别属于两个不同的大三角形。

**本步结论：** 第二条关系：PN∥DB，PN=DB/2。

### （1）第3步：先用初始位置得出答案

![该步的图形与辅助线](teaching_figures/q4a3.png)

**作图：** 观察未旋转的图：D在AB上，E在AC上。

BD=AB-AD，CE=AC-AE。

AB=AC，AD=AE，所以BD=CE。

AB⊥AC，因此BD⊥CE。

结合前两步，PM=CE/2=BD/2=PN；PM∥CE、PN∥BD，所以PM⊥PN。

**本步结论：** 第（1）问：PM=PN，PM⊥PN。

### （2）第1步：连接BD、CE，证明等长

![该步的图形与辅助线](teaching_figures/q4sas.png)

**作图：** 连BD、CE；红色△BAD与蓝色△CAE作对照。

图2中∠BAC=∠DAE=90°，且D在∠BAC内部。

∠BAD=90°-∠DAC。

∠CAE=90°-∠DAC。

所以∠BAD=∠CAE。

AB=AC，AD=AE，故△BAD≌△CAE（SAS）。

**本步结论：** BD=CE；对应顶点是B与C、A与A、D与E。

### （2）第2步：用角度一步步证明垂直

![该步的图形与辅助线](teaching_figures/q4angles.png)

**作图：** 延长BD与CE交于T；突出△BCT，令x=∠ABD。

由刚才全等，∠ACE=∠ABD=x。

等腰直角△ABC中，∠ABC=∠BCA=45°。

∠CBT=45°-x；

∠BCT=45°+x。

所以∠BTC=180°-(45°-x)-(45°+x)=90°。

这里使用图2的点与角位置。

**本步结论：** BD⊥CE。“两边相等”本身不能直接推出垂直。

### （2）第3步：旋转后PM仍是中点连线

![该步的图形与辅助线](teaching_figures/q4pm.png)

**作图：** 旋转图中单独突出△DCE；突出DP、PC与DM、ME。

D、E的位置改变了，但P始终是DC中点，M始终是DE中点。

因此在新位置的△DCE中，仍然有

PM∥CE，PM=CE/2。

不需要判断PM在图上看起来是水平还是斜着。

**本步结论：** 旋转后依然：PM∥CE，PM=CE/2。

### （2）第4步：旋转后PN仍属于△DCB

![该步的图形与辅助线](teaching_figures/q4pn.png)

**作图：** 只突出△DCB及红色PN，确认P、N分别在哪两边。

P是DC中点，N是CB中点。

所以在新位置的△DCB中，

PN∥DB，PN=DB/2。

两条小线段的长度与方向，分别由CE和DB决定。

**本步结论：** 旋转后依然：PN∥DB，PN=DB/2。

### （2）第5步：合并等长、垂直两个结论

![该步的图形与辅助线](teaching_figures/q4result.png)

**作图：** 突出小三角形PMN，在P处标直角。

因为BD=CE，

PM=CE/2=BD/2=PN。

因为BD⊥CE，且PN∥BD、PM∥CE，

所以PM⊥PN。

PM与PN相等并互相垂直，故△PMN是等腰直角三角形。

**本步结论：** 第（2）问：△PMN为等腰直角三角形，直角顶点为P。

### （3）第1步：先把面积写成BD的式子

![该步的图形与辅助线](teaching_figures/q4area.png)

**作图：** 突出两条直角边PM、PN，各标为BD/2。

自由旋转时，绕A逆时针转90°始终把B对应到C、D对应到E，所以BD与CE始终等长且垂直。

于是PM=PN=BD/2。

S△PMN=(1/2)×PM×PN

=(1/2)×(BD/2)×(BD/2)

=BD²/8。

**本步结论：** 面积只随BD的长度改变；BD越长，面积越大。

### （3）第2步：BD最多多长？

![该步的图形与辅助线](teaching_figures/q4bound.png)

**作图：** 单独画B、A、D及AB=10、AD=4。

从B经过A到D是折线，BD是直接连接B、D的线段。

因此BD≤BA+AD=10+4=14。

一般不共线的位置严格小于14。

要等于14，必须让B、A、D依次共线，也就是A在B与D之间。

**本步结论：** BD的上界为14；必须检查这个位置能否通过旋转得到。

### （3）第3步：画出达到最大值的完整位置

![该步的图形与辅助线](teaching_figures/q4max.png)

**作图：** 把AD旋转到AB的反向延长线上；重画E、M、P、N。

自由旋转允许D、A、B依次共线。

此时BD=DA+AB=4+10=14。

CE=14，PM=PN=14/2=7。

S△PMN=(1/2)×7×7=49/2。

图中小三角形仍然是等腰直角三角形，没有退化。

**本步结论：** 第（3）问：最大面积49/2；D在AB的反向延长线上时取得。
