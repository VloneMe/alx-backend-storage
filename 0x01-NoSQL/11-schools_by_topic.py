#!/usr/bin/env python3
"""
Module: python_learning_resources

This module provides a function to retrieve a list of schools based on a specific topic from a MongoDB collection.
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools that focus on a specific topic.

    :param mongo_collection: A MongoDB collection object.
    :param topic: The topic for which schools are to be retrieved.
    :return: A cursor containing school documents matching the specified topic.
    """
    return mongo_collection.find({"topics": topic})
