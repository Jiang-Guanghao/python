#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import struct
import portalocker


class Storage(object):
    def lock(self):
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.lock = True
            return True
        else:
            return False

    def commit_root_address(self, root_address):
        self.lock()
        self._f.flush()
        self._seek_superblock()
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()