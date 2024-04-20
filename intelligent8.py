import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
"""以下代码主要是根据生成的0 1 矩阵 司机乘客匹配矩阵来生成对应的图像信息 进行可视化操作"""
# 读取 Excel 文件
mapping_result = pd.read_excel("static/mapping_result.xlsx")
print(mapping_result)

def find_matching_indices(df):
    indices = np.where(df == 1)
    row_indices = indices[0]
    col_indices = indices[1]
    matching_indices = list(zip(row_indices, col_indices))
    return matching_indices

matching_indices = find_matching_indices(mapping_result)
print("Matching Indices:", matching_indices)

# 绘制散点图
x_positions = [pair[1] for pair in matching_indices]  # 乘客索引作为 x 轴位置
y_positions = [pair[0] for pair in matching_indices]  # 司机索引作为 y 轴位置

# 增加点的大小
plt.scatter(x_positions, y_positions, marker='o', s=100)

# 绘制垂直线
for x, y in zip(x_positions, y_positions):
    max_line_height = y  # 设置垂直线的最大高度为对应的散点的 y 值
    plt.axvline(x=x, color='gray', linestyle='--', linewidth=0.5, ymin=0, ymax=max_line_height)
    # 将文本放在垂直线之上
    plt.text(x=x, y=y + 0.05, s=f'{y}', va='bottom', ha='center')

plt.title('Driver-Passenger Matching')
plt.xlabel('Passenger')
plt.ylabel('Driver')

# 设置 x 轴的刻度位置和标签
plt.xticks(range(len(mapping_result.columns)))

# 设置 x 轴刻度标签的倾斜角度
plt.gca().set_xticklabels([f'{i+1}' for i in range(len(mapping_result.columns))], rotation=45)

# 设置 x 轴的范围，使其适应列的数量
plt.xlim(-0.5, len(mapping_result.columns) - 0.5)

# 显示图形
plt.tight_layout()  # 调整布局以适应标签和标题
plt.show()

