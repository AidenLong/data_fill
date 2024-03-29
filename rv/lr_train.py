# -*- coding:utf-8 -*-
# 引入所需要的全部包
import time

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler
## 模型保存/持久化
from sklearn.externals import joblib

## 设置字符集，防止中文乱码
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False

# 加载数据
start = time.time()
path = './data/result.xlsx'
# 没有混合类型时通过low_memory=F调用更多内存，加快效率
df = pd.read_excel(path)
print(df.shape)
end = time.time()
print(end - start)

# 获取前5行数据
# print(df.head())
# 查看格式信息
# print(df.info())

# 异常数据处理（异常数据过滤）
new_df = df.replace('?', np.nan)  # 替换非法字符为np.nan
datas = new_df.dropna(axis=0, how='any')  # 只要有一个数据为空，就进行行删除操作
# print(datas.describe().T)  # 观察数据的多种统计指标


# 获取x和y变量
X = datas.iloc[:, 1:-1]
Y = datas['REPRICE']

'''
    对数据集进行测试集合训练集划分
'''
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1)
# print(X_train.shape)
# print(X_test.shape)
# print(Y_train.shape)
# print(X_train.describe().T)

'''
    数据标准化
    如果一个API名字中有predict，那么就表示进行数据预测，会有一个预测结果输出
'''
ss = StandardScaler()
X_train = ss.fit_transform(X_train)  # 训练并转换
X_test = ss.transform(X_test)  # 直接使用在模型构建数据上进行一个数据标准化操作

# 模型训练
lr = ElasticNetCV(alphas=np.logspace(0, 1, 10), l1_ratio=[.1, .5, .7, .9, .95, 1], fit_intercept=False)
lr.fit(X_train, Y_train)  # 训练模型
# 模型校验
y_predict = lr.predict(X_test)  # 预测结果

print('训练R2：', lr.score(X_train, Y_train))
print('测试R2：', lr.score(X_test, Y_test))
mse = np.average((y_predict - Y_test) ** 2)
rmse = np.sqrt(mse)
print('rmse', rmse)

# joblib.dump(ss, './model/lr/data_ss.model')  # 将标准化模型保存
joblib.dump(lr, './model/lr/data_lr.model')  # 将模型保存

## 预测值和实际值画图比较
t = np.arange(len(X_test))
plt.figure(facecolor='w')  # 建一个画布，facecolor是背景色
plt.plot(t, Y_test, 'r-', linewidth=2, label='真实值')
plt.plot(t, y_predict, 'g-', linewidth=1, label='预测值')
plt.legend(loc='upper left')  # 显示图例，设置图例的位置
plt.title("线性回归预测真实值图", fontsize=20)
plt.grid(b=True)  # 加网格
plt.show()
