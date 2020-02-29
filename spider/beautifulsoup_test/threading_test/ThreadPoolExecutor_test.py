# encoding = utf-8

import time


# 创建一个线程子类
from distributed.threadpoolexecutor import ThreadPoolExecutor

def moyu_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s 开始摸鱼 %s" % (threadName, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        counter -= 1


if __name__ == '__main__':
    pool = ThreadPoolExecutor(20)
    for i in range(1,5):
        pool.submit(moyu_time('xiaoshuaib'+str(i),1,3))
