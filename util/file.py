# coding=utf-8
import codecs
import os
import shutil


# 创建文件或文件夹
def create(path):
    path = path.strip().rstrip("\\")  # 去除首位空格、去除尾部 \ 符号
    if os.path.exists(path):
        print('文件或文件夹已存在--' + path)
        return
    try:
        os.makedirs(path[0:path.rfind("\\")])  # 创建上一级文件夹
    except:
        print()
    filename = path[path.rfind("\\") + 1:len(path)]  # 获取文件名
    if filename.__contains__('.'):  # 创建文件
        fo = open(path, 'w+')
        fo.close()
    else:  # 创建文件夹
        os.makedirs(path)
        print(path + ' 创建成功')


# 删除文件夹
def rmtree(path):
    try:
        os.remove(path)
    except:
        print('路径不存在')
    try:
        project_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件路径的上一级目录
        os.remove(project_path + r'\\' + path)
    except:
        print('不能直接删除含有文件的文件夹')
    try:
        shutil.rmtree(project_path + r'\\' + path)
        print('删除成功')
    except:
        print('删除失败')


# 遍历文件夹
def merge(file):
    for root, dirs, files in os.walk(file):
        print
    for f in files:
        print(os.path.join(root, f))
        # read_Writeline(os.path.join(root, f), file + ".txt")
    for d in dirs:
        print(os.path.join(root, d))


# 文件写入
def read_Writeline(old_file, new_file):
    new = codecs.open(new_file, 'a+', 'utf-8');
    old = codecs.open(old_file, 'r', 'utf-8')  # 需要两个\\,或者用原始字符串，在引号前面加r
    try:
        new.write(old.read())
        new.flush()
    finally:
        new.close()
        old.close()


if '__main__' == __name__:
    merge('超神机械师')
