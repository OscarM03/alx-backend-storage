#!/usr/bin/env python3
"""List all"""


def list_all(mongo_collection):
    """
    Lists all documents in the specified MongoDB collection.
    Args:
        - mongo_collection (pymongo.collection.Collection):
        - The pymongo collection object.
    Returns:
        - A list of documents (dictionaries).
        - Returns an empty list if no documents are found.
    """
    documents = list(mongo_collection.find())
    return documents if documents else []
