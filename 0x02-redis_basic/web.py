#!/usr/bin/env python3

import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis client
redis_client = redis.StrictRedis()

def count_access(func: Callable) -> Callable:
    """
    Decorator to track the number of times a URL is accessed.
    
    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """
        Wraps the original function and increments the access count for the URL.
        
        Args:
            url (str): The URL to be accessed.

        Returns:
            str: The HTML content of the URL.
        """
        # Increment access count for the URL
        redis_client.incr(f"count:{url}")
        return func(url)
    return wrapper

def cache_result(timeout: int) -> Callable:
    """
    Decorator to cache the result of a function with a specified timeout.
    
    Args:
        timeout (int): The expiration time for the cache in seconds.

    Returns:
        Callable: The decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            """
            Wraps the original function and caches the result with the specified timeout.
            
            Args:
                url (str): The URL to be accessed.

            Returns:
                str: The HTML content of the URL.
            """
            cache_key = f"cache:{url}"
            cached_result = redis_client.get(cache_key)

            if cached_result is not None:
                return cached_result.decode('utf-8')
            
            result = func(url)
            redis_client.setex(cache_key, timeout, result)
            return result
        return wrapper
    return decorator

@count_access
@cache_result(timeout=10)
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL.
    
    Args:
        url (str): The URL to be accessed.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text
