import numpy as np
import pandas as pd
from scipy.optimize import linprog
#读取数据
#综合前景值矩阵
df_prospect_matrix = pd.read_excel("static/ProspectValueMatrix.xlsx")
#转化为np矩阵
np_prospect_matrix = df_prospect_matrix.values #对应U矩阵 综合前景值矩阵
#从passenger表中读取数据  获取length 距离 对应l
df_passenger = pd.read_excel("static/passenger.xlsx")
#转化为np矩阵
np_length = df_passenger['length'].values
#取消概率 从cancel_rates表中获得  对应p
df_cancel_rates = pd.read_excel("static/cancel_rates.xlsx")
np_cancel_rates = df_cancel_rates.values
#定义参数
priceEcar = 1.8 #网约车的单位时间等待成本
v1 = 0.5  # 定义Z1的权重系数v1的值
v2 = 0.5  # 定义Z2权重系数v2的值


class OptimizationModel:
    def __init__(self, U, length, price_Ecar, price_cancel_rate, v1, v2):
        self.m, self.n = U.shape #m n 分别代表行的长度 列的长度
        self.U = U #U是综合前景值矩阵
        self.length = length #l是距离 从passenger表中获得
        self.price_Ecar = price_Ecar #p_e是priceEcar  从外部参数定义获得
        self.price_cancel_rate = price_cancel_rate #p是预测的乘客取消订单的概率 从cancel_rates表中获得
        self.v1 = v1 # 权重系数  转化为线性规划问题 的Z1 权重
        self.v2 = v2 # 转化为线性规划问题 的Z2 权重
        print(self.U)

    def objective(self, x):
        Z1 = np.sum(self.U * (1 - self.price_cancel_rate) * x) # 第一个max值 Z1
        # print("priceCancelRate\n")
        # print(self.price_cancel_rate)
        # print("z1\n")
        # print(Z1)
        Z2 = np.sum(self.length * self.price_Ecar * (1 - self.price_cancel_rate) * x)  # 第二个max值 Z2
        Z1_prime = (Z1 - np.min(Z1)) / (np.max(Z1) - np.min(Z1)) #归一化后的Z1
        Z2_prime = (Z2 - np.min(Z2)) / (np.max(Z2) - np.min(Z2)) #归一化后的Z2
        return self.v1 * Z1_prime + self.v2 * Z2_prime #返回乘以权重系数后的 单线性规划矩阵

    def constraints(self, x):
        # 定义一个内部函数，它将用于创建针对每一列的约束条件
        def constraint_fn(j): #这里的j表示列索引，代表乘客
            # 返回一个lambda函数，这个函数接受变量x（决策矩阵）作为输入
            return lambda x: np.sum(x[:, j]) - 1  #并计算x中第j列的和减去1，这表示每个乘客只能与一个司机匹配

        # 定义另一个内部函数，它将用于创建针对每一行的约束条件
        def constraint_fn2(i): #这里的i表示行索引，代表司机
            # 返回一个lambda函数，这个函数接受变量x作为输入
            return lambda x: np.sum(x[i, :]) - 1 #并计算x中第i行的和减去1，这表示每个司机只能与一个乘客匹配

        constraints_fns = [] # # 初始化一个空列表，用于存储所有的约束条件函数
        for j in range(self.n): ## 对于每一列（每一个乘客），添加一个约束条件函数到列表中

            constraints_fns.append(constraint_fn(j))
        for i in range(self.m): ## 对于每一行（每一个司机），也添加一个约束条件函数到列表中

            constraints_fns.append(constraint_fn2(i))
        return constraints_fns # # 返回包含所有约束条件函数的列表

    def optimize(self):
        x0 = np.zeros((self.m, self.n))  # 通常是全零矩阵作为起始猜测
        c = np.ones((self.m * self.n,))  # 目标函数系数，需要根据实际问题调整
        bounds = [(0, 1) for _ in range(self.m * self.n)]  # 变量界限

        # 构建完整的约束矩阵A_eq和向量b_eq
        A_eq = np.zeros((2 * self.m + 2 * self.n, self.m * self.n))
        b_eq = np.zeros(2 * self.m + 2 * self.n)

        # 添加约束: 每个乘客只能与一个司机匹配
        for j in range(self.n):
            A_eq[2 * self.m + j, j::self.n] = 1
            b_eq[2 * self.m + j] = 1

        # 添加约束：每个司机只能与一个乘客匹配
        for i in range(self.m):
            A_eq[i, ::self.n] = 1
            b_eq[i] = 1

        # 使用线性规划求解器求解
        result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        return result


# 创建优化模型的实例
model = OptimizationModel(np_prospect_matrix, np_length, priceEcar, np_cancel_rates, v1, v2)
# 运行优化过程
result = model.objective(1)
print("result\n")
print(result)
optimization_result = model.optimize()
print(optimization_result)
#转化为矩阵
optimal_values = optimization_result.x
# 创建DataFrame
columns = [f'Variable_{i}' for i in range(len(optimal_values))]
optimal_df = pd.DataFrame([optimal_values], columns=columns)
# 打印结果
# print(optimal_df)
# 将DataFrame保存为Excel文件
# optimal_df.to_excel('static/optimal_solution.xlsx', index=False)