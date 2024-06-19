#!/usr/bin/env python3
"""Writing strings to Redis"""

import uuid
import redis
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ count how many times methods of the Cache class are called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Increment the count for the method's qualified name"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Stores history of inputs and outputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """actual storage"""
        input_s = f"{method.__qualname__}:inputs"
        output_s = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_s, str(args))

        res = method(self, *args, **kwargs)
        self._redis.rpush(output_s, str(res))

        return res
    return wrapper


def replay(method: Callable) -> None:
    """Displsy history of calls of a particular function"""
    redis_client = method.__self__._redis
    input_s = f"{method.__qualname__}:inputs"
    output_s = f"{method.__qualname__}:outputs"

    inputs = redis_client.lrange(input_s, 0, -1)
    outputs = redis_client.lrange(output_s, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")

    for key, value in zip(inputs, outputs):
        print(
            f"{method.__qualname__}(*{key.decode('utf-8')}) "
            f"-> {value.decode('utf-8')}")


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a randomly generated key.

        :param data: The data to store (str, bytes, int, or float).
        :return: The generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)

        return key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Gets data from Redis"""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Conversion to str"""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Conversion to Int"""
        return self.get(key, lambda d: int(d))
