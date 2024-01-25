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

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the provided key and optional conversion function.

        Args:
            key (str): The key under which the data is stored.
            fn (Callable, optional): A callable function to convert the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, or None if the key does not exist.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve a string from Redis using the provided key.

        Args:
            key (str): The key under which the string is stored.

        Returns:
            Union[str, None]: The retrieved string, or None if the key does not exist.
        """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve an integer from Redis using the provided key.

        Args:
            key (str): The key under which the integer is stored.

        Returns:
            Union[int, None]: The retrieved integer, or None if the key does not exist.
        """
        return self.get(key, fn=int)

# Example Usage:
if __name__ == "__main__":
    cache_instance = Cache()

    # Store data
    key_str = cache_instance.store("Hello, World!")
    key_int = cache_instance.store(42)

    # Retrieve data with automatic conversion
    retrieved_str = cache_instance.get_str(key_str)
    retrieved_int = cache_instance.get_int(key_int)

    print(f"Retrieved String: {retrieved_str}")
    print(f"Retrieved Integer: {retrieved_int}")

    # Retrieve and print the count for the store method
    store_method_count = cache_instance._redis.get("Cache.store")
    print(f"Number of calls to store method: {int(store_method_count)}")
