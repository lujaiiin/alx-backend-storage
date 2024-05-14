#!/usr/bin/env python3
"""modules"""


def update_topics(mongo_collection, name, topics):
    """update topics function"""

    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}},)
