#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_instance = redis.Redis()
'''The module-level Redis instance.
'''

def cached_data(method: Callable) -> Callable:
    '''Caches the fetched data and tracks access count.
    '''
    @wraps(method)
    def wrapper(url: str) -> str:
        '''Wrapper function for caching the data.
        '''
        redis_instance.incr(f'access_count:{url}')
        cached_result = redis_instance.get(f'cached_result:{url}')
        
        if cached_result:
            return cached_result.decode('utf-8')
        
        result = method(url)
        
        redis_instance.set(f'access_count:{url}', 0)
        redis_instance.setex(f'cached_result:{url}', 10, result)
        
        return result
    return wrapper

@cached_data
def fetch_page_content(url: str) -> str:
    '''Fetches the content of a URL, caches the response, and tracks the request.
    '''
    return requests.get(url).text
