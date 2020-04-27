# coding:utf-8
import itchat

# 先登录
itchat.login()

# 获取好友列表
friends = itchat.get_friends(update=True)[0:]
for i in friends:
    # 获取个性签名
    signature = i["Signature"]
    print(signature)
