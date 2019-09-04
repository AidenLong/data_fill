# -*- coding utf-8 -*- #

from sklearn.externals import joblib
import pickle
from rv import data_utils

with open('./data/keys/province_city_keys.pkl', 'rb') as file:
    province_city_keys = pickle.load(file)

with open('./data/keys/emission_keys.pkl', 'rb') as file:
    emission_keys = pickle.load(file)

with open('./data/keys/makeCode_familyCode_keys.pkl', 'rb') as file:
    makeCode_familyCode_keys = pickle.load(file)

# ss = joblib.load('data_ss.model')
lr = joblib.load('./model/data_lr.model')

province_feature = data_utils.return_array_can_be_predict(province_city_keys, '北京-北京')
emission_feature = data_utils.return_array_can_be_predict(emission_keys, '国五')
make_code_feature = data_utils.return_array_can_be_predict(makeCode_familyCode_keys, 'ALFAGIULIA')
data = [data_utils.distance_now_months_by_str('2018-12', patten='%Y-%m'), 278000, 2, 2, 2, 7, 10000, 1428.571429, 2, 30]
data.extend(emission_feature)
data.extend(province_feature)
data.extend(make_code_feature)
print(data)
data1 = [data]
print(lr.predict(data1))
