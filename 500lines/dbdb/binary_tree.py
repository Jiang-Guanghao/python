#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dbdb.logical import LogicalBase

class BinaryTree(LogicalBase):
    def _get(self, node, key):
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def _set(self, node, key, value_ref):
        if node is None:
            new_node = BinaryNode(self.node_ref_class(), key, value_ref, self.node_ref_class(), 1)
        elif key < node.key:
            new_node = BinaryNode.from_node(node, left_ref=self._insert( self._follow(node.left_ref), key, value_ref) )
        elif key > node.key:
            new_node = BinaryNode.from_node(node, right_ref=self._insert( self._follow(node.right_ref), key, value_ref) )
        else:
            new_node = BinaryNode.from_node(node, value_ref=value_ref)
        return self.node_ref_class(referent=new_node)