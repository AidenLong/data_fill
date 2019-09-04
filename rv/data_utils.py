# -*- coding utf-8 -*- #

import datetime
import pandas as pd


def distance_now_months_by_date(date1):
    '''
    距离当前时间差多少个月
    :param date1:    日期
    :return:        返回相差的距离月数
    '''
    now_date = datetime.datetime.now()
    num = (now_date.year - date1.year) * 12 + (now_date.month - date1.month)
    return num


def distance_now_months_by_str(str1, patten='%Y%m'):
    '''
    距离当前时间差多少个月
    :param str1:    日期
    :param patten:  日期格式
    :return:        返回相差的距离月数
    '''
    str2 = str(str1)
    # print(str1, str2)
    if len(str2) == 5 and str2.endswith('0'):
        str2 = str2[0:-1] + '1'
    now_date = datetime.datetime.now()
    date = datetime.datetime.strptime(str2, patten)
    num = (now_date.year - date.year) * 12 + (now_date.month - date.month)
    return num


def gear_handle(gear):
    if gear == '自动':
        return 2
    else:
        return 1


def business_handle(business):
    if business == '个人':
        return 1
    else:
        return 2


def emission_handle(emission):
    if emission and type(emission) != float:
        value = emission.strip()
        if ('三' in value or 'Ⅲ' in value or 'III' in value) and 'OBD' in value:
            return '国三+OBD'
        if '三' in value or 'Ⅲ' in value or 'III' in value:
            return '国三'
        if '二' in value or 'Ⅱ' in value or 'II' in value:
            return '国二'
        if '四' in value or 'IV' in value or 'Ⅳ' in value:
            return '国四'
        if '五' in value or 'Ⅴ' in value or 'V' in value:
            return '国五'
        if '一' in value or 'Ⅴ' in value or 'V' in value:
            return '国一'
    return '未知'


def province_value_handle(x):
    if pd.isnull(x):  # 判断是否为NaN值，== 和in 都无法判断
        return '全国'
    else:
        return str(x)


def vehicle_type_code_handle(x):
    if x == 'PS':
        return 2
    if x == 'PU':
        return 1
    if x == 'SV':
        return 3

def return_array_can_be_predict(data, target):
    data1 = [x for x in data]
    print(data1)
    print(len(data1))
    result = [0] * len(data1)
    index = data1.index(target)
    if index >= 0:
        result[index] = 1
        return result

if __name__ == '__main__':
    # print(distance_now_months(datetime.date(2018, 8, 4), "%Y-%m-%d"))
    print(emission_handle('国III'))
    print(emission_handle('国III+OBD'))
    print(emission_handle('国V'))
    print(emission_handle('国IV(国V)'))
    print(emission_handle('国IV'))
    print(distance_now_months_by_str('20180'))
