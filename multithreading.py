# --------Multi-threading------------
import time, threading

def loop():
    print('thread {} is running...'.format(threading.current_thread().name))
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended' % (threading.current_thread().name))

# print('thread %s is running...' % threading.current_thread().name)
# t = threading.Thread(target=loop, name='LoopThread')
# t.start()
# t.join()
# print('thread %s ended.' % threading.current_thread().name)

balance = 0

def change_it(n):
    # 如果不加锁的话，这个函数可能跑到一半跳出来
    global balance
    balance = balance + n
    balance = balance - n

lock = threading.Lock()
def run_thread(n):
    lock.acquire()
    try:
        for i in range(2000000):
            change_it(n)
    finally:
        lock.release()

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
