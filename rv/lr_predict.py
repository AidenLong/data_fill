# -*- coding utf-8 -*- #

import pickle
from rv import data_utils
from sklearn.externals import joblib

with open('./data/keys/city_keys.pkl', 'rb') as file:
    city_keys = pickle.load(file)
    city_keys = [x for x in city_keys]
    print(city_keys)

with open('./data/keys/emission_keys.pkl', 'rb') as file:
    emission_keys = pickle.load(file)
    emission_keys = [x for x in emission_keys]
    print(emission_keys)

with open('./data/keys/makeCode_familyCode_keys.pkl', 'rb') as file:
    makeCode_familyCode_keys = pickle.load(file)
    makeCode_familyCode_keys = [x for x in makeCode_familyCode_keys]
    print(makeCode_familyCode_keys)

# lr = joblib.load('./model/lr/data_lr.model')
lr = joblib.load('./model/jupyter/data_lr.model')
# ss = joblib.load('./model/lr/data_ss.model')


def predict(register_time, city, mileage, make, family, gear0='自动', engine=2, business='商家', vehicle_type_code='PS',
            publish_date='2014-3', new_price=500000):
    '''
        档位类型        1-手动，2-自动
        发动机大小       2， 1.8， 2.4
        卖方类型        1-个人，2-商家
        车龄             37
        行驶公里数       250000
        平均每月行驶公里数  22500
        新车价格           349800
        车辆类型            3-suv 2-客车 1-皮卡
        车辆款式发布时间    30
        地区           北京
        排放标准        国五
        品牌和系列code alfagiulia
    '''
    mileage_int = int(mileage)
    publish_date_value = data_utils.distance_now_months_by_str(publish_date, patten='%Y-%m')
    emission_feature = data_utils.get_array_can_be_predict(emission_keys, '国五')
    make_code_feature = data_utils.get_array_can_be_predict(makeCode_familyCode_keys, make + family.upper())

    age = data_utils.distance_now_months_by_str(register_time, patten='%Y-%m')
    # 发布时间, 排放标准，品牌系列码 待查询
    province_feature = data_utils.get_array_can_be_predict(city_keys, city)
    data = [data_utils.gear_handle(gear0),
            float(engine),
            data_utils.business_handle(business),
            age, mileage_int, mileage_int / age,
            int(new_price),
            data_utils.vehicle_type_code_handle(vehicle_type_code),
            publish_date_value]
    data.extend(emission_feature)
    data.extend(province_feature)
    data.extend(make_code_feature)
    print(data)
    # print(len(data))
    data1 = [data]
    # data1 = ss.transform(data1)
    price = lr.predict(data1)
    print(price)
    return price[0]


if __name__ == '__main__':
    print(round(predict(register_time='2015-10', city='北京', mileage=30300, make='BMW', family='525LI'), 1))
