import requests
import json
import pandas as pd
import numpy
import os

def get_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=jQuery341001657575837432268_1581070969707&_=1581070969708'
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'}
    res = requests.get(url, headers=headers).text
    a = res.split('jQuery341001657575837432268_1581070969707(')[1].split(')')[0]
    c = json.loads(a)
    data = json.loads(c['data'])
    return data

def print_data_china():
    data = get_data()
    print('统计截至时间：'+str(data['lastUpdateTime'])[:10])
    print('全国确诊人数：'+str(data['chinaTotal']['confirm']))
    print('相较于昨天确诊人数：'+str(data['chinaAdd']['confirm']))
    print('全国疑似病例：'+str(data['chinaTotal']['suspect']))
    print('相较于昨天疑似人数：'+str(data['chinaAdd']['suspect']))
    print('全国治愈人数：'+str(data['chinaTotal']['heal']))
    print('相较于昨天治愈人数：'+str(data['chinaAdd']['heal']))
    print('全国死亡人数：'+str(data['chinaTotal']['dead']))
    print('相较于昨天死亡人数：'+str(data['chinaAdd']['dead']))


# def print_data_path_china():
#     data = get_data()['areaTree'][0]['children']
#     path_data = []
#     path_china = []
#     path = str(input('请输入你要查询的省份：'))
#     for i in data:
#         path_china.append(i['name'])
#         path_data.append(i['children'])
#     if path in path_china:
#         num = path_china.index(path)
#         data_path = path_data[num]
#         print('{:^10}{:^10}{:^10}{:^10}{:^10}{:^10}{:^10}{:^10}{:^10}'.format('地区','累计确诊人数','相较于昨日确诊人数','累计疑似病例','相较于昨日疑似病例','累计治愈人数','相较于昨日治愈人数','累计死亡人数','相较于昨日死亡人数'))
#         for i in data_path:
#             name = i['name']
#             today = i['today']
#             total = i['total']
#             a = '{:^10}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}'
#             print(a.format(name, str(total['confirm']), str(today['confirm']), str(total['confirm']), str(today['suspect']), str(total['heal']), str(today['heal']), str(total['dead']), str(today['dead'])))

data = get_data()

# 数据明细，数据结构比较复杂，一步一步打印出来看，先明白数据结构
areaTree = data['areaTree']
# 国内数据
china_data = areaTree[0]['children']
china_list = []
for a in range(len(china_data)):
    province = china_data[a]['name']
    province_list = china_data[a]['children']
    for b in range(len(province_list)):
        city = province_list[b]['name']
        total = province_list[b]['total']
        today = province_list[b]['today']
        china_dict = {}
        china_dict['province'] = province
        china_dict['city'] = city
        china_dict['total'] = total
        china_dict['today'] = today
        china_list.append(china_dict)
        
china_data = pd.DataFrame(china_list)


# 定义数据处理函数
def confirm(x):
    confirm = eval(str(x))['confirm']
    return confirm
def suspect(x):
    suspect = eval(str(x))['suspect']
    return suspect
def dead(x):
    dead = eval(str(x))['dead']
    return dead
def heal(x):
    heal =  eval(str(x))['heal']
    return heal
# 函数映射
china_data['confirm'] = china_data['total'].map(confirm)
china_data['suspect'] = china_data['total'].map(suspect)
china_data['dead'] = china_data['total'].map(dead)
china_data['heal'] = china_data['total'].map(heal)
china_data['addconfirm'] = china_data['today'].map(confirm)
china_data['addsuspect'] = china_data['today'].map(suspect)
china_data['adddead'] = china_data['today'].map(dead)
china_data['addheal'] = china_data['today'].map(heal)
china_data = china_data[["province","city","confirm","suspect","dead","heal","addconfirm","addsuspect","adddead","addheal"]]



# date =str(data['lastUpdateTime'])[:10]
# china_data['date']= date

# global_data = pd.DataFrame(data['areaTree'])
# global_data['confirm'] = global_data['total'].map(confirm)
# global_data['suspect'] = global_data['total'].map(suspect)
# global_data['dead'] = global_data['total'].map(dead)
# global_data['heal'] = global_data['total'].map(heal)
# global_data['addconfirm'] = global_data['today'].map(confirm)
# global_data['addsuspect'] = global_data['today'].map(suspect)
# global_data['adddead'] = global_data['today'].map(dead)
# global_data['addheal'] = global_data['today'].map(heal)
# global_data = global_data[["name","confirm","suspect","dead","heal","addconfirm","addsuspect","adddead","addheal"]]
# global_data['date']= date

# china_data = china_data.append(global_data, ignore_index=True)


print(china_data)

fileop= open('haha,txt','a+')
fileop.write(str(china_data))
fileop.close



