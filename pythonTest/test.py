import requests
from lxml import etree


class QuanshuSpider(object):
    def __init__(self):
        self.session = requests.Session()
        self.index_url = 'http://www.quanshuwang.com/book/9/9055'  # 网址可更换为全书网里面的书目录页
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'
        }

    def get_index_page(self):
        index_page = self.session.get(self.index_url, headers=self.headers).content.decode('gbk')
        html = etree.HTML(index_page)
        self.title = html.xpath('//*[@id="chapter"]/div[3]/div[1]/strong/text()')[0]
        authors = html.xpath('//*[@id="chapter"]/div[3]/div[1]/span/text()')[0]
        self.author = authors[3:]
        print(self.title, self.author)
        chapter_urls = html.xpath('//*[@id="chapter"]/div[3]/div[3]/ul/div[2]/li/a/@href')
        return chapter_urls

    def parse_chapter_page(self):
        for chapter_url in self.get_index_page():
            try:
                chapter_page = self.session.get(chapter_url, ).content.decode('gbk')
                html = etree.HTML(chapter_page)
                chapter_content = html.xpath('//*[@id="content"]/text()')
                chapter_titles = html.xpath('//*[@id="directs"]/div[1]/h1/strong/text()')[0]
                chapter_title = chapter_titles[3:] + '\n\n'
                # print(chapter_content.strip())
                self.save_data(chapter_title)
                print('正在保存 ' + chapter_url)
                print(chapter_title)
                for content in chapter_content:
                    contents = '    ' + content.strip() + '\n'
                    self.save_data(contents)
            except Exception as e:
                print(e)
                continue

    def save_data(self, content):
        with open(self.title + ' ' + self.author + '.txt', 'a+', encoding='utf-8') as f:
            f.write(content)
            f.close()


if __name__ == '__main__':
    spider = QuanshuSpider()
    spider.parse_chapter_page()