"""writen time: 2024年4月18日20:38:43"""
"""This is my own website"""
"""https://github.com/huange888/huange888"""
"""以下代码主要是根据乘客对司机的七个属性的前景矩阵得出一个综合的前景值矩阵"""
import numpy as np
import pandas as pd

# 乘客期待矩阵的地址
passExpectAdd = "static/passengerExpectation.xlsx"
df_passExpectation = pd.read_excel(passExpectAdd)
#评价因子
factors = ["serviceScore", "gender","isSmoke","carEnvironment","complainTimes","driveYears","predictWaitTime"]
addressList = []
for i in factors:
    addressList.append('static/ProspectMatrix_'+i+'.xlsx')
# print(addressList)
prospect_serviceScore = pd.read_excel(addressList[0])
prospect_gender = pd.read_excel(addressList[1])
prospect_isSmoke = pd.read_excel(addressList[2])
prospect_carEnvironment = pd.read_excel(addressList[3])
prospect_complainTimes = pd.read_excel(addressList[4])
prospect_driveYears = pd.read_excel(addressList[5])
prospect_predictWaitTime = pd.read_excel(addressList[6])

#转化为numpy数组
prospect_serviceScore_numpy = prospect_serviceScore.values
prospect_gender_numpy = prospect_gender.values
prospect_isSmoke_numpy = prospect_isSmoke.values
prospect_carEnvironment_numpy = prospect_carEnvironment.values
prospect_complainTimes_numpy = prospect_complainTimes.values
prospect_driveYears_numpy = prospect_driveYears.values
prospect_predictWaitTime_numpy = prospect_predictWaitTime.values



class Normalizer:
    def __init__(self, min_val=0, max_val=1):
        self.min_val = min_val
        self.max_val = max_val

    def normalize(self, data):
        """
        对输入的numpy数组进行归一化处理
        :param data: numpy数组
        :return: 归一化后的numpy数组
        """

        # 获取数据的最大值和最小值
        min_val = np.min(data)
        max_val = np.max(data)

        # 进行归一化处理
        normalized_data = (data - min_val) / (max_val - min_val)

        # # 缩放到指定的[min_val, max_val]区间  目前不太需要
        # normalized_data = normalized_data * (self.max_val - self.min_val) + self.min_val

        return normalized_data

#weight权重
resultMatrix = pd.read_excel("static/resultMatrix.xlsx")
weight = resultMatrix['weight'].tolist()

# 所有属性归一化处理
factors_numpy = [prospect_serviceScore_numpy, prospect_gender_numpy, prospect_isSmoke_numpy, prospect_carEnvironment_numpy,
            prospect_complainTimes_numpy, prospect_driveYears_numpy]
prospectMatrix = []
for i in range(len(factors_numpy)):
    normalizer = Normalizer()
    normalized_matrix = normalizer.normalize(factors_numpy[i])
    weighted_matrix = normalized_matrix * weight[i]  # 乘以权重
    prospectMatrix.append(weighted_matrix)
    # print(normalized_matrix)
prospectMatrix = np.array(prospectMatrix)

# 将所有加权矩阵相加得到前景值矩阵
prospectValueMatrix = np.sum(prospectMatrix, axis=0)

prospectValueMatrix = pd.DataFrame(prospectValueMatrix,columns=[f'Passenger_{i + 1}' for i in range(len(df_passExpectation))])
# 输出前景值矩阵和权重，检查结果
print(prospectValueMatrix)
print(weight)
prospectValueMatrix.to_excel("static/ProspectValueMatrix.xlsx",index=False)

"""#至此 已成艺术！"""
"""不过接下来还有更大的问题要解决 这才是重头戏"""
