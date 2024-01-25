#!/usr/bin/env python3
"""
Cache module.

This module defines a Cache class that utilizes
a Redis client to store data.
"""

import redis
import uuid
from typing import Union

class Cache:
    """
    This cache class for storing data in Redis.
    """

    def __init__(self) -> None:
        """
        This cache class constructor.

        This initializes a Redis client and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This store data in Redis and return the generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The generated key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

"""# Example Usage: """
if __name__ == "__main__":
    cache_instance = Cache()

    """# Store a string """
    string_key = cache_instance.store("Hello, World!")
    print(f"String Key: {string_key}")

    """# Store an integer """
    int_key = cache_instance.store(42)
    print(f"Integer Key: {int_key}")

    """# Store a float """
    float_key = cache_instance.store(3.14)
    print(f"Float Key: {float_key}")

    """# Store bytes """
    bytes_key = cache_instance.store(b"Binary Data")
    print(f"Bytes Key: {bytes_key}")
