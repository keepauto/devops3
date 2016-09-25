import threading
import time
from Queue import Queue


class Th(threading.Thread):
    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.setName(thread_name)
        self.Q = Queue(1)
        self.Next = None

    def run(self):
        while True:
            num = self.Q.get()
            if num >= 1000000:
                self.Next.Q.put(num)
                break
            else:
                num += 1
                self.Next.Q.put(num)


if __name__ == "__main__":
    num = 0
    th_list=[]
    th_list.append(Th("T0"))
    for i in range(1, 10):
        th_list.append(Th("T%d" % i))
        th_list[i-1].Next=th_list[i]
    th_list[-1].Next = th_list[0]

    for i in th_list:
        i.start()
    print int(time.time())
    th_list[0].Q.put(num)


    for i in th_list:
        i.join()
    print int(time.time())
