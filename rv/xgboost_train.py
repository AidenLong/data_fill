# -*- coding utf-8 -*- #

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from xgboost import XGBRegressor

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
X = datas.iloc[:, 1:-1]
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

# cv_params = {'n_estimators': [400, 500, 600, 700, 800]}
# other_params = {'learning_rate': 0.1, 'n_estimators': 500, 'max_depth': 5, 'min_child_weight': 1, 'seed': 0,
#                 'subsample': 0.8, 'colsample_bytree': 0.8, 'gamma': 0, 'reg_alpha': 0, 'reg_lambda': 1}
#
# model = XGBRegressor(**other_params)
# optimized_GBM = GridSearchCV(estimator=model, param_grid=cv_params, scoring='r2', cv=5, verbose=1, n_jobs=4)
# optimized_GBM.fit(X_train, Y_train)
# evalute_result = optimized_GBM.grid_scores
# print('每轮迭代运行结果:{0}'.format(evalute_result))
# print('参数的最佳取值：{0}'.format(optimized_GBM.best_params_))
# print('最佳模型得分:{0}'.format(optimized_GBM.best_score_))

# xgboost
# params = [1, 2, 3, 4, 5, 6]
# test_scores = []
# for param in params:
#     clf = XGBRegressor(max_depth=param)
#     test_score = np.sqrt(-cross_val_score(clf, X_train, Y_train, cv=100, scoring='neg_mean_squared_error'))
#     test_scores.append(np.mean(test_score))
# plt.plot(params, test_scores)
# plt.title('max_depth vs CV Error')
# plt.show()

xgb = XGBRegressor(max_depth=6)
xgb.fit(X_train, Y_train)

## 模型保存/持久化
from sklearn.externals import joblib

joblib.dump(xgb, './model/lr/data_xgboost.model')  # 将模型保存

y_final = xgb.predict(X_test)
y_final_train = xgb.predict(X_train)
print('训练集R2', r2_score(Y_train, y_final_train))
print('测试集R2', r2_score(Y_test, y_final))

mse = np.average((y_final - Y_test) ** 2)
rmse = np.sqrt(mse)
print('rmse', rmse)

## 预测值和实际值画图比较
t = np.arange(len(X_test))
plt.figure(facecolor='w')  # 建一个画布，facecolor是背景色
plt.plot(t, Y_test, 'r-', linewidth=2, label='真实值')
plt.plot(t, y_final, 'g-', linewidth=1, label='预测值')
plt.legend(loc='upper left')  # 显示图例，设置图例的位置
plt.title("线性回归预测真实值图", fontsize=20)
plt.grid(b=True)  # 加网格
plt.show()
