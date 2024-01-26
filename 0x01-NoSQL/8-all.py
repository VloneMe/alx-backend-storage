#!/usr/bin/env python3
"""
Module: document_listing

This module provides a function to list all documents in a MongoDB collection.
"""

def list_all(mongo_collection):
    """
    Lists all documents in the given MongoDB collection.

    :param mongo_collection: A MongoDB collection object.
    :return: A cursor containing all documents in the collection.
    """
    return mongo_collection.find()
