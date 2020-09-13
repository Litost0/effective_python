import threading
import asyncio
from aiohttp import web

# def consumer():
#     r = ''
#     while True:
#         n = yield r
#         if not n:
#             return
#         print('[CONSUMER] Consuming %s...' % n)
#         r = '200 OK'


# def produce(c):
#     c.send(None)
#     n = 0
#     while n < 5:
#         n = n + 1
#         print('[PRODUCER] Producing %s...' % n)
#         r = c.send(n)
#         print('[PRODUCER] Consumer return: %s' % r)
#     c.close()



async def wget(host):
    print('wget %s...' % host)
    reader, writer = await asyncio.open_connection(host, 80)
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

    # EventLoop的直接调用：
    # loop = asyncio.get_event_loop()
    # tasks = [wget(host) for host in ['www.bilibili.com',
    #     'www.baidu.com', 'www.ustc.edu.cn']]
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()


    # 更常见的实现：不直接调用EventLoop的底层方法，而是使用asyncio.run()等更高级的函数
    HOSTS = ['www.bilibili.com', 'www.baidu.com', 'www.ustc.edu.cn']

    async def main():
        tasks = [wget(host) for host in HOSTS]
        await asyncio.gather(*tasks)

    asyncio.run(main())













