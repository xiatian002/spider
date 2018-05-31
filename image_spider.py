#!/usr/bin/python
#-*- coding:utf-8 -*-
import requests
import time
import csv
import random
import socket
import os
#import http.client
from bs4 import BeautifulSoup

#if len(sys.argv) !=4:
#    print('3 arguments were required but only find'+str(len(sys.argv)-1))
#    exit()
category='thread0806.php?fid=16&search=&page='
#try:
page_start=[1]
page_end=3
#except :
#    print("The second and thrid argument must be numbers! ")
#    exit()

def get_content(url,date=None):
    header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'__cfduid=d3ce75ac11355f82527c2ef982edde87e1524752837; UM_distinctid=1630259e876469-09ab95f6a9f1bc-4c322073-100200-1630259e878656; CNZZDATA950900=cnzz_eid%3D898198707-1524752468-%26ntime%3D1524752468',
        'DNT':'1',
        'Host':'cl.svtk.pw',
        'Referer':'http://cl.svtk.pw/index.php',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
    }
    timeout=random.choice(range(80,120))

    while True:
        try:
            rep=requests.get(url,headers=header,timeout=timeout)
            rep.encoding='gbk'
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

def get_title_urls(rep_text):#从帖子列表获取帖子链接和帖子名称
    final=[]
    bs=BeautifulSoup(rep_text,"html.parser")
    body=bs.body
    data=body.find("table",{"id":"ajaxtable"})
    tbody=data.find("tbody",{'style':'table-layout:fixed;'})
    tr=tbody.find_all("tr",{'class':'tr3 t_one tac'})
        
    links=[]
    names=[]
    for link in tr:
        tital_h3=link.find('h3')
        if tital_h3:
            tital_a=tital_h3.find('a')
            for href_a in tital_a:
                href_a=tital_a.get('href')
                if href_a=='notice.php?fid=-1#1':
                    break
                else:
                    href_name=tital_a.get_text()
                    links.append(href_a)
                    names.append(href_name)
    #                print(href_a)
    return links,names
    sleep(1)

def get_image_paper_link(html):#获取图片的链接
    url_links=[]
    url_name=[]
    body=BeautifulSoup(html,'html.parser').body
    bef_div=body.find('div',{'class':'tpc_content do_not_catch'})
    input_dom=bef_div.find_all('input')
#    lis=ul.find_all('li',{'class':'wall'})
    for inputs in input_dom:
        if inputs:
#            div=li.find('div',{'id':'hudtitle'})
            url_links.append(inputs.get('data-src'))
            url_name.append(str(random.choice(range(1,100)))+'.jpg')
    return url_links,url_name

def image_downs(url,name):
    web_host="http://cl.svtk.pw/"
    #os.mkdir('E:\\vscode\\spider\\images\\'+title_name)
    #os.chdir('E:\\vscode\\spider\\images\\'+title_name)
    for single_url in url:
        for single_name in name:
            result_image=requests.get(single_url,timeout=50)
            if result_image.status_code==200:
                open(single_name,'wb').write(result_image.content)
                #time.sleep(random.choice(range(2,5)))
                print("download %s is over"%single_name)
            name.pop(0)
            break
        time.sleep(random.choice(range(2,5)))

def start():
    page_domain='http://cl.svtk.pw/'
    page_url='http://cl.svtk.pw/'+category

    #if page_start[0]<=page_end:
    while page_start[0] <= page_end:#从起始页到尾页循环起来gogogogo~~~~
        title_pages_urls=[]
        title_page_name=[]
        send_wall_url=page_url+str(page_start[0])
        page_resource=get_content(send_wall_url)
        title_pages_urls,title_page_name=get_title_urls(page_resource)
        page_start[0]=page_start[0]+1
#        i=0
        for wallpage_url in title_pages_urls[9:-1]:
            #if dir_name in title_page_name:
            os.makedirs('images/0525/'+title_page_name[9])
            os.chdir('images/0525/'+title_page_name[9])
            html=get_content(page_domain+wallpage_url)
            image_url,image_name=get_image_paper_link(html)
            image_downs(image_url,image_name)
            title_page_name.pop(0)
            #break
            time.sleep(random.choice(range(2,5)))
	    os.chdir('/opt/py/spider/')

if __name__=='__main__':
#    url='http://cl.svtk.pw/thread0806.php?fid=16'
#    html=get_content(url)
#    result=get_data(html)
    start()
