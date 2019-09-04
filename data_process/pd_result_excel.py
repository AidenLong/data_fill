# -*- coding utf-8 -*- #

import pandas as pd

data = pd.read_excel('小程序更新包-0808.xlsx')

row_num, column_num = data.shape  # 数据共有多少行，多少列
print(row_num, column_num)
print('the sample number is %s and the column number is %s' % (row_num, column_num))
# 这里我们的数据共有210000行，假设要让每个文件1万行数据，即分成21个文件
print(data.iloc[0:2, :])
for i in range(0, 21):
    save_data = data.iloc[i * 5000:(i + 1) * 5000, :]  # 每隔1万循环一次
    file_name = './result/小程序更新包-0808_' + str(i) + '.xlsx'
    save_data.to_excel(file_name, sheet_name='public opinion', index=False)
