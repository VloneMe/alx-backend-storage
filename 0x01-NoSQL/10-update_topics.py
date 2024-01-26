#!/usr/bin/env python3
"""
Module: school_topic_update

This module provides a function to update the topics of a school document in a MongoDB collection.
"""

def update_topics(mongo_collection, name, topics):
    """
    Updates the topics of a school document in the given MongoDB collection based on the name.

    :param mongo_collection: A MongoDB collection object.
    :param name: The name of the school whose topics need to be updated.
    :param topics: The new topics to be set for the school.
    :return: None
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
