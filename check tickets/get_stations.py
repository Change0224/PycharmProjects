import requests
import re
import os


def getStation():
    #发送请求获取所有车站名称，通过输入的站名转换为查询地址的参数
    url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9141'
    #发送查询请求
    response = requests.get(url,verify=True) #请求并进行验证
    #print(response.text)
    #获取需要的车站名称
    # stations = re.findall('[\u4e00-\u9fa5]+\|[A-Z]+',response.text)
    # print(stations)
    stations = re.findall('([\u4e00-\u9fa5]+)\|([A-Z]+)',response.text)
    #print(stations)
    stations = dict(stations)  #转换为字典类型
    stations = str(stations)     #转换成字符串类型，否则无法写入文件
    write(stations)

def write(stations):
    #以写模式打开文件
    file = open('stations.text','w',encoding='utf_8_sig')
    file.write(stations)
    file.close()

def read():
    #以读模式打开文件
    file = open('stations.text','r',encoding='utf_8_sig')
    data = file.readline()
    file.close()
    return data

def isStations():
    #判断车站文件是否存在
    isStations = os.path.exists('stations.text')
    return isStations




