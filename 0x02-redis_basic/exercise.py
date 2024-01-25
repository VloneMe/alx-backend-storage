#!/usr/bin/env python3
"""
Cache module.

This module defines a Cache class that utilizes a Redis client to store and retrieve data.
"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps

class Cache:
    """
    Cache class for storing and retrieving data in/from Redis.
    """

    def __init__(self) -> None:
        """
        Cache class constructor.

        Initializes a Redis client and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """
        Decorator to count the number of times a method is called.

        Args:
            method (Callable): The method to be decorated.

        Returns:
            Callable: The decorated method.
        """
        key = method.__qualname__

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            self._redis.incr(key)
            return method(self, *args, **kwargs)

        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return the generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The generated key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

# Example Usage:
if __name__ == "__main__":
    cache_instance = Cache()

    # Call store method multiple times
    for _ in range(5):
        cache_instance.store("Test Data")

    # Retrieve and print the count for the store method
    store_method_count = cache_instance._redis.get("Cache.store")
    print(f"Number of calls to store method: {int(store_method_count)}")
