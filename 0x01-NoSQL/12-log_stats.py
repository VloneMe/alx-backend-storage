#!/usr/bin/env python3
"""
Module: nginx_logs_info

This module provides a function to print information about the nginx logs collection.
"""

from pymongo import MongoClient

def print_nginx_logs_info():
    """
    Print information about the nginx logs collection.
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    
    # Access the nginx logs collection
    collection = client.logs.nginx
    
    # Print total number of documents in the collection
    print(f"{collection.estimated_document_count()} logs")
    
    # Print counts for each HTTP method
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        method_count = collection.count_documents({'method': method})
        print(f"\t{method}: {method_count}")
    
    # Count and print status check logs
    check_get = collection.count_documents({'method': 'GET', 'path': "/status"})
    print(f"{check_get} status check")

if __name__ == "__main__":
    print_nginx_logs_info()
