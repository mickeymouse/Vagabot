from functools import wraps
import asyncio

def bg_task(delay=60) :
    def decorator(func) :
        @wraps(func)
        @asyncio.coroutine
        def wrapper(*args, **kwargs) :
            while True :
                yield from func(*args, **kwargs)
                yield from asyncio.sleep(delay)
        return wrapper
    return decorator
