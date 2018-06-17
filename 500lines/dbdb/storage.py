#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import portalocker

class Storage(object):
    def lock(self):
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.lock = True
            return True
        else:
            return False