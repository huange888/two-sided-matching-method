import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def single_objective_optimization(U, length, cancel_rate, pe, v1, v2):
    m, n = U.shape
    # 生成一个随机的 0-1 矩阵
    x = np.random.randint(0, 2, (m, n))

    # 确保每个司机和每个乘客只匹配一次
    for i in range(m):
        if np.sum(x[i, :]) > 1:
            # 找到重复匹配的乘客索引
            duplicate_matches = np.where(x[i, :] == 1)[0]
            # 随机选择一个匹配并取消其他匹配
            keep_match = np.random.choice(duplicate_matches)
            x[i, duplicate_matches] = 0
            x[i, keep_match] = 1

    for j in range(n):
        if np.sum(x[:, j]) > 1:
            # 同上，找到重复匹配的司机索引
            duplicate_matches = np.where(x[:, j] == 1)[0]
            keep_match = np.random.choice(duplicate_matches)
            x[duplicate_matches, j] = 0
            x[keep_match, j] = 1
    # 计算 Z1 和 Z2
    Z1 = U * (1 - cancel_rate) * x
    Z2 = length * pe * (1 - cancel_rate) * x
    Z1_SUM = np.sum(U * (1 - cancel_rate) * x)
    Z2_SUM = np.sum(length * pe * (1 - cancel_rate) * x)

    best_sum = Z1_SUM + Z2_SUM
    # 归一化 Z1 和 Z2
    Z1_prime = (Z1 - np.min(Z1)) / (np.max(Z1) - np.min(Z1))
    Z2_prime = (Z2 - np.min(Z2)) / (np.max(Z2) - np.min(Z2))

    # 计算加权和得到最终的目标函数 Z
    Z = v1 * np.sum(Z1_prime) + v2 * np.sum(Z2_prime)

    return Z, x ,best_sum

def optimize_with_iterations(U, length, cancel_rate, pe, v1, v2, max_iterations=10000, tolerance=10000):
    best_sum = 0
    best_x = None
    iteration_history = []  # 记录每次迭代的 best_sum
    no_improvement_count = 0  # 用于跟踪连续无改进的迭代次数

    for i in range(max_iterations):
        Z, x, current_sum = single_objective_optimization(U, length, cancel_rate, pe, v1, v2)
        print("current_sum :", current_sum)
        if current_sum > best_sum:
            best_sum = current_sum

            best_x = x
            no_improvement_count = 0
            iteration_history.append(best_sum)
        else:
            no_improvement_count += 1

        # 如果连续多次迭代没有改进，或者达到最大迭代次数，停止迭代
        if no_improvement_count >= tolerance or i == max_iterations - 1:
            break

    return best_sum, best_x, iteration_history


# 设置参数
priceEcar = 1.8
v1 = 0.5
v2 = 0.5


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

# 执行优化并获取结果
best_sum, assignment_matrix, iteration_history = optimize_with_iterations(
    np_prospect_matrix, np_length, np_cancel_rates, priceEcar, v1, v2
)

print("Final Objective Function Value:", best_sum)
print("Assignment Matrix:\n", assignment_matrix)

# 将结果保存到 Excel
df_assignment = pd.DataFrame(assignment_matrix)
df_assignment.to_excel("static/assignment.xlsx", index=False)

# 绘制迭代图像
plt.figure(figsize=(10, 5))
plt.plot(iteration_history, marker='o')
plt.title('Best Sum per Iteration')
plt.xlabel('Iteration')
plt.ylabel('Best Sum')
plt.show()


