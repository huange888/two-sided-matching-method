"""written by huange on 2024年4月18日19:36:03"""
"""This is my own website"""
"""https://github.com/huange888/huange888"""

import pandas as pd

# 乘客期待矩阵的地址
passExpectAdd = "static/passengerExpectation.xlsx"
df_passExpectation = pd.read_excel(passExpectAdd)
# 保存最终的收益和损失矩阵的DataFrame到Excel文件
df_profit_serviceScore = pd.read_excel('static/final_profit_matrix_serviceScore.xlsx')
df_profit_serviceScore.columns = [f'Passenger_{i + 1}' for i in range(len(df_passExpectation))]
df_profit_gender = pd.read_excel('static/final_profit_matrix_gender.xlsx')
df_profit_isSmoke = pd.read_excel('static/final_profit_matrix_isSmoke.xlsx')
df_profit_carEnvironment = pd.read_excel('static/final_profit_matrix_carEnvironment.xlsx')
df_profit_complainTimes = pd.read_excel('static/final_profit_matrix_complainTimes.xlsx')
df_profit_driveYears = pd.read_excel('static/final_profit_matrix_driveYears.xlsx')
df_profit_predictWaitTime = pd.read_excel('static/final_profit_matrix_predictWaitTime.xlsx')

df_loss_serviceScore = pd.read_excel('static/final_loss_matrix_serviceScore.xlsx')
df_loss_gender = pd.read_excel('static/final_loss_matrix_gender.xlsx')
df_loss_isSmoke = pd.read_excel('static/final_loss_matrix_isSmoke.xlsx')
df_loss_carEnvironment = pd.read_excel('static/final_loss_matrix_carEnvironment.xlsx')
df_loss_complainTimes = pd.read_excel('static/final_loss_matrix_complainTimes.xlsx')
df_loss_driveYears = pd.read_excel('static/final_loss_matrix_driveYears.xlsx')
df_loss_predictWaitTime = pd.read_excel('static/final_loss_matrix_predictWaitTime.xlsx')


# 计算前景值
class Prospect():
    def __init__(self):
        self.eta = 0
        self.alpha = 0
        self.beta = 0

    def setParameter(self, eta, alpha, beta):
        self.eta = eta
        self.alpha = alpha
        self.beta = beta

    def setInfoFromProfit(self, profit):
        self.profit = profit

    def setInfoFromLoss(self, loss):
        self.loss = loss

    def getAllParameter(self):
        print(self.alpha, self.beta, self.eta)

    def calculateProspect(self):
        #算法核心如下
        result = self.profit**self.alpha +  ((-1*self.loss)**self.beta)*(-1*self.eta)
        return result


class ProspectMatrix:
    def __init__(self):
        self.info = "ok"

    def calculateProspectScore(self, df_profit, df_loss):
        prospect_score_list = []
        columns = [f'Passenger_{i + 1}' for i in range(len(df_profit.columns))]
        # 假设df_profit和df_loss可以通过某个索引进行匹配
        for profit_index, profit_row in df_profit.iterrows():
            if profit_index in df_loss.index:
                loss_row = df_loss.loc[profit_index]
                prospect_scores = []
                for j in columns:
                    prospect = Prospect()
                    prospect.setParameter(alpha=0.88, beta=0.88, eta=2.55)
                    prospect.setInfoFromProfit(profit_row[j])
                    prospect.setInfoFromLoss(loss_row[j])
                    prospect_score = prospect.calculateProspect()
                    prospect_scores.append(prospect_score)
                prospect_score_list.append(prospect_scores)
        return prospect_score_list

profit_df_list = [df_profit_serviceScore, df_profit_gender,df_profit_isSmoke,df_profit_carEnvironment,df_profit_complainTimes,df_profit_driveYears,df_profit_predictWaitTime]
factors = ["serviceScore", "gender","isSmoke","carEnvironment","complainTimes","driveYears","predictWaitTime"]
loss_df_list = [df_loss_serviceScore,df_loss_gender,df_loss_isSmoke,df_loss_carEnvironment,df_loss_complainTimes,df_loss_driveYears,df_loss_predictWaitTime]
for i in range(len(profit_df_list)):
    prospectMatrix = ProspectMatrix()
    result = prospectMatrix.calculateProspectScore(profit_df_list[i], loss_df_list[i])
    df_result = pd.DataFrame(result, columns=[f'Passenger_{i + 1}' for i in range(len(df_passExpectation))])
    df_result.to_excel(f"static/ProspectMatrix_{factors[i]}.xlsx",index=False)
    print(df_result)

#此时排查出来profit_gender 和 loss_gender矩阵有问题 证明intelligent4代码里面有问题
#2024年4月18日20:10:42  目前已解决问题 就是之前的{0,1} 和 {1,0}搞反了

