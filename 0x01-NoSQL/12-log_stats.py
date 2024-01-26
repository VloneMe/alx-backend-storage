#!/usr/bin/env python3
"""
Python script that provides some stats about Nginx logs stored in MongoDB:

Aggregation operations
"""
from pymongo import MongoClient
from typing import Tuple, List, Dict

def get_nginx_stats() -> Tuple[int, List[Dict[str, int]], int]:
    """
    Queries nginx collection for specific data.

    Returns a tuple containing:
        - Total count of all documents in the collection.
        - Count of each HTTP method in the collection.
        - Count of each GET calls to the /status path.
    """
    client: MongoClient = MongoClient()
    db = client.logs
    collection = db.nginx
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    
    method_stats = [{'method': method, 'count': collection.count_documents({'method': method})} for method in methods]
    doc_count = collection.estimated_document_count()
    status_path_stats = collection.count_documents({'method': 'GET', 'path': '/status'})
    
    client.close()
    return doc_count, method_stats, status_path_stats

def print_nginx_stats() -> None:
    """
    Prints statistics from the nginx query.
    """
    doc_count, method_stats, status_path_stats = get_nginx_stats()
    print(f'{doc_count} logs')
    print('Methods:')
    for method in method_stats:
        print(f'\tmethod {method["method"]}: {method["count"]}')
    print(f'{status_path_stats} status check')

if __name__ == '__main__':
    print_nginx_stats()
