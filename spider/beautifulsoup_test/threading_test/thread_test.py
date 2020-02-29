import time
from  threading import Thread


def sleep_task(sleep_time):
    print("sleep {} seconds start".format(sleep_time))
    time.sleep(sleep_time)
    print("sleep {} seconds end".format(sleep_time))

class sleepThrad(Thread):
    def __init__(self,sleep_time):
        self.sleep_time = sleep_time
        super().__init__()#子类调用父类的__init__()方法进行必要的初始化

    def run(self):
        print("sleep {} seconds start".format(self.sleep_time))
        time.sleep(self.sleep_time)
        print("sleep {} seconds end".format(self.sleep_time))

def sleep_task1():
    print("sleep 2 seconds start")
    time.sleep(2)
    print("sleep 2 seconds end")

def sleep_task2():
    print("sleep 3 seconds start")
    time.sleep(3)
    print("sleep 3 seconds end")

# if __name__ == '__main__':
#     # thread1 = Thread(target=sleep_task1)
#     # thread2 = Thread(target=sleep_task2)
#     # thread1.start()
#     # thread2.start()
#
#     thread1 = Thread(target=sleep_task,args=(2,))
#     thread2 = Thread(target=sleep_task,args=(3,))
#     thread1.start()
#     thread2.start()


if __name__ == '__main__':
    start_time = time.time()
    t1 = sleepThrad(1)
    t1.setDaemon(True)
    t2 = sleepThrad(2)
    t2.setDaemon(True)
    t1.start()
    t2.start()
    # t1.join()
    # t2.join()
    end_time = time.time()
    print('last_time:{}'.format(end_time-start_time))