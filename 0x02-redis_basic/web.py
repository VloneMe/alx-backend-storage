#!/usr/bin/env python3

import redis
import requests
from functools import wraps
from typing import Callable

def track_and_cache_page(fn: Callable) -> Callable:
    """
    Decorator for tracking and caching the result of the get_page function.

    Args:
        fn (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """
        Wrapper function that:
        - checks whether a URL's data is cached
        - tracks the usage count of the decorated function

        Args:
            url (str): The URL to be accessed.

        Returns:
            str: The content of the URL.
        """
        redis_client = redis.Redis()
        redis_key_count = f'count:{url}'
        redis_key_cached_data = f'cached_data:{url}'
        
        # Track usage count
        redis_client.incr(redis_key_count)

        # Check if data is cached
        cached_data = redis_client.get(redis_key_cached_data)
        if cached_data:
            return cached_data.decode('utf-8')

        # Fetch data and cache it
        response = fn(url)
        redis_client.setex(redis_key_cached_data, 10, response)
        return response

    return wrapper

@track_and_cache_page
def get_page(url: str) -> str:
    """
    Makes an HTTP request to a given URL.

    Args:
        url (str): The URL to be accessed.

    Returns:
        str: The content of the URL.
    """
    response = requests.get(url)
    return response.text
