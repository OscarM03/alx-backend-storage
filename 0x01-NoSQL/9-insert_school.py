#!/usr/bin/env python3
"""Insert a document"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the specified MongoDB
    collection based on kwargs.

    Returns:
        - The new _id of the inserted document.
    """
    res = mongo_collection.insert_one(kwargs)
    return res.inserted_id
