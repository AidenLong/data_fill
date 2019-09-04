# -*- coding utf-8 -*- #

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import r2_score

# 加载数据
path = './data/result_city.xlsx'
# 没有混合类型时通过low_memory=F调用更多内存，加快效率
df = pd.read_excel(path)
print(df.shape)

# 获取前5行数据
# print(df.head())
# 查看格式信息
# print(df.info())

# 异常数据处理（异常数据过滤）
new_df = df.replace('?', np.nan)  # 替换非法字符为np.nan
datas = new_df.dropna(axis=0, how='any')  # 只要有一个数据为空，就进行行删除操作
# print(datas.describe().T)  # 观察数据的多种统计指标


# 获取x和y变量
X = datas.iloc[:, 0:-1]
Y = datas['REPRICE']

'''
    对数据集进行测试集合训练集划分
    X：特征矩阵（类型一般是DataFrame）
    Y：特征矩阵对应的Label（类型一般是Series）
    test_size：对X/Y进行划分的时候，测试集合的数据占比，是一个（0-1）之间的float类型的值
    random_state：数据分割是基于随机器进行分割的,该参数给定随机数种子；
        给一个值(int类型)的作用就是保证每次分割所产生的数数据集是完全相同的
'''
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

# xgboost
params = [1, 2, 3, 4, 5, 6]
test_scores = []
for param in params:
    clf = XGBRegressor(max_depth=param)
    test_score = np.sqrt(-cross_val_score(clf, X_train, Y_train, cv=100, scoring='neg_mean_squared_error'))
    test_scores.append(np.mean(test_score))
plt.plot(params, test_scores)
plt.title('max_depth vs CV Error')
plt.show()

xgb = XGBRegressor(max_depth=50)
xgb.fit(X_train, Y_train)

y_final = np.expm1(xgb.predict(X_test))
y_final_train = np.expm1(xgb.predict(Y_train))
print('训练集R2' + r2_score(Y_train, y_final_train))
print('测试集R2' + r2_score(Y_test, y_final))
# 提交结果
submission_df = pd.DataFrame(data={'Id': X_test.index, 'SalePrice': y_final})
# print (submission_df.head(10))
print(submission_df)
submission_df.to_csv('submission_xgboosting.csv', columns=['Id', 'SalePrice'], index=False)
