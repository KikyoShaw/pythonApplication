import requests, base64


# 百度AI开放平台鉴权函数
def get_access_token():
    url = 'https://aip.baidubce.com/oauth/2.0/token'
    data = {
        'grant_type': 'client_credentials',  # 固定值
        'client_id': '7LUPX5XQcDUYIXTu-_YMAT-mvEgIRKVQ',  # 在开放平台注册后所建应用的API Key
        'client_secret': '9hDv4cbZhzclm91JOP8AEwc-tTI8pxLx'  # 所建应用的Secret Key
    }
    res = requests.post(url, data=data)
    res = res.json()
    access_token = res['access_token']
    return access_token


def image_process(img_before, img_after, how_to_deal):
    # 函数的三个参数，一个是转化前的文件名，一个是转化后的文件名，均在同一目录下，第三个是图像处理能力选择
    request_url = 'https://aip.baidubce.com/rest/2.0/image-process/v1/' + how_to_deal
    if how_to_deal == 'style_trans':  # 判断如果是 图像风格化，需要额外添加一个风格配置
        others = 'pencil'  # 风格化参数，具体可设置范围参见下面注释
        '''
        cartoon：卡通画风格
        pencil：铅笔风格
        color_pencil：彩色铅笔画风格
        warm：彩色糖块油画风格
        wave：神奈川冲浪里油画风格
        lavender：薰衣草油画风格
        mononoke：奇异油画风格
        scream：呐喊油画风格
        gothic：哥特油画风格
        '''
    else:
        others = ''

    file = open(img_before, 'rb')  # 二进制读取图片
    origin_img = base64.b64encode(file.read())  # 将图片进行base64编码
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'access_token': get_access_token(),
        'image': origin_img,
        'option': others
    }

    res = requests.post(request_url, data=data, headers=headers)
    res = res.json()

    if res:
        f = open(img_after, 'wb')
        after_img = res['image']
        after_img = base64.b64decode(after_img)
        f.write(after_img)
        f.close()


if __name__ == '__main__':
    img_before = 'black.jpg'  # 当前目录下的图片
    img_after = img_before.split('.')  # 将原文件名分成列表
    img_after = img_after[0] + '_1.' + img_after[1]  # 新生成的文件名为原文件名上加 _1

    image_process(img_before, img_after, 'colourize')
    # 第三个参数： selfie_anime 为人像动漫化，colourize 图像上色，style_trans 为图像风格化
    print('done!')
