import threading
import random
import time

philosophersLog = []
chopsticks = []

mutex = threading.Lock()

# philosopher 哲学家的编号。
# pickLeftFork 和 pickRightFork 表示拿起左边或右边的叉子。
# eat 表示吃面。
# putLeftFork 和 putRightFork 表示放下左边或右边的叉子。
class DiningPhilosophers(threading.Thread):
    def __init__(self,philosopher,conn,sem,times):
        super(DiningPhilosophers, self).__init__()
        self.philosopher = philosopher
        self.conn = conn
        self.times = times
        self.sem = sem

    def run(self):
       
        for i in range(self.times):
            global chopsticks
            global mutex
            self.sem.acquire()
            self.thinking()
            self.pickLeftFork()
            self.pickRightFork()
            self.eat()
            self.putLeftFork()
            self.putRightFork()
            self.sem.release()
            
    def thinking(self):
        print(f'philosopher{self.philosopher} is thinking')
        time.sleep(random.randint(1,5))


    def pickLeftFork(self):
        chopsticks[self.philosopher].acquire()
        #print(f'philosopher{self.philosopher} pick LeftFork')
        mutex.acquire()
        philosophersLog.append([self.philosopher,1,1])
        mutex.release()
        

    def pickRightFork(self):
        chopsticks[(self.philosopher+1)%5].acquire()
        #print(f'philosopher{self.philosopher} pick RightFork')
        mutex.acquire()
        philosophersLog.append([self.philosopher,2,1])
        mutex.release()

    def eat(self):
        print(f'philosopher{self.philosopher} is eating')
        time.sleep(random.randint(1,5))
        mutex.acquire()
        philosophersLog.append([self.philosopher,0,3])
        mutex.release()

    def putLeftFork(self):
        chopsticks[self.philosopher].release()
        #print(f'philosopher{self.philosopher} put LeftFork')
        mutex.acquire()
        philosophersLog.append([self.philosopher,1,2])
        mutex.release()


    def putRightFork(self):
        chopsticks[(self.philosopher+1)%5].release()
        #print(f'philosopher{self.philosopher} put RightFork')
        mutex.acquire()
        philosophersLog.append([self.philosopher,2,2])
        mutex.release()

def InputTimes():
    try:
        r = int(input("请输入需要进餐的次数(1-60)"))
    except Exception as e:
        print(e)
        r = 0
    return r

if __name__ == "__main__":
    conn = threading.Condition()   # 条件变量锁
    sem = threading.BoundedSemaphore(4)  # 最多允许4个线程同时运行
    times = InputTimes()

    if times > 0 and times <= 60:
        threads = []
        for i in range(5):
            chopsticks.append(threading.Lock())

        for i in range(5):
            t = DiningPhilosophers(philosopher = i,conn = conn,sem = sem, times = times)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print(philosophersLog)
    else :
        print("输入错误，请输入整数1-60")

    