"""written by huange on 2024年4月18日19:36:03"""
"""This is my own website"""
"""https://github.com/huange888/huange888"""
import math

import pandas as pd

# 读取数据
driverAddress = "static/driverSimulate1.xlsx"
df_driver = pd.read_excel(driverAddress)
df_driver.columns = ['serviceScore', 'gender', 'isSmoke', 'carEnvironment', 'complainTimes',
                     'driveYears', 'predictWaitTime', 'noChargeTime']
passExpectAdd = "static/passengerExpectation.xlsx"
df_passExpectation = pd.read_excel(passExpectAdd)

# 先转换类型 便于下列程序判断
df_driver['gender'] = df_driver['gender'].astype(str)

class Compare:
    def __init__(self):
        self.serviceScoreO = 0
        self.serviceScoreE = 0
        self.genderO = 0
        self.genderE = 0
        self.isSmokeO = 0
        self.isSmokeE = 0
        self.carEnvironmentO = 0
        self.carEnvironmentE = 0
        self.complainTimesO = 0
        self.complainTimesE = 0
        self.driveYearsO = 0
        self.driveYearsE = 0
        self.predictWaitTimeO = 0
        self.predictWaitTimeE = 0
        self.UO = 7
        self.UE = 7

    def setInfoFromDriver(self, serviceScore, gender, isSmoke, carEnvironment, complainTimes, driveYears,
                          predictWaitTime):
        self.serviceScoreO = serviceScore
        self.genderO = gender
        self.isSmokeO = isSmoke
        self.carEnvironmentO = carEnvironment
        self.complainTimesO = complainTimes
        self.driveYearsO = driveYears
        self.predictWaitTimeO = predictWaitTime

    def setInfoFromExpectation(self, serviceScore, gender, isSmoke, carEnvironment, complainTimes, driveYears,
                               predictWaitTime):
        self.serviceScoreE = serviceScore
        self.genderE = gender
        self.isSmokeE = isSmoke
        self.carEnvironmentE = carEnvironment
        self.complainTimesE = complainTimes
        self.driveYearsE = driveYears
        self.predictWaitTimeE = predictWaitTime

    def profitEfficiencyType(self, object, expectation):
        if object >= expectation:
            return object - expectation
        else:
            return 0

    def lossEfficiencyType(self, object, expectation):
        if object < expectation:
            return object - expectation
        else:
            return 0

    def TriangularFuzzyNumber(self, uO, UO, uE, UE):
        object1 = max((uO - 1) / UO, 0)
        object2 = uO / uO
        object3 = min((uO + 1) / UO, 1)
        expectation1 = max((uE - 1) / UE, 0)
        expectation2 = uE / UE
        expectation3 = min((UE + 1) / UE, 1)
        result = math.sqrt(
            1 / 3 * ((object1 - expectation1) ** 2 + (object2 - expectation2) ** 2 + (object3 - expectation3) ** 2))
        return result

    def profitLanguageType(self, object, expectation):
        if object <= expectation:
            return 0
        else:
            return self.TriangularFuzzyNumber(uO=object, UO=self.UO, uE=expectation, UE=self.UE)

    def lossLanguageType(self, object, expectation):
        if object < expectation:
            return (-1) * self.TriangularFuzzyNumber(uO=object, UO=self.UO, uE=expectation, UE=self.UE)
        else:
            return 0

    def profitEnumType(self, object, expectation):
        if object == expectation:
            return 1
        #没加str之前 在intelligent5.py运行之前 出现了问题 因为profit_gender全部都是0
        #原来是之前是 {0,1} 导致出现了问题
        elif str(expectation) == "{1,0}":
            return 1
        else:
            return 0

    def lossEnumType(self, object, expectation):
        if object == expectation:
            return 0
        elif str(expectation) == "{1,0}":
            return 0
        else:
            return -1



# 创建7个空列表，每个字段一个，用于存储每个字段的收益和损失矩阵
profit_matrices_serviceScore = []
profit_matrices_gender = []
profit_matrices_isSmoke = []
profit_matrices_carEnvironment = []
profit_matrices_complainTimes = []
profit_matrices_driveYears = []
profit_matrices_predictWaitTime = []

