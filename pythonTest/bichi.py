import requests,re,time
from  bs4 import  BeautifulSoup
'''
作者是帅气逼人的钢铁直男
爬取的是网址：www.win4000.com13
需要的库：BeautifulSoup time requests re
工具    ：visual studio code
'''
s=time.clock()
pp=1#图片数量
end=1
path='C:\\Users\\win10\\Desktop\\python\\爬取桌面壁纸图\\壁纸\\'#修改图片保存路径
def danz(id):#定义单页爬取函数
    page=1
    while True:#无限循环
        global pp#在函数内修改外部变量需要声明
        html = requests.get("http://www.win4000.com/wallpaper_detail_%s_%s.html"%(id,page))#获取单章网址内容
        if html.status_code==404:#如果是404证明爬取完了
            break#退出循环
        jpg = BeautifulSoup(html.text,'lxml')#解析
        jpg1=jpg.find('img',class_='pic-large')['src']#调用
        jpg = requests.get(jpg1).content#访问jpg链接，因为是二进制，所以需要.content
        with open("%s%s.jpg"%(path,pp),'wb') as f:#保存jpg
            f.write(jpg)
        print("第%s张图片下载完成"%pp)
        if int(pp)==end and all=='n':#爬取到指定页数并且不是爬取所有就结束脚本
            e=time.clock()#获取时间
            exit("完成耗时%s秒"%(e-s))
        page=page+1#自增
        pp=pp+1#自增
def m(url):
    html=requests.get(url)#获取网页内容
    if html.status_code==404:
        ukjias=1
    else:
        a=re.findall(r'http://www.win4000.com/wallpaper_detail_(.+?).html',html.text)#获取单章id
        for aa in a:#阅遍字典
            danz(aa)#使用单章jpg保存函数
def mian(lx):
    page=1#这个和函数是不一样的 函数内变量不影响外部变量除非global
    for i in range(5):#循环五次 因为他只有五页列表
        m("http://www.win4000.com/zt/%s_%s.html"%(lx,page))#使用函数
        page=page+1#自增
url='http://www.win4000.com/zt/index.html'#标签网页
html=requests.get(url)#获取网页内容
a=BeautifulSoup(html.text,'lxml')#解析
a1=a.find('div',class_="main")#获取div内标签
a2=a1.find_all('li')#获取所有li标签内容
pl=0#序列号
l=[True]*60#字典
print('#'*40+'爬取类型'+'#'*40)
for a3 in a2:#阅历标签内容
    url=re.search(r'(.*)/(.+?)\.',a3.find('a')['href'])[2].replace('_1','')#获取id
    title=re.sub('<(.+?)>','',str(a3.p))#标题
    l[pl]=url#把url写入字典以便调用
    print("序列号%s：%s"%(pl,title))
    pl=pl+1#自增序列号
print('#'*40+'爬取类型'+'#'*40)
xzlx=input('输入需要爬取类型的序列号：')#获取序列号
all=input('是否需要爬取全部图片(y/n)：') #如果需要全部爬取就y 需要爬取指定数量就n
if all=='n':#如果等于n就爬取指定数量
    end=int(input("输入需要爬取数量：")) #需要图片多少张
print('#'*40+'开始爬取'+'#'*40)
mian(l[int(xzlx)])#调用函数
#如果是全部图片保存就打印
e=time.clock()#计算时间
print("完成耗时%s秒"%(e-s))