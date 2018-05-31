#-*- coding:utf-8 -*-
import time
import os
import http.client
import requests
import csv
import socket
from bs4 import BeautifulSoup
import random
import sys

#if len(sys.argv) !=4:
#    print('3 arguments were required but only find'+str(len(sys.argv)-1))
#    exit()
category='girls'
#try:
page_start=[1]
page_end=3
#except :
#    print("The second and thrid argument must be numbers! ")
#    exit()

def get_content(url,data=None):
    header={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'ae74935a9f5bd890e996f9ae0c7fe805=q5vS1ldKBFw%3DoYi%2BY%2FgxHgk%3D9SHVZegsDfo%3DigWzepDZpBk%3Daa0wj%2BrGoS4%3DlopdREWA8%2B4%3D2jeJiQbDVoE%3D5OOqG0vlOE0%3D; __utma=30129849.1826657722.1524832176.1524832176.1524832176.1; __utmb=30129849.12.10.1524832177; __utmc=30129849; __utmz=30129849.1524832177.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __qca=P0-770944660-1524832177264; __utmt=1',
        'Host':'wallpaperswide.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
    }
    timeout=random.choice(range(80,100))

    while True:
        try:
            rep=requests.get(url,headers=header,timeout=timeout)
            rep.encoding='utf-8'
            break

        except socket.timeout as e:
            print("3:",e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print("4:",e)
            time.sleep(random.choice(range(20,40)))    

        except http.client.BadStatusLine as e:
            print("5:",e)
            time.sleep(random.choice(range(30,80)))

        except http.client.IncompleteRead as e:
            print("6:",e)

    return  rep.text

def get_paper_link(html):#获取壁纸下载连接，我电脑是16:9的屏幕
    bs=BeautifulSoup(html,'html.parser')
    body=bs.body
    div=body.find('div',{'id':'wallpaper-resolutions'})
    h3=div.find_all('h3')
    for h in h3:
        if h.string == 'HD 16:9':
            links=div.find('a',title='HD 16:9 1600 x 900 wallpaper')
            if links:
                link_url=links.get("href")
                link_name=links.get("href").replace('/download/','')
#                print(link_url)

    time.sleep(random.choice(range(5,10)))
    return link_url,link_name

def get_wall_paper_link(html):#获取从缩略图到下载界面的链接
    url_links=[]
    body=BeautifulSoup(html,'html.parser').body
    bef_div=body.find('div',{'id':'content'})
    ul=bef_div.find('ul')
    lis=ul.find_all('li',{'class':'wall'})
    for li in lis:
        if li:
            div=li.find('div',{'id':'hudtitle'})
            url_links.append(div.find('a').get('href'))
    return url_links

def start():
    page_domain='http://wallpaperswide.com'
    page_url='http://wallpaperswide.com/'+category+'-desktop-wallpapers/page/'

    #if page_start[0]<=page_end:
    while page_start[0] <= page_end:#从起始页到尾页循环起来gogogogo~~~~
        send_wall_url=page_url+str(page_start[0])
        page_resource=get_content(send_wall_url)
        wallpages_urls=get_wall_paper_link(page_resource)
        page_start[0]=page_start[0]+1

        for wallpage_url in wallpages_urls:
            html=get_content(page_domain+wallpage_url)
            image_url,image_name=get_paper_link(html)
            down_image(image_url,image_name)

def down_image(url,name):
    web_host="http://wallpaperswide.com"
    result_image=requests.get(web_host+url)
    if result_image.status_code==200:
        open('E:\\vscode\\spider\\images\\'+name,'wb').write(result_image.content)
        time.sleep(random.choice(range(5,10)))
        print("download %s is over"%name)

if __name__=='__main__':
    
#    url="http://wallpaperswide.com/lonely_woman-wallpapers.html"
#    html=get_content(url)
#    image_url,image_name=get_paper_link(html)
#    down_image(image_url,image_name)
    start()

