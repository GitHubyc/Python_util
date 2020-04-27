import re
import shutil
import os
import win32com.client

# 在一个文件夹中，遍历文件信息抽取到相同文件夹。修改名称后进行移动
dir_url="C:\\Users\\Administrator\\Desktop\\music"
def getInfo(base_file):
    _shell = win32com.client.DispatchEx("shell.Application")
    _dir = _shell.NameSpace(dir_url)
    item = _dir.ParseName(os.path.split(base_file)[1])
    title = _dir.GetDetailsOf(item, 21) # 标题
    artists = _dir.GetDetailsOf(item, 13) # 歌手
    album = _dir.GetDetailsOf(item, 14) # 专辑

    return title, artists, album

def rename(file_path, title):
    '''重命名'''
    new_filel_name = title + '.mp3'
    new_file_path = os.path.join(os.path.dirname(file_path), new_filel_name)
    if file_path != new_file_path:
        os.rename(file_path, new_file_path)
        print(file_path, '已更名为：', new_file_path)
    else:
        new_file_path = file_path

    return new_file_path

def moveByArtist(file_path, artists, album):
    NEW_BASE_DIR = dir_url
    file_name = os.path.split(file_path)[1]

    '''根据歌手、专辑分组'''
    # artist_list = []
    # if artists in artist_list:
    #     # 存在歌手数据
    #     if not re.search(r'^？+$', album.strip()):
    #         # 移到专辑下
    #         new_path = os.path.join(NEW_BASE_DIR, artists.strip(), album.strip(), file_name)
    #     else:
    #         # 移到歌手下
    #         new_path = os.path.join(NEW_BASE_DIR, artists.strip(), file_name)
    # else:
    #     # 移到其他
    #     new_path = os.path.join(NEW_BASE_DIR, '其他', file_name)
    '''根据歌手分组'''
    print(artists.strip())
    if artists.strip() == '':
        new_path = os.path.join(NEW_BASE_DIR, '其他', file_name)
    else:
       new_path = os.path.join(NEW_BASE_DIR, artists.strip(), file_name)


    if not os.path.exists(os.path.dirname(new_path)):
        os.makedirs(os.path.dirname(new_path))
    if file_path != new_path:
        shutil.move(file_path, new_path)
        print(file_path, '已经移动到:', new_path)
    return new_path
if __name__ == "__main__":
    directory_base = dir_url
    fileExtList = [".mp3", ".wav"]
    for root, directory, file_list in os.walk(directory_base):
        for file_name in file_list:
            if os.path.splitext(file_name)[1] in fileExtList:
                file_path = os.path.join(root, file_name)
                title, artists, album = getInfo(file_path)
                print(title, artists, album,sep=', ')
                title = title.strip().replace('?','').replace('|','')
                if title.strip():
                    # 取到title
                    file_path = rename(file_path, title) # 重命名
                moveByArtist(file_path, artists, album) # 移动