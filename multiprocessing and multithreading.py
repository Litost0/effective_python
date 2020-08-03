import os, time, random, threading
import subprocess
from multiprocessing import Process, Pool, Queue

# print('Process (%s) start...' % os.getpid())

# pid = os.fork()
# if pid == 0:
#     print('I am a child process ({}) and my parent is {}.'.format(os.getpid(), os.getppid()))
# else:
#     print('I ({}) just created a child process ({}).'.format(os.getpid(), pid))


# 子进程要执行的代码
def run_proc(name):
    print('Run child process {} ({})...'.format(name, os.getpid()))


def long_time_task(name):
    print('Run task {} ({})'.format(name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task {} runs {:.2f} seconds.'.format(name, (end-start)))

# 进程间通信，用Queue实现

# 写数据进程执行的代码：
def write(q):
    print('Process to write: {}'.format(os.getpid()))
    for value in ['A', 'B', 'C']:
        print('Put {} to queue...'.format(value))
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码：
def read(q):
    print('Process to read: {}'.format(os.getpid()))
    while True:
        value = q.get(True)
        print('Get {} from queue.'.format(value))

# --------Multi-threading------------
def loop():
    print('thread {} is running...'.format(threading.current_thread().name))
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % threading.current_thread().name)


if __name__ == '__main__':
    # print('Parent process {}.'.format(os.getpid()))
    # p = Process(target=run_proc, args=('test',)) # 创建Process实例
    # print('Child process will start.')
    # p.start() # 启动进程
    # p.join() # 等待子进程结束之后继续运行，用于进程间同步
    # print('Child prodess end.')

    # print('Parent process {}'.format(os.getpid()))
    # p = Pool(10) # 同时进行的进程数
    # for i in range(5):
    #     p.apply_async(long_time_task, args=(i,))
    # print('Waiting for all subprocesses done...')
    # p.close() # 在join之前完成
    # p.join() # 等待所有子进程执行完毕
    # print('All subprocesses done.')

    # print('$ nslookup www.python.org')
    # r = subprocess.call(['nslookup', 'www.python.org'])
    # print('Exit code:', r)

    # print('$ nslookup')
    # p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, 
    #     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
    # print(output.decode('utf-8'))
    # print('Exit code:', p.returncode)

    # 父进程创建Queue，并传给各个子进程：
    print('Parent process: {}'.format(os.getpid()))
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程，写入：
    pw.start()
    # 启动子进程，读出：
    pr.start()
    # 等待pw结束：
    pw.join()
    # 强制结束pr:
    pr.terminate()




















