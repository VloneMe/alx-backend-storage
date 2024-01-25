#!/usr/bin/env python3
"""
A module with tools for request caching and tracking.
"""

import redis
import requests
from functools import wraps
from typing import Callable

redis_instance = redis.Redis()
"""
The module-level Redis instance.
"""

def cache_and_track(method: Callable) -> Callable:
    """
    Decorator to cache the output of fetched data and track the request count.
    
    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function for caching the output and tracking the request count.
        
        Args:
            url (str): The URL to be accessed.

        Returns:
            str: The content of the URL.
        """
        redis_instance.incr(f'request_count:{url}')
        cached_result = redis_instance.get(f'cached_result:{url')

        if cached_result:
            return cached_result.decode('utf-8')

        result = method(url)
        redis_instance.set(f'request_count:{url}', 0)
        redis_instance.setex(f'cached_result:{url}', 10, result)
        return result

    return wrapper

@cache_and_track
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response,
    and tracking the request count.

    Args:
        url (str): The URL to be accessed.

    Returns:
        str: The content of the URL.
    """
    return requests.get(url).text
