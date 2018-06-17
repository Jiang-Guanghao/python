#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class DBDB(object):
    def __init__(self, f):
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)
    
    def __get_item__(self, key):
        self._assert_not_closed()
        return self._tree.get(key)

    def __set_item__(self, key, value):
        self._assert_not_closed()
        return self._tree.set(key, value)

    def commit(self):
        self._assert_not_closed()
        self._tree.commit()

    def _assert_not_closed():
        if self._storage.closed:
            raise ValueError("Database Closed!")