loss_matrices_serviceScore = []
loss_matrices_gender = []
loss_matrices_isSmoke = []
loss_matrices_carEnvironment = []
loss_matrices_complainTimes = []
loss_matrices_driveYears = []
loss_matrices_predictWaitTime = []

# 遍历司机数据框的每一行
for index_driver, row_driver in df_driver.iterrows():
    p1=[]
    p2=[]
    p3=[]
    p4=[]
    p5=[]
    p6=[]
    p7=[]
    d1=[]
    d2=[]
    d3=[]
    d4=[]
    d5=[]
    d6=[]
    d7=[]
    # 遍历乘客期望数据框的每一行
    for index_pass, row_pass in df_passExpectation.iterrows():
        # 创建Compare类实例
        compare = Compare()

        # 将数据输入到Compare类中
        compare.setInfoFromDriver(row_driver['serviceScore'], row_driver['gender'], row_driver['isSmoke'],
                                  row_driver['carEnvironment'],
                                  row_driver['complainTimes'], row_driver['driveYears'], row_driver['predictWaitTime'])
        compare.setInfoFromExpectation(row_pass['serviceScore'], row_pass['gender'], row_pass['isSmoke'],
                                       row_pass['carEnvironment'],
                                       row_pass['complainTimes'], row_pass['driveYears'], row_pass['predictWaitTime'])

        # 计算每个字段的收益
        profit_serviceScore = compare.profitEfficiencyType(row_driver['serviceScore'], row_pass['serviceScore'])
        profit_gender = compare.profitEnumType(row_driver['gender'], row_pass['gender'])
        profit_isSmoke = compare.profitEfficiencyType(row_driver['isSmoke'], row_pass['isSmoke'])
        profit_carEnvironment = compare.profitLanguageType(row_driver['carEnvironment'], row_pass['carEnvironment'])
        profit_complainTimes = compare.profitEfficiencyType(row_driver['complainTimes'], row_pass['complainTimes'])
        profit_driveYears = compare.profitEfficiencyType(row_driver['driveYears'], row_pass['driveYears'])
        profit_predictWaitTime = compare.profitEfficiencyType(row_driver['predictWaitTime'], row_pass['predictWaitTime'])

        loss_serviceScore = compare.lossEfficiencyType(row_driver['serviceScore'], row_pass['serviceScore'])
        loss_gender = compare.lossEnumType(row_driver['gender'], row_pass['gender'])
        loss_isSmoke = compare.lossEfficiencyType(row_driver['isSmoke'], row_pass['isSmoke'])
        loss_carEnvironment = compare.lossLanguageType(row_driver['carEnvironment'], row_pass['carEnvironment'])
        loss_complainTimes = compare.lossEfficiencyType(row_driver['complainTimes'], row_pass['complainTimes'])
        loss_driveYears = compare.lossEfficiencyType(row_driver['driveYears'], row_pass['driveYears'])
        loss_predictWaitTime = compare.lossEfficiencyType(row_driver['predictWaitTime'], row_pass['predictWaitTime'])

        p1.append(profit_serviceScore)
        p2.append(profit_gender)
        p3.append(profit_isSmoke)
        p4.append(profit_carEnvironment)
        p5.append(profit_complainTimes)
        p6.append(profit_driveYears)
        p7.append(profit_predictWaitTime)

        d1.append(loss_serviceScore)
        d2.append(loss_gender)
        d3.append(loss_isSmoke)
        d4.append(loss_carEnvironment)
        d5.append(loss_complainTimes)
        d6.append(loss_driveYears)
        d7.append(loss_predictWaitTime)

    profit_matrices_serviceScore.append(p1)
    profit_matrices_gender.append(p2)
    profit_matrices_isSmoke.append(p3)
    profit_matrices_carEnvironment.append(p4)
    profit_matrices_complainTimes.append(p5)
    profit_matrices_driveYears.append(p6)
    profit_matrices_predictWaitTime.append(p7)

    loss_matrices_serviceScore.append(d1)
    loss_matrices_gender.append(d2)
    loss_matrices_isSmoke.append(d3)
    loss_matrices_carEnvironment.append(d4)
    loss_matrices_complainTimes.append(d5)
    loss_matrices_driveYears.append(d6)
    loss_matrices_predictWaitTime.append(d7)
        # 将计算结果添加到对应字段的列表中

