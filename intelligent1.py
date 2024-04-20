"""written by huange on 2024年4月18日19:36:03"""
"""This is my own website showing about my main information"""
#以下是个人主页信息
"""https://github.com/huange888/huange888"""
#如下是仓库地址
# https://github.com/huange888/two-sided-matching-method

import pandas as pd
#模拟数据 simulate
# 设置最大显示行数和列数
pd.options.display.max_rows = 10  # 设置为None表示显示所有行
pd.options.display.max_columns = 10  # 设置为None表示显示所有列
passgenerAddress = "static/passenger.xlsx"
df_passenger= pd.read_excel(passgenerAddress)
df_passenger.columns=['length', 'priceCancelHead', 'priceWait']
print(df_passenger)

driverAddress = "static/driver.xlsx"
df_driver = pd.read_excel(driverAddress)
df_driver.columns=['serviceScore', 'gender', 'isSmoke', 'carEnvironment', 'complainTimes',
       'driveYears', 'predictWaitTime', 'noChargeTime']
print(df_driver)

# 假设的等级划分标准
def change1(data):
    score = int(data)
    if score >= 100:
        return 7
    elif score >= 95:
        return 6
    elif score >= 90:
        return 5
    elif score >= 85:
        return 4
    elif score >= 80:
        return 3
    elif score >= 75:
        return 2
    elif score >= 70:
        return 1
    else:
        return 'No Grade'

df_driver['carEnvironment'] = df_driver['serviceScore'].apply(change1)

# 打印更新后的carEnvironment列
print(df_driver['carEnvironment'])

def change2(data):
    score = int(data)
    if score >= 100:
        return 3
    elif score >= 95:
        return 4
    elif score >= 90:
        return 6
    elif score >= 85:
        return 7
    elif score >= 80:
        return 8
    elif score >= 75:
        return 9
    elif score >= 70:
        return 10
    else:
        return 'No Grade'

df_driver['complainTimes'] =  df_driver['serviceScore'].apply(change2)
print(df_driver['complainTimes'])
#有无吸烟
def change3(data):
    score = int(data)
    if score >= 85:
        return 0
    else:
        return 1

df_driver['isSmoke'] = df_driver['serviceScore'].apply(change3)
print(df_driver['isSmoke'])
#预计等待时间
def change4(data):
    score = int(data)
    if score >= 100:
        return 3
    elif score >= 95:
        return 4
    elif score >= 90:
        return 5
    elif score >= 85:
        return 6
    elif score >= 80:
        return 7
    elif score >= 75:
        return 8
    elif score >= 70:
        return 9
    else:
        return 'No Grade'

df_driver['predictWaitTime'] = df_driver['serviceScore'].apply(change4)
print(df_driver['predictWaitTime'])
#性别
def change5(data):
    score = int(data)
    if score >= 80:
        return 1
    else:
        return 0
df_driver['gender']  = df_driver['serviceScore'].apply(change5)
print(df_driver['gender'])

def change6(data):
    score = int(data)
    if score >= 100:
        return 20
    elif score >= 95:
        return 16
    elif score >= 90:
        return 14
    elif score >= 85:
        return 12
    elif score >= 80:
        return 8
    elif score >= 75:
        return 4
    elif score >= 70:
        return 2
    else:
        return 'No Grade'

df_driver['driveYears'] = df_driver['serviceScore'].apply(change6)
print(df_driver['driveYears'])

df_driver.to_excel('static/driverSimulate1.xlsx',index=False)