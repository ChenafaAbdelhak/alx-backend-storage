#!/usr/bin/env python3
"""module for cache class"""
import uuid
import redis
from typing import Union, Callable


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
            fn: Callabale = None) -> Union[str, bytes, int, float]:
        """retrieve a value from redis storage"""
        value = self._redis.get(key)
        return fn(value) if fn is not None else value

    def get_str(self, key: str) -> str:
        """Retrieves a string value from a Redis data storage."""
        data = self._redis.get(key)
        if data is not None:
            return data.decode("utf-8")
        return None

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from a Redis data storage."""
        data = self._redis.get(key)
        if data is not None:
            return int(data)
        return None
