#!/usr/bin/env python3
"""
Redis client module.

This module defines a Cache class that utilizes
a Redis client to store and retrieve data.
"""

import redis
from uuid import uuid4
from functools import wraps
from typing import Any, Callable, Optional, Union


def count_calls(method: Callable) -> Callable:
    """
    The decorator for Cache class methods to track call count.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        """
        This wraps called method and adds its call
        count to Redis before execution.

        Args:
            self (Any): The instance of the Cache class.
            *args: Variable arguments.
            **kwargs: Keyword arguments.

        Returns:
            str: The result of the original method.
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    This decorator for Cache class method to
    track arguments and outputs.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """
        This wraps called method and tracks its passed arguments
        by storing them in Redis.

        Args:
            self (Any): The instance of the Cache class.
            *args: Variable arguments.

        Returns:
            str: The result of the original method.
        """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """
    This check Redis for how many times a function
    was called and display:
        - How many times it was called
        - Function args and output for each call

    Args:
        fn (Callable): The function to be checked.
    """
    client = redis.Redis()
    calls = client.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]

    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


class Cache:
    """
    Caching class.
    """
    def __init__(self) -> None:
        """
        This initialize a new cache object.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This stores data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The generated key under which the data is stored.
        """
        key = str(uuid4())
        client = self._redis
        client.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Gets key's value from Redis and converts
        the result byte into the correct data type.

        Args:
            key (str): The key under which the data is stored.
            fn (Optional[Callable]): A callable function
            to convert the retrieved data.

        Returns:
            Any: The retrieved data, or None if the key does not exist.
        """
        client = self._redis
        value = client.get(key)

        if not value:
            return

        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if callable(fn):
            return fn(value)

        return value

    def get_str(self, data: bytes) -> str:
        """
        This converts bytes to a string.

        Args:
            data (bytes): The data in bytes.

        Returns:
            str: The converted string.
        """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """
        This converts bytes to integers.

        Args:
            data (bytes): The data in bytes.

        Returns:
            int: The converted integer.
        """
        return int(data)
