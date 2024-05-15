#!/usr/bin/env python3
"""modles"""
from typing import Union, Callable, Optional, Any
from functools import wraps
import uuid
import redis


def count_calls(method: Callable) -> Callable:
    """ mo"""

    @wraps(method)
    def wrapper(self, *args, **kwds) -> Any:
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ call fun"""

    @wraps(method)
    def wrapper(self, *args, **kwds) -> Any:
        inp = "{}:inputs".format(method.__qualname__)
        out = "{}:outputs".format(method.__qualname__)
        rv = method(self, *args, **kwds)

        self._redis.rpush(inp, str(args))
        self._redis.rpush(out, str(rv))
        return rv
    return wrapper


def replay(method: Callable) -> None:
    """ fun"""

    n = method.__qualname__
    cache = redis.Redis()
    num = cache.get(n).decode("utf-8")
    print("{} was called {} times:".format(n, num))
    inputs = cache.lrange(n + ":inputs", 0, -1)
    outputs = cache.lrange(n + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(n, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    """ cache class"""

    def __init__(self) -> None:
        """ Redis client as a private variable"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store fun"""

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """get function"""

        data = self._redis.get(key)
        if data:
            if fn:
                return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """grt str fun"""

        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """ get int function"""

        return self.get(key, lambda d: int(d))
