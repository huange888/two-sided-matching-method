# two-sided-matching-method
A personalized ride-sharing two-sided matching decision-making method considering passenger no-show behavior

## 参考论文地址：[1]包伊宁,陈希,张文博.考虑乘客爽约行为的网约车个性化司乘双边匹配决策方法[J/OL].工业工程与管理,1-15[2024-04-20].
http://kns.cnki.net/kcms/detail/31.1738.t.20240409.0956.003.html
对应目录paper/Chinese_paper
## 感受
# 历时八天  有两天都在看英文文献 
对应目录 paper/English_paper
后面的五天或者六天都是看着中文文献 来看公式来写python代码
![image](https://github.com/huange888/two-sided-matching-method/assets/118048444/ab40922a-e258-444b-9b62-ad07372ced33)

# 在2024年4月20日17:07:45 终于完成了这个智慧决策的大作业
# 第一次感受到了博士论文的复杂度

## 不足
# 在后面的优化算法那一块只是用了随机生成 0 1 矩阵并且做了个迭代 人为的判断最优化函数  
# 这点存在不足 可以优化的地方就是利用ortools来解决这个最优化问题 但是我下载了 官网好像有问题 一直在维护中
# 我的用法就是暴力模拟法 疯狂迭代
# 利用其他包的优化算法也可以实现这个最优化的司乘问题的双边匹配

## 个人地址
https://github.com/huange888/two-sided-matching-method

# 迭代次数图片  只保留了实现最优化的迭代次数 实际上是迭代了一万或者几万次
![png_1](https://github.com/huange888/two-sided-matching-method/assets/118048444/15f781b6-4853-4dd2-98e4-dedc6ea406e8)

#以下图片是最后的匹配结果

![png_2](https://github.com/huange888/two-sided-matching-method/assets/118048444/e81de200-e191-4dc1-ab3a-79fc5b0ce8b7)

## 个人仓库地址：
https://github.com/huange888/two-sided-matching-method

## 运行方式
# 从intelligent1.py 到 intelligent8.py依次运行
# 其中intelligent7.py的 assignment.xlsx每次都会变化 得到的最优值对应static/mappping_result.xlsx 为最优值674
# 但是算法用的是暴力随机迭代法 可以用更加高级的算法来迭代 得到最优化模型
