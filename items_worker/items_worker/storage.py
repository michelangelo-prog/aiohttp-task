from sqlitedict import SqliteDict

from .config import PATH_TO_DB


def get_storage():
    return SqliteDict(PATH_TO_DB, autocommit=True)


def add_to_storage(key, value):
    storage = get_storage()
    storage[key] = value


def get_from_storage(key):
    storage = get_storage()
    return storage[key]
