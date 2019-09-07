from functools import wraps
import asyncio
import numpy as np


def prettify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f'\ncalling {func.__name__}')
        print(f'args = {args}')
        print(f"sleeping for: {kwargs.get('delay')} sec")
        return func(*args, **kwargs)
    return wrapper


def delay():
    return np.random.rand(1)[0].round(2)


@prettify
async def work(x,y,z,delay=delay):
    await asyncio.sleep(delay)
    print(f'finished: x={x:.2f}, y={y:.2f}, z={z:.2f}, delay={delay:.2f}')
    return z, delay


async def main():
    arr = np.random.rand(3,10).round(2)
    tasks = (work(x,y,x, delay=delay()) for x,y,z in zip(*arr))
    results = await asyncio.gather(*tasks)
    return list(results)


if __name__ == '__main__':
    res = asyncio.run(main())
    print(res)


