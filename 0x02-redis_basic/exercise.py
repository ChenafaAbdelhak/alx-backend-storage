#!/usr/bin/env python3
"""module for cache class"""
import uuid
import redis
from typing import Union


class Cache:
    """object for storing"""

    def __init__(self) -> None:
        """initialize an instance"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store data in redis and return the key"""
        data_key = uuid.uuid4()
        self._redis.set(data_key, data)
        return data_key