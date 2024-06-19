#!/usr/bin/env python3
"""Writing strings to Redis"""

import uuid
import redis
from typing import Union, Optional, Callable


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

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
