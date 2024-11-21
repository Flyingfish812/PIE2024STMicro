1. 根据MPN和MANUFACTURER NAME两个参数一起唯一确定一个元件（通过check.ipynb进行验证）。代表某个厂家生产的某一种类型的元件。在opamps-xref.csv中，STMicro MPN和STMicro Name唯一确定一个元件，Competitor MPN和Competitor Name唯一确定一个元件，与opamps-features.csv中的MPN和MANUFACTURER对照找到对应元件，提取特征数据。如果找不到对应元件，则存入not_found表格中。（not_found.ipynb文件）在opamps-xref.csv中去掉not_found的元件，得到opamps-xref-cleaned.csv。
2. 数据抽样，根据Cross Reference Type的值进行分组抽样，忽略SF类别，如果在抽样中遇到not_found中的元件则跳过。数量多于1000的类别抽取1000个样本，否则抽取全部样本。
3. 将 STMicro元件的特征与 Competitor元件的特征拼接为一个完整的特征向量。对于数值型特征（浮点型、整数型），比较 STMicro 和Competitor 在某特征的数值，通过(大数- 小数) / 大数 得到一个0到1之间的特征差异值。对于字符串类型的Supplier_Package特征，特征不一致赋值1，一致赋值0。
4. 使用 opamps-xref.csv 中的Cross Reference Type作为目标标签。将 Cross Reference Type 转化为连续相似性分数。D = 0.2; C = 0.5; B = 0.8; A = 1.0. 将B/Downgrade和 B/Upgrade 都看做B，将C/Upgrade 和 C/Downgrade 都看做C。将拼接后的特征向量输入随机森林回归器，为了弥补不同类别样本数量的不均衡，考虑样本权重。

对数据组的需要：
1. 在清洗数据时，输出opamps-xref.csv，涉及的元件在opamps-features.csv中都能找到。
2. 在opamps-features.csv中根据MPN和MANUFACTURER NAME两个参数能唯一确定一个元件，不存在重复条目。
3. 改善样本数量不均衡问题

1.在opamps-features.csv中发现，存在MPN相同，MANUFACTURER NAME不同的情况，可以理解为不同厂家生产的同一种零件。那么可以说，(MPN, MANUFACTURER)可以唯一确定一个元件。
2.在opamps-xref.csv中，(STMicro MPN,STMicro Name)可以对应一个STMicro生产的元件，(Competitor MPN,Competitor Name)可以对应一个Competitor生产的元件。Cross Reference Type是这两个元件的相似度分类相似度类别？upgraded和downgraded代表两种产品哪种更好，但其对应的相似度是相同的？
4.数据不平衡

