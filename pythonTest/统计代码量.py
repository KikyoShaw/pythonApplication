# 导入库
import os
import time

# 指定读取的路径
base_dir = ''

# 文件列表
file_lists = []

# 指定想要统计的文件类型
file_type = ['py']


# 遍历文件, 递归遍历文件夹中的所有
# 定义一个 getDir_or_File 函数，看名字都应该知道是什么意思了吧
# base_dir 是我们定义的路径（路径为 ./）
def getDir_or_File(base_dir):
    # 将文件列表定义为全局的
    global file_lists

    # 遍历当前目录下所有的目录路径，目录名，文件名
    for parent, dirnames, filenames in os.walk(base_dir):
        # 遍历文件名
        for filename in filenames:
            # 获取后缀
            file = filename.split('.')[-1]
            # 如果获取的后缀是我们定义文件类型
            if file in file_type:
                # 将目录路径与文件名连接起来，如（'./code.py'）
                file_lists.append(os.path.join(parent, filename))


# 统计一个文件的行数
def countLines(file_name):
    # 定义一个变量 count，并赋值为 0
    count = 0
    # 这里我们使用 open 函数来读取文件内容，readlines() 的意思是按行读取
    for file_line in open(file_name, 'r', encoding='utf-8').readlines():
        # 过滤掉空行，空行总不是你写的代码吧对吧
        if file_line != '' and file_line != '\n':
            # 满足上面的条件的话就行数 + 1
            count += 1
    # 打印文件名和行数
    print(file_name + '----', count)
    # 返回 count，为什么要返回？因为这只是一个文件而已，既然要统计代码行数总不能只统计一个文件吧？
    return count


if __name__ == '__main__':
    # 用于基准测试的性能计数器。
    startTime = time.perf_counter()
    # 调用 getDir_or_File() 函数来遍历目录 and 文件
    getDir_or_File(base_dir)
    # 定义代码总行数的变量，并赋值为 0
    totallines = 0
    # 遍历所有文件
    for filelist in file_lists:
        # 计算总代码行数
        totallines = totallines + countLines(filelist)
    # 打印代码行数
    print('total lines:', totallines)
    # 打印程序执行时间
    print('Success! Cost Time: %0.2f seconds' % (time.perf_counter() - startTime))