# 创建最终的每个字段的收益和损失矩阵的DataFrame
final_profit_matrix_serviceScore = pd.DataFrame(profit_matrices_serviceScore,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_profit_matrix_gender = pd.DataFrame(profit_matrices_gender,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_profit_matrix_isSmoke = pd.DataFrame(profit_matrices_isSmoke,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_profit_matrix_carEnvironment = pd.DataFrame(profit_matrices_carEnvironment,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_profit_matrix_complainTimes = pd.DataFrame(profit_matrices_complainTimes,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_profit_matrix_driveYears = pd.DataFrame(profit_matrices_driveYears,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_profit_matrix_predictWaitTime = pd.DataFrame(profit_matrices_predictWaitTime,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])

final_loss_matrix_serviceScore = pd.DataFrame(loss_matrices_serviceScore,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_loss_matrix_gender = pd.DataFrame(loss_matrices_gender,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_loss_matrix_isSmoke = pd.DataFrame(loss_matrices_isSmoke,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_loss_matrix_carEnvironment = pd.DataFrame(loss_matrices_carEnvironment,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_loss_matrix_complainTimes = pd.DataFrame(loss_matrices_complainTimes,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_loss_matrix_driveYears = pd.DataFrame(loss_matrices_driveYears,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])
final_loss_matrix_predictWaitTime = pd.DataFrame(loss_matrices_predictWaitTime,columns=[f'Passenger_{i+1}' for i in range(len(df_passExpectation))])

# 保存最终的收益和损失矩阵的DataFrame到Excel文件
final_profit_matrix_serviceScore.to_excel('static/final_profit_matrix_serviceScore.xlsx', index=False)
final_profit_matrix_gender.to_excel('static/final_profit_matrix_gender.xlsx', index=False)
final_profit_matrix_isSmoke.to_excel('static/final_profit_matrix_isSmoke.xlsx', index=False)
final_profit_matrix_carEnvironment.to_excel('static/final_profit_matrix_carEnvironment.xlsx', index=False)
final_profit_matrix_complainTimes.to_excel('static/final_profit_matrix_complainTimes.xlsx', index=False)
final_profit_matrix_driveYears.to_excel('static/final_profit_matrix_driveYears.xlsx', index=False)
final_profit_matrix_predictWaitTime.to_excel('static/final_profit_matrix_predictWaitTime.xlsx', index=False)

final_loss_matrix_serviceScore.to_excel('static/final_loss_matrix_serviceScore.xlsx', index=False)
final_loss_matrix_gender.to_excel('static/final_loss_matrix_gender.xlsx', index=False)
final_loss_matrix_isSmoke.to_excel('static/final_loss_matrix_isSmoke.xlsx', index=False)
final_loss_matrix_carEnvironment.to_excel('static/final_loss_matrix_carEnvironment.xlsx', index=False)
final_loss_matrix_complainTimes.to_excel('static/final_loss_matrix_complainTimes.xlsx', index=False)
final_loss_matrix_driveYears.to_excel('static/final_loss_matrix_driveYears.xlsx', index=False)
final_loss_matrix_predictWaitTime.to_excel('static/final_loss_matrix_predictWaitTime.xlsx', index=False)

# 打印最终的每个字段的收益和损失矩阵的DataFrame
print(final_profit_matrix_serviceScore)
print(final_profit_matrix_gender)
print(final_profit_matrix_isSmoke)
print(final_profit_matrix_carEnvironment)
print(final_profit_matrix_complainTimes)
print(final_profit_matrix_driveYears)
print(final_profit_matrix_predictWaitTime)

print(final_loss_matrix_serviceScore)
print(final_loss_matrix_gender)
print(final_loss_matrix_isSmoke)
print(final_loss_matrix_carEnvironment)
print(final_loss_matrix_complainTimes)
print(final_loss_matrix_driveYears)
print(final_loss_matrix_predictWaitTime)

