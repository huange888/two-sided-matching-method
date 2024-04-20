import numpy as np
import pandas as pd

relateMetrixAdd = "D:/A-EditedFiles/PythonApplication/my_intelligent/static/relateMetrix.xlsx"
df_relateMetrix = pd.read_excel(relateMetrixAdd)


# 假设我们有一个直接影响矩阵M
# M = np.array([
#     [0, 2, 0, 3],
#     [0, 0, 5, 1],
#     [4, 0, 0, 0],
#     [2, 1, 0, 0]
# ])
# 将DataFrame转换为NumPy数组
# 假设Excel文件中的矩阵没有标题行和标题列，且矩阵数据从第一行第一列开始
M = df_relateMetrix.iloc[:, :].values
print(M)
# 归一化直接影响矩阵M
N = M / np.max(M)
print(N)
# 计算综合影响矩阵T
I = np.identity(len(N))  # 单位矩阵
T = (N @ (I - N))  # 计算T，这里使用了 @ 运算符来代替 np.dot() 或 np.linalg.multi()
# 迭代计算T的近似值，直到收敛
# for _ in range(3000):  # 这里迭代1000次，根据实际情况调整
#     T_new = T * (I - N)
#     T = T_new + N  # 更新T的值
#     # 检查T是否收敛，如果变化很小，则认为已经收敛
#     if np.allclose(T, T_new):
#         break

# T = N * (I - N)  # 计算T的初始值
# for _ in range(3000):  # 这里迭代3000次，根据实际情况调整
#     T_new = T * (I - N)  # 计算新的N的幂次
#     T += T_new  # 将新的N的幂次累加到T中
#     if np.allclose(T, T_new, atol=1e-6):  # 检查T是否收敛
#         break
print(T)
# 计算影响度D和被影响度C
D = T.sum(axis=1)  # 每一行的和
C = T.sum(axis=0)  # 每一列的和

# 计算中心度和原因度
Centrality = D + C
Causality = D - C

# 将结果转换为DataFrame
# D = pd.Series(D, name='Influence Degree')
# C = pd.Series(C, name='Being Influenced Degree')
# Centrality = pd.Series(Centrality, name='Centrality')
# Causality = pd.Series(Causality, name='Causality')

print("Influence Degree 影响度(D):\n", D)
print("Being Influenced Degree 被影响度(C):\n", C)
print("Centrality 中心度(D+C):\n", Centrality)
print("Causality 原因度(D-C):\n", Causality)

