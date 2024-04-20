"""written by huange on 2024年4月18日19:36:03"""
"""This is my own website"""
"""https://github.com/huange888/huange888"""
"""以下代码主要是计算司机七个属性的权重系数  利用的是DEMATEL方法"""
import math

import numpy as np
import pandas as pd

# 读取Excel文件中的直接影响矩阵
relateMetrixAdd = "static/relateMatrix.xlsx"
df_relateMetrix = pd.read_excel(relateMetrixAdd)

# 将DataFrame转换为NumPy数组
M = df_relateMetrix.values

# 归一化直接影响矩阵M
N = M / np.max(M)

# 计算综合影响矩阵T
I = np.identity(len(M))  # 单位矩阵
T = N * (I - N)  # 计算T的初始值


# 计算影响度D和被影响度C
D = T.sum(axis=1)  # 每一行的和
C = T.sum(axis=0)  # 每一列的和


# 计算中心度和原因度
Centrality = D + C
Causality = D - C

#计算重要度 gamaH
gamaH = []
for i in range(len(Centrality)):
    gamaH.append(math.sqrt(Centrality[i]*Centrality[i]+Causality[i]*Causality[i]))
gamaH= np.array(gamaH)

#计算权重
weight = []
for i in range(len(Centrality)):
    weight.append(gamaH[i]/sum(gamaH))
weight = np.array(weight)


# 将结果转换为DataFrame
resultMetrix = pd.DataFrame({
    'Influence Degree': D,  # 影响度
    'Being Influenced Degree': C,  # 被影响度
    'Centrality': Centrality,  # 中心度
    'Causality': Causality , # 原因度
    'gamaH' : gamaH , #重要度
    'weight' :weight #权重
})

# 打印结果
print(resultMetrix)
resultMetrix.to_excel("static/resultMatrix.xlsx", index=False)
