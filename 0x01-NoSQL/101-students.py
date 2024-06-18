#!/usr/bin/env python3
"""Task 14"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score in descending order.
    Each student document will include the average score
    with key 'averageScore'.

        Returns:
            - A list of students with their average score.
    """
    arg = [
        {
            "$addFields": {
                "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]
    students = list(mongo_collection.aggregate(arg))
    return students
