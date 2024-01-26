#!/usr/bin/env python3
"""
Module: document_insertion

This module provides a function to insert a new document into a MongoDB collection.
"""

def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the given MongoDB collection.

    :param mongo_collection: A MongoDB collection object.
    :param kwargs: Key-value pairs representing the fields and values for the new document.
    :return: The ObjectId of the newly inserted document.
    """
    new_document = mongo_collection.insert_one(kwargs)
    return new_document.inserted_id
