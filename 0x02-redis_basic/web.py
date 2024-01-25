#!/usr/bin/env python3
"""
Caching and tracking module for requests.
"""

import redis
import requests
from functools import wraps
from typing import Callable

def cache_and_track_request(fn: Callable) -> Callable:
    """
    Decorator for fetching content with caching and tracking.

    Args:
        fn (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """
    @wraps(fn)
    def wrapper(endpoint: str) -> str:
        """
        Wrapper function to check cache and track usage count.

        Args:
            endpoint (str): The endpoint to be accessed.

        Returns:
            str: The content fetched from the endpoint.
        """
        redis_client = redis.Redis()
        redis_client.incr(f'request_count:{endpoint}')
        cached_content = redis_client.get(f'cached_content:{endpoint}')
        
        if cached_content:
            return cached_content.decode('utf-8')

        response = fn(endpoint)
        redis_client.setex(f'cached_content:{endpoint}', 10, response)
        return response

    return wrapper

@cache_and_track_request
def fetch_content(endpoint: str) -> str:
    """
    Makes an HTTP request to the specified endpoint.

    Args:
        endpoint (str): The endpoint to be accessed.

    Returns:
        str: The content fetched from the endpoint.
    """
    response = requests.get(endpoint)
    return response.text

# Example Usage:
if __name__ == "__main__":
    # Example Endpoint
    example_endpoint = "https://www.example.com"
    
    # Access the endpoint multiple times
    for _ in range(3):
        content = fetch_content(example_endpoint)
        print(f"Fetched content from endpoint. Length: {len(content)}")

    # Print request count for the endpoint
    request_count = redis_client.get(f'request_count:{example_endpoint}')
    print(f"Request count for the endpoint: {int(request_count)}")
