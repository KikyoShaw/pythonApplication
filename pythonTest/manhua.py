import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re
from tqdm import tqdm

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
}


def get_index(index_url):
    chapterslist = {}
    response = requests.get(index_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    chapterList = soup.select('#chapterList')[0]
    chapters = chapterList.select('a')
    for chapter in chapters:
        chapterslist[chapter['title']] = chapter['href']
    return chapterslist


def quote_keys_for_json(json_str):
    """给键值不带双引号的json字符串的所有键值加上双引号。
    注：解析一般的不严格的json串，可以check out https://github.com/dmeranda/demjson, 速度比标准库要慢。"""
    quote_pat = re.compile(r'".*?"')
    a = quote_pat.findall(json_str)
    json_str = quote_pat.sub('@', json_str)
    key_pat = re.compile(r'(\w+):')
    json_str = key_pat.sub(r'"\1":', json_str)
    assert json_str.count('@') == len(a)
    count = -1

    def put_back_values(match):
        nonlocal count
        count += 1
        return a[count]

    json_str = re.sub('@', put_back_values, json_str)
    return json_str


def decode(raw, chapter_id):
    # 移动unicode对应数字位数为chapter_id最后值
    # 解密减 加密加
    # !__cr.imgpath=__cr.imgpath.replace(/./g,function(a){return String.fromCharCode(a.charCodeAt(0)-__cr.chapter_id%10)})!
    result = ''
    for i in raw:
        result += chr(ord(i) - int(chapter_id) % 10)
    return result


def get_info(index_url, num, index_dict):
    base = index_url
    tail = index_dict[f'{str(num)}话']
    detial_url = base + tail
    response = requests.get(detial_url, headers=headers)
    raw_address = BeautifulSoup(response.text, 'lxml').select('#content > div.comiclist > script')[0].string
    address = re.search('__cr.init\(({.*?})\)', raw_address, re.S)
    if address:
        # 类似python的字典形式 但引用没有引号用quote_keys_for_json()转一下
        # quote_keys_for_json()出处，https://segmentfault.com/q/1010000006090535?_ea=1009953
        info = json.loads(quote_keys_for_json(address.group(1)))
    return info


def get_certain_chapter_links(index_url, chapter, index_dict):
    certain_chapter_links = []
    info = get_info(index_url, chapter, index_dict)
    image_path = decode(info['chapter_addr'], info['chapter_id'])
    certain_chapter_total = int(info['end_var'])
    for num in range(1, certain_chapter_total + 1):
        # 核心拼接"//" + i + "/comic/" + this.imgpath + a
        image_address = 'http://mhpic.' + info['domain'] + '/comic/' + image_path + str(num) + '.jpg' + \
                        info['comic_definition']['middle']
        # image_address = 'http://mhpic.' + info['domain'] + '/comic/' + image_path + str(num) + '.jpg' +info['comic_definition']['high']
        certain_chapter_links.append(image_address)
    return certain_chapter_total, certain_chapter_links


def downloadFILE(url, name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    resp = requests.get(url=url, stream=True, headers=headers)
    content_size = int(int(resp.headers['Content-Length']) / 1024)
    with open(name, "wb") as f:
        print("Pkg total size is:", content_size, 'k,start...')
        for data in tqdm(iterable=resp.iter_content(1024), total=content_size, unit='k', desc=name):
            f.write(data)
        print(name, "download finished!")


if __name__ == "__main__":
    # 动漫主页https://www.zymk.cn/1/
    index_url = 'https://www.zymk.cn/1/'
    index_dict = get_index(index_url)
    # 下载目录doupo
    if not os.path.exists('zyresult'):
        os.mkdir('zyresult')
    # 爬取的章节1到802
    for chapter in range(1, 803):
        try:
            total, certain_chapter_links = get_certain_chapter_links(index_url, chapter, index_dict)
            for i in range(0, total):
                temp = f'{str(chapter).zfill(3)}话{str(int(i) + 1).zfill(2)}.jpg'
                name = os.path.join('zyresult', temp)
                url = certain_chapter_links[i]
                downloadFILE(url, name)
        except Exception as e:
            error = f'error at {chapter} ep'
            detail = str(e)
            print(error + '\n' + detail + '\n')
            with open('log.txt', 'a', encoding='utf-8') as f:
                f.write(error + '\n' + detail + '\n')
                f.close()
            continue