import threading
import asyncio
from aiohttp import web

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'


def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

@asyncio.coroutine
def hello():
    print('Hello, world! (%s)' % threading.currentThread())
    # 异步调用asyncio.sleep(1):
    r = yield from asyncio.sleep(1) # yield from 可以调用另一个generator
    print('Hello again! (%s)' % threading.currentThread())

async def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = await connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    await writer.drain()
    while True:
        line = await reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()



# def my_generator():
    
#     for i in range(3):
#         print('before {}'.format(i))
#         n = yield 99
#         print('after: {},{}'.format(i,n))

if __name__ == '__main__':
    # c = consumer() # generator
    # produce(c)


    # def chain(*iterables):
    #     for it in iterables:
    #         yield from it
    #         print('hh')

    # s = 'ABC'
    # t = tuple(range(3))
    # l = list(chain(s, t))
    # print(l)


    # # 获取EventLoop:
    # loop = asyncio.get_event_loop()

    # tasks = [hello(), hello()]
    # # 执行corountine:
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()

    loop = asyncio.get_event_loop()
    tasks = [wget(host) for host in ['www.bilibili.com',
        'www.baidu.com', 'www.ustc.edu.cn']]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()














