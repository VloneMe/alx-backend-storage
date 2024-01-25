# web.py

import redis
import requests
from functools import wraps
from typing import Callable

def cache_and_track_page(fn: Callable) -> Callable:
    """
    Decorator for handling HTTP requests with caching and tracking.

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
        redis_client.incr(f'count:{url}')
        cached_data = redis_client.get(f'cached_data:{url}')
        
        if cached_data:
            return cached_data.decode('utf-8')

        response = fn(url)
        redis_client.setex(f'cached_data:{url}', 10, response)
        return response

    return wrapper

@cache_and_track_page
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
