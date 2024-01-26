#!/usr/bin/env python3
"""
Module: log_statistics

This module provides a function to retrieve and print statistics from a MongoDB collection of nginx logs.
"""

from pymongo import MongoClient

def log_stats():
    """
    Retrieve and print statistics from the nginx logs collection.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    
    # Access the logs collection
    logs_collection = client.logs.nginx
    
    # Count total logs
    total = logs_collection.count_documents({})
    
    # Count logs by HTTP methods
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})
    
    # Count status check logs
    path = logs_collection.count_documents({"method": "GET", "path": "/status"})
    
    # Print statistics
    print(f"{total} logs")
    print("Methods:")
    print(f"\tGET: {get}")
    print(f"\tPOST: {post}")
    print(f"\tPUT: {put}")
    print(f"\tPATCH: {patch}")
    print(f"\tDELETE: {delete}")
    print(f"{path} status check")

if __name__ == "__main__":
    log_stats()
