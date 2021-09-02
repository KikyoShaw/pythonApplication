import requests, re, os
from bs4 import BeautifulSoup
from time import sleep
from random import uniform


# 网址解析
def url_open(url):
    headers = {}
    headers[
        "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    headers["Referer"] = "https://www.ivsky.com/bizhi/"
    html = requests.get(url, headers=headers).text

    return html


# 获取全部主题图片链接
def get_url_all():
    print("正在收集整理壁纸主题网址，请稍候.....")
    print()
    theme_url_list = []
    theme_title_list = []
    data = []
    page_totle = 100  # 壁纸主题共有100页
    # 逐页收集主题URL
    for page in range(1, page_totle + 1):
        url = "https://www.ivsky.com/bizhi/index_{}.html".format(page)
        html = url_open(url)
        soup = BeautifulSoup(html, "html.parser")
        url_all = soup.find_all("div", class_="il_img")
        for each in url_all:
            theme_title = each.a["title"]
            theme_title_list.append(theme_title)
            theme_url = "https://www.ivsky.com" + each.a["href"]
            theme_url_list.append(theme_url)
        # 将数据打包以便能够将两个数据一起返回
        data.append(theme_url_list)
        data.append(theme_title_list)
        break  # 减少调试运行时间使用 若要获取全部主题链接则删除此处即可

    theme_totle = len(data[0])  # 计算主题数目
    print("壁纸网址收集结束，共收集%d个主题，准备进行图片下载....." % theme_totle)
    sleep(1)  # 走个形式而已

    return data


def save_img(img_url_list, theme_name, work_path):
    # 更改图片保存路径（分主题保存）
    save_path = work_path + r"\%s" % theme_name
    if os.path.exists(save_path) == True:
        os.chdir(save_path)
    else:
        os.mkdir(save_path)
        os.chdir(save_path)

    num = 0  # 当前任务图片下载计数
    for img_url in img_url_list:
        num += 1
        print("正在下载主题“%s”第%d张图片" % (theme_name, num))
        headers = {}
        headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        content = requests.get(img_url, headers=headers).content
        with open("%d.jpg" % num, "wb") as f:
            f.write(content)

        sleep_time = uniform(0.18, 0.37)  # 随机休眠 减少服务器压力 (真有诚意调大点即可)
        sleep(sleep_time)


def get_img(data):
    img_root_url = "https://img.ivsky.com/img/bizhi/pre/"
    num_1 = -1  # 标题索引 用于后面索引标题
    work_path = os.getcwd()
    num_2 = 0  # 统计图片总张数
    for theme_url in data[0]:
        # print(theme_url)
        num_1 += 1
        theme_name_temp_1 = data[1][num_1]  # 获取对应的主题名称
        img_url_list = []  # 用于存储单个主题的图片下载链接

        # 文件名称检查，删除非法字符。
        theme_name_temp2 = []
        symbol_check = ['\\', '/', ':', '*', '?', '<', '.', '|', ',', '.', ';', '[', ']', "《", "》"]  # 名称符号检查
        p_theme_name = r'[\u4e00-\u9fa5]'
        theme_name_temp3 = re.findall(p_theme_name, theme_name_temp_1)
        for each in theme_name_temp3:
            if each in symbol_check:
                pass
            else:
                theme_name_temp2.append(each)
        theme_name = "".join(theme_name_temp2)

        print()
        print("正在下载主题：%s" % theme_name)
        print()

        # 每个页面16张图片 若主题图片数目大于16张图片存在多个页面.....
        p_img_num = r'.+[(](\d+?)张[)]'
        img_num = int(re.findall(p_img_num, theme_name_temp_1)[0])
        if img_num / 16 > img_num // 16:
            page_totle = img_num // 16 + 1
        else:
            page_totle = img_num / 16

        # 获取全部图片链接
        if page_totle == 1:
            html = url_open(theme_url)
            soup = BeautifulSoup(html, "html.parser")
            soup_img_url = soup.find_all("div", class_="il_img")
            for each in soup_img_url:
                temp = each.img["src"].split("/t/")[1]
                img_url = img_root_url + temp
                img_url_list.append(img_url)
                num_2 += 1
        else:
            for page in range(1, page_totle + 1):
                url = theme_url + "index_{}.html".format(page)
                html = url_open(url)
                soup = BeautifulSoup(html, "html.parser")
                soup_img_url = soup.find_all("div", class_="il_img")
                for each in soup_img_url:
                    temp = each.img["src"].split("/t/")[1]
                    img_url = img_root_url + temp
                    img_url_list.append(img_url)
                    num_2 += 1

        save_img(img_url_list, theme_name, work_path)  # 图片下载保存
    print()
    print("任务结束，共计下载图片%d张" % num_2)


def main():
    # 修改工作路径
    path = r'D:\res'
    if os.getcwd() != path:
        if os.path.exists(path) == False:
            os.mkdir(path)
            os.chdir(path)
        else:
            os.chdir(path)

    data = get_url_all()
    get_img(data)


if __name__ == "__main__":
    main()