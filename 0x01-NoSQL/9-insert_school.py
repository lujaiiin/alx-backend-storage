#!/usr/bin/env python3
"""modules"""


def insert_school(mongo_collection, **kwargs):
    """insert school function"""

    return mongo_collection.insert_one(kwargs).inserted_id
