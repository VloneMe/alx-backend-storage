#!/usr/bin/env python3
"""
Module: top_students

This module provides a function to retrieve all students from a MongoDB collection, sorted by average score.
"""

def top_students(mongo_collection):
    """
    Returns all students sorted by their average score.

    :param mongo_collection: A MongoDB collection object containing student data.
    :return: A cursor containing student documents sorted by average score in descending order.
    """
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
