#-*- coding:utf-8 -*-
import requests
import csv
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup

def get_content(url,data=None):
    header={#header作为头信息可以直接从浏览器中复制出来
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'vjuids=-1b5a26784.162f7b5b81c.0.ca7e2517b102d8; vjlast=1524574304.1524574304.30; Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1524574304; Hm_lpvt_080dabacb001ad3dc8b9b9049b36d43b=1524574304; userNewsPort0=1; f_city=%E5%8C%97%E4%BA%AC%7C101010100%7C; Wa_lvt_1=1524574305; Wa_lpvt_1=1524574305',
        'Host':'www.weather.com.cn',
        'Referer':'https://www.baidu.com/link?url=BazjPlq8cvSUN9OFI4fWxRcRBBXvFxOfBsq8ao43JTxju09wkbL-f9_NesufLU7HhdQvJd5VyqII3cpjLe_hhK&wd=&eqid=b7e7d4ec0002d21b000000025adf285c',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
    }
    timeout=random.choice(range(80,120))#设置随即的timeout时间
    
    while True:
        try:
            rep=requests.get(url,headers=header,timeout=timeout)
            rep.encoding='utf-8'
            break

        except socket.timeout as e:
            print('3:',e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print('4:',e)
            time.sleep(random.choice(range(20,60)))

        except http.client.BadStatusLine as e:
            print('5:',e)
            time.sleep(random.choice(range(30,80)))

        except http.client.IncompleteRead as e:
            print('6:',e)
            time.sleep(random.choice(range(5,15)))

    return rep.text

def get_data(rep_text):

    final=[]
    bs=BeautifulSoup(rep_text,"html.parser")#创建BeautifulSoup对象
    body=bs.body
    data=body.find('div',{'id':'7d'}) 
    ul=data.find('ul')
    li=ul.find_all('li')

    for day in li:#获取li中的全部内容
        temp=[]
        date=day.find('h1').string#获取天气的时间，查找h1标签
        temp.append(date)
        inf=day.find_all('p')#查找所有p标签
        temp.append(inf[0].string)
        if inf[1].find('span') is None:
            temperature_highest=None
        else:
            temperature_highest=inf[1].find('span').string
            temperature_highest=temperature_highest.replace('℃','')
        temperature_lowest=inf[1].find('i').string
        temperature_lowest=temperature_lowest.replace('℃','')#去掉℃符号
        temp.append(temperature_highest)
        temp.append(temperature_lowest)
        final.append(temp)

    return final

def write_data(data,name):
    file_name=name
    with open(file_name,"a",newline='') as f:
        f_csv=csv.writer(f)
        f_csv.writerows(data)

if __name__ == '__main__':
    url='http://www.weather.com.cn/weather/101010100.shtml'
    html=get_content(url)
    result=get_data(html)
    write_data(result,'weather.csv')