# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

from threading import RLock
from weakref import proxy

from .node import Node

class Registry(object):
    """
The "Registry" class provides thread-safe access to node instances.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    def __init__(self, connection):
        """
Constructor __init__(Registry)

:param connection: homee connection instance

:since: 1.0.0
        """

        self._connection = proxy(connection)
        """
homee connection
        """
        self._nodes = { }
        """
Nodes
        """
        self.lock = RLock()
        """
Underlying lock instance
        """
        self.timeout = 10
        """
Lock timeout in seconds
        """
    #

    def __enter__(self):
        """
python.org: Enter the runtime context related to this object.

:since: 1.0.0
        """

        self.lock.acquire(timeout = self.timeout)
    #

    def __exit__(self, exc_type, exc_value, traceback):
        """
python.org: Exit the runtime context related to this object.

:return: (bool) True to suppress exceptions
:since:  1.0.0
        """

        self.lock.release()
        return False
    #

    def add_node(self, node):
        """
Adds a new node to this registry.

:param node: Node instance to be added

:since: 1.0.0
        """

        if (not isinstance(node, Node)): raise ValueError("Node '{0!r}' given is invalid".format(node))

        with self:
            if (not self.is_node_known(node.id)): self._nodes[node.id] = node
        #
    #

    def add_or_update_node(self, node):
        """
Adds a node to or updates a node in this registry.

:param node: Node instance to be added / updated

:since: 1.0.0
        """

        if (not isinstance(node, Node)): raise ValueError("Node '{0!r}' given is invalid".format(node))
        self._nodes[node.id] = node
    #

    def get_node(self, node_id):
        """
Returns the node for the ID given.

:param node_id: homee node ID

:return: (object) Node instance
:since:  1.0.0
        """

        _return = None

        with self:
            if (self.is_node_known(node_id)): _return = self._nodes[node_id]
        #

        return _return
    #

    def get_node_id_for_name(self, node_name):
        """
Returns the node ID for the name given is registered.

:param node_name: homee node name

:return: (int) homee node ID
:since:  1.0.0
        """

        _return = None

        with self:
            for node_id in self._nodes:
                if (self._nodes[node_id].name == node_name):
                    _return = node_id
                    break
                #
            #
        #

        return _return
    #

    def is_node_known(self, node_id):
        """
Returns true if the node ID given is registered.

:param node_id: homee node ID

:return: (bool) True if known
:since:  1.0.0
        """

        return (node_id in self._nodes)
    #

    def update_node(self, node):
        """
Updates a node in this registry.

:param node: Node instance to be updated

:since: 1.0.0
        """

        if (not isinstance(node, Node)): raise ValueError("Node '{0!r}' given is invalid".format(node))

        with self:
            if (self.is_node_known(node.id)): self._nodes[node.id] = node
        #
    #

    def update_node_attribute(self, node_id, attribute_id, attribute_value):
        """
Updates a node attribute in this registry.

:param node_id: homee node ID
:param attribute_id: homee attribute ID
:param attribute_value: Attribute value

:since: 1.0.0
        """

        with self:
            if (self.is_node_known(node_id)):
                self._nodes[node_id]._update_attribute_value(attribute_id, attribute_value)
            #
        #
    #
#