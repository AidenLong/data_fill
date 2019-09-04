# -*- coding utf-8 -*- #

# data = [1, 2, 3, 4, 5]
# index = data.index(2)
# print(index)
#
# new_data = [0] * len(data)
# new_data[index] = 1
# print(new_data)

import pandas as pd
import numpy as np

# 通过行标签索引行数据  index可以为整数
data = [[1, 2, 3], [4, 5, 6]]
index = [0, 1]
columns = ['a', 'b', 'c']
df = pd.DataFrame(data=data, index=index, columns=columns)
print(df)
print(df.iloc[:, 0:-1])
print('=====')
print(next(df.iterrows())[1])
print(df.keys().array)
print('.................')
