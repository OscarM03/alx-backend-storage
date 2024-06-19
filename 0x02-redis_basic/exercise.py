#!/usr/bin/env python3
"""Writing strings to Redis"""

import uuid
import redis
from typing import Union


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
