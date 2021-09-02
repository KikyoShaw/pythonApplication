import pdfkit
import requests
import parsel
url = 'https://blog.csdn.net/qq_41562665/article/details/90546750'
headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}
response = requests.get(url=url, headers=headers)
html = response.text
selector = parsel.Selector(html)
title = selector.css('.title-article::text').get()
article = selector.css('article').get()  # 提取标签为article 的内容

src_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Document</title>

</head>
<body>
    {content}
</body>
</html>
'''
with open(title+'.html', mode='w+', encoding='utf-8') as f:
    f.write(src_html.format(content=article))
    print(title+'================保存成功')

config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
pdfkit.from_file(title+'.html', title+'.pdf', configuration=config)

print(title+'.pdf','已保存成功')