import requests
import time
sentence = "Dear, I love you forever!"
for char in sentence.split():
   allChar = []
   for y in range(12, -12, -1):
       lst = []
       lst_con = ''
       for x in range(-30, 30):
            formula = ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3
            if formula <= 0:
                lst_con += char[(x) % len(char)]
            else:
                lst_con += ' '
       lst.append(lst_con)
       allChar += lst
   print('\n'.join(allChar))
   time.sleep(1)

   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
   }
   try:
       resp = requests.get('http://httpbin.org/ip', headers=headers, timeout=3)
       ip = resp.json()['origin']
   except requests.exceptions.ConnectionError:
       print('请保证网络通畅，无网络！')
   except requests.exceptions.ReadTimeout:
       print('请保证网络通畅，程序即将退出！')
       time.sleep(5)
       os.system(exit())

   list = ['666,我太高兴了', '这虽然不是我想要的结果,但我尊重你的选择!', '我会加倍努力,让你接受我的!']
   print('亲爱的，我喜欢你很久了，你愿意接受我吗？(1:接受 2:不接受 3:暂时不考虑)')
   print('你有10秒考虑时间，请仔细考虑!')
   time.sleep(10)
   print('请遵从你的内心大胆输入,一次就好:')
   a = input()
   while (a != '1' and a != '2' and a != '3'):
       print('输入错误,请重新输入!:')
       print('1:接受，2:不接受 3:暂时不考虑')
       a = input()


def send(a):
   # 以qq邮箱为例
   smtpserver = 'smtp.qq.com'
   user = '发送方(你)的邮箱账号'
   password = '发送方（你）的邮箱的SMTP授权码'
   sender = '发送方（你）的邮箱账号'
   # receive为接收方，也可以写自己(不让对方知道)
   receive = '接收方（她）的邮箱账号'
   # subject为邮件主题
   subject = 'Dear'
   # 定义格式及输入内容
   msg = MIMEText('<html><h1>%sIP:%s</h1></html>' % (list[a - 1], ip), 'html', 'utf-8')
   msg['Subject'] = Header(subject, 'utf-8')
   # 执行发送操作
   smtp = smtplib.SMTP()
   smtp.connect(smtpserver)
   smtp.login(user, password)
   smtp.sendmail(sender, receive, msg.as_string())
   smtp.quit()


send(int(a))
    print('谢谢你的选择!')
    time.sleep(5)