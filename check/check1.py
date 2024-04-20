import pandas as pd
# 设置最大显示行数和列数
pd.options.display.max_rows = 10  # 设置为None表示显示所有行
pd.options.display.max_columns = 10  # 设置为None表示显示所有列
passgenerAddress = "D:/A-EditedFiles/PythonApplication/my_intelligent/static/passenger.xlsx"
df_passenger= pd.read_excel(passgenerAddress)
df_passenger.columns=['length', 'priceCancelHead', 'priceWait']
print(df_passenger)

driverAddress = "D:/A-EditedFiles/PythonApplication/my_intelligent/static/driverSimulate.xlsx"
df_driver = pd.read_excel(driverAddress)
df_driver.columns=['serviceScore', 'gender', 'isSmoke', 'carEnvironment', 'complainTimes',
       'driveYears', 'predictWaitTime', 'noChargeTime']
print(df_driver)



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
calculate_instance = Calculate()
#外部获取参数
calculate_instance.setInfo(
    priceTaxi=2,  # 假设出租车价格为10.0
    priceEcar=1.8,    # 假设电动汽车价格为8.0
    priceCancel=3.0,    # 假设取消订单的价格为3.0
    Time=10,            #总时间为十分钟
    timezero= 3   #免责取消的时间为3分钟
)

# 假设行驶距离为  未知 在passenger表中  length
# 假设取消订单的心理价格未知  在pass表  priceCancelHead
# 假设等待单位时间成本  未知 在pass表中 priceWait
# calculate_instance.setPassenger(length=3,priceCancelHead=2,priceWait=1.2)

# 假设网约车的等待时间未知 在driverSimulate表中  time1Ecar 对应 表中的 predictWaitTime 字段
# calculate_instance.setDriver(time1Ecar=3)

# print(calculate_instance.getTpie())
# print(calculate_instance.getTpiepie())
# print(calculate_instance.predictCancelRate())

#从driverSimulate表获取参数
predictWaitTime = df_driver['predictWaitTime'].tolist()
passenger = ['length', 'priceCancelHead', 'priceWait']
driver = ['serviceScore', 'gender', 'isSmoke', 'carEnvironment', 'complainTimes',
       'driveYears', 'predictWaitTime', 'noChargeTime'] #数组下标的第六个

print(df_passenger.iloc[0][0])
print(df_driver.iloc[0][6])
# print(predictWaitTime)
#从passenger表获取参数



rate = []
for i in range(len(df_driver['predictWaitTime'])):
    calculate_instance.setDriver(df_driver.iloc[i][6]) #第i行的第6个 即predictWaitTime
    for j in range(len(df_passenger['length'])) :
            calculate_instance.setPassenger(length=df_passenger.iloc[j][0],priceCancelHead=df_passenger.iloc[j][1],priceWait=df_passenger.iloc[j][2])
            rate.append(calculate_instance.predictCancelRate())
print(rate)


class Driver:
    def __init__(self, serviceScore, gender, isSmoke, carEnvironment, complainTimes, driveYears, predictWaitTime,
                 noChargeTime):
        self.serviceScore = serviceScore
        self.gender = gender
        self.isSmoke = isSmoke
        self.carEnvironment = carEnvironment
        self.complainTimes = complainTimes
        self.driveYears = driveYears
        self.predictWaitTime = predictWaitTime
        self.noChargeTime = noChargeTime


##intelligent5
# prospect_score_list = []
# columns = [f'Passenger_{i+1}' for i in range(len(df_passExpectation))]
# for profit_index, profit_row in df_profit_serviceScore.iterrows():
#     l1 = []
#
#     for loss_index , loss_row in df_loss_serviceScore.iterrows():
#
#         prospect = Prospect()
#         prospect.setParameter(alpha=0.88,beta=0.88,eta=2.55)
#         prospect.getAllParameter()
#         for j in columns:
#             prospect.setInfoFromProfit(profit_row[j])
#             prospect.setInfoFromLoss(loss_row[j])
#             prospect_score = prospect.calculateProspect()
#             l1.append(prospect_score)
#     prospect_score_list.append(l1)

# print(len(prospect_score_list))
# print(len(prospect_score_list[0]))
# print(prospect_score_list)

# df_prospect_score = pd.DataFrame(prospect_score_list,columns=columns)
# df_prospect_score.to_excel('df_prospect_score.xlsx',index=False)
#在代码的最后面
# prospectMatrix = ProspectMatrix()
# result = prospectMatrix.calculateProspectScore(df_profit_serviceScore, df_loss_serviceScore)
# df_result = pd.DataFrame(result, columns=[f'Passenger_{i + 1}' for i in range(len(df_passExpectation))])
# print(df_result)
# df_result.to_excel('static/prospect_score.xlsx', index=False)

#intelligent7的代码
def optimize(self): #定义优化器  实现最优化算法
        x0 = np.ones((self.m, self.n))  # 开始猜测，初始化一个全为1的矩阵，其行数为m，列数为n
        c = np.zeros((self.m * self.n,))  # 成本函数系数，这里初始化为0，因为我们通常在求解线性规划时使用负系数来最大化目标函数
        bounds = [(0, 1) for _ in range(self.m * self.n)]  # 变量的界限，这里为每个决策变量x_ij设置了一个范围从0到1的界限，
                                                            # 意味着每个决策变量可以是0或1，符合二进制变量的定义

        A = np.zeros((len(self.constraints(x0)), self.m * self.n))
        b = np.zeros(len(self.constraints(x0)))

        # 初始化约束矩阵A和约束向量b。A的行数由约束的数量决定，列数由决策变量的数量决定（m*n）。
        # b是与A对应的约束向量，其长度与A的行数相同。

        # 填充约束矩阵A和右边界向量b
        for i, constraint in enumerate(self.constraints(x0)):
            A[i, :] = constraint(x0)
            b[i] = 1

        # 这里的constraint是一个函数，它接受决策变量的数组x0作为输入，并返回一个与x0同长度的数组，
        # 该数组表示由x0构成的点满足约束时的值。如果该值为正，则表示满足约束。

        # 使用线性规划求解器求解
        result = linprog(c, A_eq=A, b_eq=b, bounds=bounds, method='highs')

        # 返回优化结果
        return result


def constraints(self, x): #x的值 是司机和乘客匹配的值 当x为1时代表匹配 为0时代表不匹配
        constraints = []
        for j in range(self.n):
            constraints.append(np.sum(x[:, j]) <= 1)
        for i in range(self.m):
            constraints.append(np.sum(x[i, :]) <= 1)
        return constraints