import subprocess
import os
from time import time

proc = subprocess.Popen(
    ['echo', 'Hello from the child!'],
    stdout=subprocess.PIPE)
out, err = proc.communicate()
print(out.decode('utf-8'))

print('# ---------------------------------------------------------------------------------------')

proc = subprocess.Popen(['sleep', '0.3'])
while proc.poll() is None: # poll:检查这个进程是否结束，如果没有结束返回None，否则返回return code
    print('Working...')
    i = 0
    while i < 100000:
        i = i + 1
    print('next roll...')

print('Exit status', proc.poll())

print('# ---------------------------------------------------------------------------------------')

def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc

start = time()
procs = []
for _ in range(10):
    proc = run_sleep(0.1) # 把10个子进程都启动起来
    procs.append(proc)

for proc in procs:
    proc.communicate()
end = time()
print('Finished in {:.3f} seconds'.format(end-start)) # 若所有子进程逐个运行，总延迟时间可能要长10倍

print('# ---------------------------------------------------------------------------------------')
'''
需求： 从Python程序向子进程输送数据，然后获取子进程的输出信息
用命令行式的openssl工具加密一些数据
'''
def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Q13S\x11'
    proc = subprocess.Popen(['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc

procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    procs.append(proc)

for proc in procs:
    out, err = proc.communicate()
    print(out[-10:])

print('# ---------------------------------------------------------------------------------------')

'''
UNIX管道：用平行的子进程来搭建平行的链条；
所谓搭建链条，就是把第一个子进程的输出，与第二个子进程的输入联系起来
'''
def run_md5(input_stdin):
    proc = subprocess.Popen(
        ['md5'],
        stdin=input_stdin,
        stdout=subprocess.PIPE)
    return proc

input_procs = []
hash_procs = []
for _ in range(3):
    pass




