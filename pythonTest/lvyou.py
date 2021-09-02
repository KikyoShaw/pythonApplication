#去哪儿景点信息抓取
 
# -*- coding: UTF-8 -*-
import requests
import re,time,os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
 
class Qner(object):
    def __init__(self):
        self.ua=UserAgent()
        self.headers={"User-Agent":self.ua.random}
        self.url='https://piao.qunar.com/ticket/list.htm?keyword='
        self.city=city
        self.pagemax=int()
        self.hrefs=[]
 
 
    def get_pagemax(self):
        url=f'{self.url}{city}'
        response=requests.get(url,headers=self.headers)
        if response.status_code==200:
            soup=BeautifulSoup(response.text,'lxml')
            a=soup.find('div',class_="pager").find_all('a')
            pagemax=a[-2].get_text()
            self.pagemax=int(pagemax)
 
 
    def get_urllist(self):
        for i in range(1,self.pagemax+1):
            url=f'{self.url}{city}&page={i}'
            print(url)
            response = requests.get(url, headers=self.headers)
            time.sleep(2)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                divs=soup.find_all('div',class_="sight_item_detail clrfix")
                for div in divs:
                    name=div.find('a',class_="name").get_text()
                    print(name)
                    address=div.find('p',class_="address color999").find('span').get_text()
                    print(address)
                    try:
                        price=div.find('span',class_="sight_item_price").find('em').get_text()
                        print(price)
                    except:
                        print("价格不详！")
                    href = div.find('h3',class_='sight_item_caption').find('a')['href']
                    href = f'https://piao.qunar.com{href}'
                    self.hrefs.append(href)
                print(self.hrefs)
                time.sleep(5)
 
if __name__ == '__main__':
    city="北京"
    spider=Qner()
    spider.get_pagemax()
    spider.get_urllist()