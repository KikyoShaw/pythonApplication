import requests  # 导入requests库
import base64  # 导入base64库

# 借助https://console.faceplusplus.com.cn平台来实现换脸
API_Key = '7LUPX5XQcDUYIXTu-_YMAT-mvEgIRKVQ'  # 你自己申请的API Key
API_Secret = '9hDv4cbZhzclm91JOP8AEwc-tTI8pxLx'  ##你自己申请的API Secret


# 定义一个获取图片的人脸特征参数的函数
def find_face(imgpath):  # 查找人脸参数（图片位置）
    url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'  # 使用的人脸识别网站
    data = {'api_key': API_Key, 'api_secret': API_Secret, 'image_url': imgpath, 'return_landmark': 1}  # 相关个人账号参数等
    files = {'image_file': open(imgpath, 'rb')}  # 打开图片
    response = requests.post(url, data=data, files=files)  # 用requests.poet（）函数将个人账号参数和图片发送到网站
    res_json = response.json()  # 转换为json
    faces = res_json['faces'][0][
        'face_rectangle']  # 获取面部大小的四个值，分别为长宽高低{'width': 176, 'top': 128, 'left': 80, 'height': 176}
    return faces  # 返回图片的面部参数


# 定义一个换脸函数,函数中number表示两张脸的相似度为99%
def change_face(image_1, image_2, number=99):
    url = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"  # 使用的换脸网址
    find_p1 = find_face(image_1)  # 第1张图片的人脸参数
    find_p2 = find_face(image_2)  # 第2张图片的人脸参数
    rectangle1 = str(str(find_p1['top']) + ',' + str(find_p1['left']) + ',' + str(find_p1['width']) + ',' + str(
        find_p1['height']))  # 得到图片1坐标
    rectangle2 = str(str(find_p2['top']) + ',' + str(find_p2['left']) + ',' + str(find_p2['width']) + ',' + str(
        find_p2['height']))  # 得到图片2坐标

    page1 = open(image_1, 'rb')  # 以二进制打开图片1
    page1_64 = base64.b64encode(page1.read())  # 将字符串转成成base64编码
    page1.close()  # 关闭图片1

    page2 = open(image_2, 'rb')  # 二进制打开图片2
    page2_64 = base64.b64encode(page2.read())  # 将字符串转成成base64编码
    page2.close()  # 关闭图片2

    data = {'api_key': API_Key, 'api_secret': API_Secret, 'template_base64': page1_64,
            'template_rectangle': rectangle1, 'merge_base64': page2_64, 'merge_rectangele': rectangle2,
            'merge_rate': number}  # 参数信息
    response = requests.post(url, data=data).json()  # 发送参数到换脸网站
    results = response['result']  # 得到返回参数
    image = base64.b64decode(results)  # 转换信息
    with open('新图片.jpg', 'wb') as file:  # 将信息写入到图片
        file.write(image)
    print("转换完成了！")


if __name__ == '__main__':
    image1 = r"D:\res\1.jpg"
    image2 = r"D:\res\5.jpg"
    change_face(image1, image2)