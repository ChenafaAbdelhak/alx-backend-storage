#!/usr/bin/env python3
"""module for cache class"""
import uuid
import redis
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """decorator that counts the number of times a method is called."""    
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Union[str, bytes, int, float]:
        """Wrapper function that increments the count and calls the original method."""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """object for storing"""

    def __init__(self) -> None:
        """initialize an instance"""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store data in redis and return the key"""
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
        self,
        key: str,
        fn: Callable = None,
    ) -> Union[str, bytes, int, float]:
        """Retrieves a value from a Redis data storage."""
        data = self._redis.get(key)

        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """Retrieves a string value from a Redis data storage."""
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from a Redis data storage."""
        return self.get(key, lambda x: int(x))
