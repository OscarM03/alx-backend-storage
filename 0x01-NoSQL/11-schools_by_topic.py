#!/usr/bin/env python3
"""Finding a specific thing in a document"""


def schools_by_topic(mongo_collection, topic):
    """
    Retrieves all documents from the specified MongoDB
    collection that contain a certain topic.

    Returns:
        - A list of documents (dictionaries) that contain the specified topic.
    """
    filter_name = {"topic": topic}
    documents = list(mongo_collection.find(filter_name))
    return documents
