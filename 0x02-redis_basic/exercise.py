#!/usr/bin/env python3
"""module for cache class"""
import uuid
import redis
from typing import Union, Callable, Optional


class Cache:
    """object for storing"""

    def __init__(self) -> None:
        """initialize an instance"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store data in redis and return the key"""
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(self, key: str,
            fn: Optional(Callabale) = None) -> Union[str, bytes, int, float]:
        """retrieve a value from redis storage"""
        value = self._redis.get(key)
        return fn(value) if fn is not None else value

    def get_str(self, key: str) -> Optional(str):
        """Retrieves a string value from a Redis data storage."""
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional(int):
        """Retrieves an integer value from a Redis data storage."""
        return self.get(key, lambda d: int(d))
