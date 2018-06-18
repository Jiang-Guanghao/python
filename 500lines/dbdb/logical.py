#!/usr/bin/env python3
# -*- coding: utf-8 -*_

class LogicalBase(object):
    def get(self, key):
        if not self._storage.locked:
            self._refresh_tree_ref()
        return self._get(self._follow(self._tree_ref), key)

    def set(self, key, value):
        if self._storage.locked:
            self._refresh_tree_ref()
        self._tree_ref = self._insert(self._follow(self._tree_ref), key, self.value_ref_class(value))
        
    def commit(self):
        self._tree_ref.store(self._storage)
        self._storage.commit_root_address(self._tree_ref.address)

    def store(self, storage):
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = store.write(self.referent_to_string(self._regerent))

    def _refresh_tree_ref(self):
        self._tree_ref = self.node_ref_class(address=self._storage._get_root_assress())

class ValueRef(object):
    def store(self, storage):
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_string(self._referent))


    