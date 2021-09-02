import requests
from lxml import etree


# 编写了一个常用的方法，输入url即可返回text的文本；
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    else:
        print("请求状态码 != 200,url错误.")
        return None


for number in range(0, 101):  # 利用range函数循环0-100，抓去第1页到100页。
    initialize_url = "https://bj.lianjia.com/zufang/pg" + str(number) + "/#contentList"  # 字符串拼接出第1页到100页的url；

    html_result = get_one_page(initialize_url)  # 获取URL的text文本
    html_xpath = etree.HTML(html_result)  # 转换成xpath格式
    # 抓去首页中的url（每页有30条房源信息）
    page_url = html_xpath.xpath(
        "//div[@class='content w1150']/div[@class='content__article']//div[@class='content__list']/div/a[@class='content__list--item--aside']/@href")

    for i in page_url:  # 循环每一条房源url
        true_url = "https://bj.lianjia.com" + i  # 获取房源的详情页面url
        true_html = get_one_page(true_url)  # 获取text文本
        true_xpath = etree.HTML(true_html)  # 转换成xpath格式

        # 抓取页面题目，即：房源详情页的标题
        title = true_xpath.xpath("//div[@class='content clear w1150']/p[@class='content__title']//text()")
        # 抓取发布时间并对字符串进行分割处理
        release_date = true_xpath.xpath("//div[@class='content clear w1150']//div[@class='content__subtitle']//text()")
        release_date_result = str(release_date[2]).strip().split("：")[1]
        # 抓取价格
        price = true_xpath.xpath("//div[@class='content clear w1150']//p[@class='content__aside--title']/span//text()")
        # 抓取房间样式
        house_type = true_xpath.xpath(
            "//div[@class='content clear w1150']//ul[@class='content__aside__list']//span[2]//text()")
        # 抓取房间面积
        acreage = true_xpath.xpath(
            "//div[@class='content clear w1150']//ul[@class='content__aside__list']//span[3]//text()")

        print(str(title) + " --- " + str(release_date_result) + " --- " + str(price) + " --- " + str(
            house_type) + " --- " + str(acreage))

        # 写入操作，将信息写入一个text文本中
        with open(r"E:\admin.txt", 'a') as f:
            f.write(str(title) + " --- " + str(release_date_result) + " --- " + str(price) + " --- " + str(
                house_type) + " --- " + str(acreage) + "\n")
