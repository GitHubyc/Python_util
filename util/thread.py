import threading
import time
import random


def takeSleep(id, name):
    print(name + '-' + id + ':线程开始运行...')
    time.sleep(random.randint(0, 3))
    print(name + '-' + id + ':线程任务结束')


print('主程序开始运行...')
threads = []
for i in range(0, 5):
    t = threading.Thread(target=takeSleep, args=(str(i), 'zhangphil'))
    threads.append(t)
    t.start()

print('主程序运行中...')

# 等待所有线程任务结束。
for t in threads:
    t.join()

print("所有线程任务完成")