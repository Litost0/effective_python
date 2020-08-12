import asyncio
import random, time

# ANSI colors
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)

async def makerandom(idx: int, threshold: int = 6) -> int:
    print(c[idx + 1] + f"Initiated makerandom({idx}).")
    i = random.randint(0, 10)
    while i <= threshold:
        print(c[idx + 1] + f"makerandom({idx}) == {i} too low; retrying.")
        # 小于一个threshold的话，跳出去执行其他的协程
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    print(c[idx + 1] + f"---> Finished: makerandom({idx}) == {i}" + c[0])
    return i

async def main():
    # asyncio.gather(*aws, loop=None, ..)
    # run awaitable objects in the aws sequence concurrently
    # return: aggregate list of returned values
    res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3))) 
    return res

if __name__ == "__main__":
    random.seed(444)
    # run: execute the coroutine and return the result
    r1, r2, r3 = asyncio.run(main())
    print()
    print(f"r1: {r1}, r2: {r2}, r3: {r3}")


