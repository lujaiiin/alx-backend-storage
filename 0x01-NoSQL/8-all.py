#!/usr/bin/env python3
"""modules"""


def list_all(mongo_collection):
    """list all function"""

    return mongo_collection.find()
