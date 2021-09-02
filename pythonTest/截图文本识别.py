import keyboard  # python用的是3.6版本，3.6版本以上可能会出问题（框架不支持）
from PIL import ImageGrab  # PIL较多用于2.7版本的Python中，到python3版本已经用Pillow代替PIL了(pip install pillow)
from aip import AipOcr  # 百度AI人工智能
import time
import sys


class TextRecognition():
    def __init__(self):
        APP_ID = '百度AI对应的appid值'
        API_KEY = '百度AI对应的appkey值'
        SECRET_KEY = '百度AI对应的secretkey值'

    self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def toScreenhot(self):  # 截图函数
    keyboard.wait(hotkey='ctrl+alt+a')
    keyboard.wait(hotkey='enter')
    time.sleep(0.1)  # 睡眠0.1秒，加载缓存，否则有延迟只能加载上一张图片
    image = ImageGrab.grabclipboard()  # 能够从剪切板当中获取图片，并且生成出来
    image.save('screenhot.jpg')


def getImage(self):  # 二进制文件读取函数
    with open('screenhot.jpg', 'rb') as fp:
        return fp.read()


def textRecognition(self, writetype):  # 文本识别函数
    img = self.getImage()
    text = self.client.basicGeneral(img)  # 返回文字内容
    result = text['words_result']
    with open('content.txt', writetype + '+', encoding='utf8') as fp:
        for i in result:
            fp.write(i['words'] + '\n')
            print(i['words'])


if __name__ == '__main__':
    writetype = input("欢迎来到文本识别系统！请先选择识别文本写入方式：（覆盖内容写入输入w/追加内容写入输入a）\n")
    if writetype == 'w' or writetype == 'a':
        print("温馨提示：请登录QQ/Tim，同时按下CTRL+ALT+A对指定识别内容进行截图，然后按下回车键完成截图。")
        while 1:
            print("提示：请用户开始截图！")
            TextRecognition().toScreenhot()
            print("==============================================================")
            TextRecognition().textRecognition(writetype)
            print("==============================================================")
            print("提示：文字识别已完成，上述内容即为content.txt文本所写入的内容。\n是否继续？（y/n）")
            judge = input("我选择：")
            if judge == 'y':
                continue
            elif judge == 'n':
                break
            else:
                while 1:
                    print("警告：请输入正确的选项（y/n）！")
                    judge1 = input("我选择：")
                    if judge1 == 'y':
                        break
                    elif judge1 == 'n':
                        sys.exit(0)
                    else:
                        continue
    else:
        print("警告：请输入正确的识别文本写入方式：（覆盖内容写入输入w/追加内容写入输入a）！")
        sys.exit(0)