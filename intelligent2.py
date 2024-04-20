"""written by huange on 2024年4月18日19:36:03"""
"""This is my own website"""
"""https://github.com/huange888/huange888"""
"""以下代码主要是负责推算每个乘客对每个司机的取消概率 可参考论文的3.1具体公式实现"""
import numpy as np
import pandas as pd

# 读取数据
passgenerAddress = "static/passenger.xlsx"
df_passenger = pd.read_excel(passgenerAddress)
driverAddress = "static/driverSimulate.xlsx"
df_driver = pd.read_excel(driverAddress)

class Calculate:
    def __init__(self):
        self.priceTaxi = 0.0
        self.priceEcar = 0.0
        self.priceCancel = 0.0
        self.Time = 0.0
        self.timezero = 0.0
        self.length = 0.0
        self.priceCancelHead = 0.0
        self.priceWait = 0.0
        self.time1Ecar = 0.0
        self.tpie = 0.0
        self.tpiepie = 0.0

    #从外部自定义参数
    def setInfo(self,priceTaxi,priceEcar,priceCancel,Time,timezero):
        self.priceTaxi = priceTaxi
        self.priceEcar = priceEcar
        self.priceCancel = priceCancel
        self.Time = Time
        self.timezero = timezero
    #从passenger表中获取参数
    def setPassenger(self,length,priceCancelHead,priceWait):
        self.length = length
        self.priceCancelHead = priceCancelHead
        self.priceWait = priceWait

    #从driverSimulate表中获取参数
    def setDriver(self,time1Ecar):
        self.time1Ecar = time1Ecar

    #以下为获取参数

    def getTpie(self):
        ##以下信息计算得到
        self.tpie = self.time1Ecar - ((self.priceTaxi - self.priceEcar) * self.length + self.priceCancelHead) / self.priceWait  # 等到网约车和 早于timezero时刻 等到出租车的单位成本一致 对应的时间
        return self.tpie

    def getTpiepie(self):
        self.tpiepie = self.time1Ecar - (((self.priceTaxi - self.priceEcar) * self.length) + self.priceCancel) / self.priceWait  # 等到网约车和 晚于timezero时刻 等到出租车的单位成本一致 对应的时间
        return self.tpiepie

    def predictCancelRate(self):
        # 确保tpie和tpiepie的值已经计算
        self.getTpie()
        self.getTpiepie()
        # 计算预测的取消率
        cancelRate = 0.0
        if self.tpie < 0:
            cancelRate = 0.0
        elif self.tpie > self.timezero and self.tpie>0:
            cancelRate = (self.time1Ecar*self.priceWait - (self.priceTaxi - self.priceEcar)*self.length + self.priceCancelHead) / (self.Time*self.priceWait)
        elif self.tpie>self.timezero and self.time1Ecar > self.tpie and self.tpiepie < self.timezero:
            scancelRate = self.timezero / self.Time
        elif (self.tpie>self.timezero and self.time1Ecar > self.tpie and self.tpiepie > self.timezero and self.time1Ecar > self.tpiepie ) or (self.tpie>self.time1Ecar and self.tpiepie > self.timezero and self.time1Ecar > self.tpiepie):
            cancelRate = self.time1Ecar*self.priceWait  - (self.priceTaxi - self.priceEcar)*self.length + self.priceCancel / (self.Time*self.priceWait)
        elif self.tpie > self.time1Ecar and self.tpiepie > self.time1Ecar:
            cancelRate = self.time1Ecar / self.Time

        if cancelRate > 1:
            return 1
        else:
            return cancelRate

# 创建Calculate类的实例
calculate_instances = np.zeros(len(df_passenger) * len(df_driver)).reshape(len(df_driver), len(df_passenger))

# 外部获取参数
base_info = {
    'priceTaxi': 2,
    'priceEcar': 1.8,
    'priceCancel': 3.0,
    'Time': 10,
    'timezero': 3
}

# 遍历driver DataFrame的每一行
for i, driver_row in enumerate(df_driver.iterrows()):
    # 创建Calculate对象
    calculate_instance = Calculate()

    # 设置基本信息
    calculate_instance.setInfo(**base_info)

    # 设置司机信息
    calculate_instance.setDriver(driver_row[1]['predictWaitTime'])

    # 遍历passenger DataFrame的每一行
    for j, passenger_row in enumerate(df_passenger.iterrows()):
        # 设置乘客信息
        calculate_instance.setPassenger(
            length=passenger_row[1]['length'],
            priceCancelHead=passenger_row[1]['priceCancelHead'],
            priceWait=passenger_row[1]['priceWait']
        )

        # 计算预测取消率并存储在对应的位置
        cancel_rate = calculate_instance.predictCancelRate()
        calculate_instances[i, j] = cancel_rate

# 输出所有的预测取消率
print(calculate_instances)

# 假设 calculate_instances 是一个 NumPy 数组，我们将其转换为 pandas DataFrame
df_cancel_rates = pd.DataFrame(calculate_instances, columns=[f'Passenger_{i+1}' for i in range(len(df_passenger))])

# 为 DataFrame 设置行索引
df_cancel_rates.index = [f'Driver_{i+1}' for i in range(len(df_driver))]

# 打印转换后的 DataFrame
print(df_cancel_rates)
df_cancel_rates.to_excel('static/cancel_rates.xlsx', index=False)
