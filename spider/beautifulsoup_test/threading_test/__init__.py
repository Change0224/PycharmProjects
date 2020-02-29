from threading import Thread
import  time

class sleepThrad(Thread):
    def __init__(self,sleep_time):
        self.sleep_time = sleep_time
        super().__init__()#子类调用父类的__init__()方法进行必要的初始化

    def run(self):
        print("sleep {} seconds start".format(self.sleep_time))
        time.sleep(self.sleep_time)
        print("sleep {} seconds end".format(self.sleep_time))

if __name__ == '__main__':
    t1 = sleepThrad(2)
    t2 = sleepThrad(3)
    t1.start()
    t2.start()
    print("main end")
