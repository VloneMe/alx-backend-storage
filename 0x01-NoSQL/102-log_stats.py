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
    
    # Print statistics for HTTP methods
    print(f"{total} logs")
    print("Methods:")
    print(f"\tGET: {get}")
    print(f"\tPOST: {post}")
    print(f"\tPUT: {put}")
    print(f"\tPATCH: {patch}")
    print(f"\tDELETE: {delete}")
    print(f"{path} status check")
    
    # Count and print top 10 IPs
    print("IPs:")
    sorted_ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    
    for s in sorted_ips:
        print(f"\t{s.get('_id')}: {s.get('count')}")

if __name__ == "__main__":
    log_stats()
