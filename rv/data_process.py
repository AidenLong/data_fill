# -*- coding utf-8 -*- #
import pickle

import pandas as pd
from rv import data_utils

data = pd.read_excel('./data/data.xlsx')

'''
    描述， 内部key， 收集时间， 网络来源， 上牌时间， 档位（自动或者手动）， 发动机， 商家（商家、个人）， 消费者
    爬取的url， 车源id， 排量， 信息发布时间， spcode， 网络价格， 车龄（月）， 行驶距离， 每月行驶距离
    信息发布时间， 城市， 品牌， 系列， 省份， 品牌code， 系列code， 系列描述中文， 
    车辆类型code， 款式年份， 款式月份， 中文描述， 引擎描述， 批发价格
    零售价格，  新车价格， 比率， web-price x ratio， 数据库中的残值率， 样本的残值率， 款式年月组合， spkey
    
'''
names = ['comb', 'vehiclekey', 'gathertime', 'websource', 'registrationtime', 'gear0', 'engine', 'business', 'seller',
         'url', 'cheyuanhao', 'emission0', 'publishtime0', 'spcode', 'web_price', 'age', 'mileage', 'monthly_mileage',
         'publishtime', 'city', 'make', 'family', 'province', 'MakeCode', 'FamilyCode', 'FamilyDescriptionChinese',
         'VehicleTypeCode', 'YearGroup', 'MonthGroup', 'DescriptionChinese', 'EngineDescription', 'GoodWholesale',
         'GoodRetail', 'NewPrice', 'RATIO', 'REPRICE', 'RBRV', 'SARV', 'RVdif', 'aa', 'spkey'
         ]
row_num, column_num = data.shape  # 数据共有多少行，多少列

important_names = ['gear0', 'engine', 'business', 'age', 'mileage', 'monthly_mileage',
                   'NewPrice', 'VehicleTypeCode', 'aa']
important_data = data[important_names]
# print(important_data.describe())
print(important_data.head())
# print(important_data['age'])

'''
    缺失值排量如何填补的问题
'''

# print('处理挂牌时间')
# # 挂牌时间处理为距离当前时间的月数
# important_data["registrationtime"] = important_data["registrationtime"].apply(
#     lambda x: pd.Series(data_utils.distance_now_months_by_date(x)))

print('处理档位信息')
# 档位方式（自动挡2，手动挡1）
important_data["gear0"] = important_data["gear0"].apply(
    lambda x: pd.Series(data_utils.gear_handle(x)))

print('处理出售方信息')
# 档位方式（自动挡2，手动挡1）
important_data["business"] = important_data["business"].apply(
    lambda x: pd.Series(data_utils.business_handle(x)))

# 排放标准
# 缺失值补充
print('处理排放标准')
    # data_utils.emission_value_fill(data)
    # 同义词替换
    # data["emission0"] = data["emission0"].apply(
    #     lambda x: pd.Series(data_utils.emission_handle(x)))
# one-hot处理
emission0 = pd.get_dummies(data["emission0"])
emission_keys = emission0.keys()
with open("./data/keys/emission_keys.pkl", "wb") as file:
    pickle.dump(emission_keys, file, True)

for key in emission_keys:
    important_data[key] = emission0[key]

# 处理省市数据
print('处理省市数据')
# data['province'] = data['province'].map(lambda x: data_utils.province_value_handle(x))
# data['province_city'] = data['province'].str.cat(data['city'], sep='-')
# one-hot处理
city = pd.get_dummies(data["city"])
city_keys = city.keys()
with open("./data/keys/city_keys.pkl", "wb") as file:
    pickle.dump(city_keys, file, True)
for key in city_keys:
    important_data[key] = city[key]

print('处理品牌系列数据')
# 处理品牌系列数据
data['makeCode_familyCode'] = data['MakeCode'].str.cat(data['FamilyCode'])
# one-hot处理
makeCode_familyCode = pd.get_dummies(data["makeCode_familyCode"])
makeCode_familyCode_keys = makeCode_familyCode.keys()
with open("./data/keys/makeCode_familyCode_keys.pkl", "wb") as file:
    pickle.dump(makeCode_familyCode_keys, file, True)
for key in makeCode_familyCode_keys:
    important_data[key] = makeCode_familyCode[key]

print('处理车辆类型数据')
# 处理车辆类型数据
important_data["VehicleTypeCode"] = important_data["VehicleTypeCode"].apply(
    lambda x: pd.Series(data_utils.vehicle_type_code_handle(x)))

print('处理发布时间')
# 发布时间处理为距离当前时间的月数
important_data["aa"] = important_data["aa"].apply(
    lambda x: pd.Series(data_utils.distance_now_months_by_str(x)))

important_data['REPRICE'] = data['REPRICE']

print('end, save to file....')
important_data.to_excel('./data/result.xlsx', sheet_name='result')
