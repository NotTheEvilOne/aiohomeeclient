# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

import asyncio

try: from types import new_class
except ImportError: new_class = None

from .attribute_property_interfaces import *

class AttributePropertyInterface(object):
    """
The "AttributePropertyInterface" class provides a properties based API for
a preselected node attribute.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    def __init__(self, node, attribute):
        """
Constructor __init__(AttributePropertyInterface)

:param node: Node instance of the attribute
:param attribute: Attribute instance

:since: 1.0.0
        """

        self.attribute = attribute
        self.node = node
    #

    def __getattr__(self, name):
        """
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Instance attribute
:since:  1.0.0
        """

        _return = None

        if (hasattr(self.attribute, name)): _return = getattr(self.attribute, name)
        elif (hasattr(self.node, name)): _return = getattr(self.node, name)
        else: _return = object.__getattribute__(self, name)

        return _return
    #

    @property
    def interfaces_implemented(self):
        """
Returns the interfaces implemented.

:return: (list) Interfaces implemented
:since:  1.0.0
        """

        return self._interfaces
    #

    def is_interface_implemented(self, name):
        """
Returns true if the given interface name is implemented for this attribute
property interface instance.

:param name: Interface name

:return: (bool) True if implemented
:since:  1.0.0
        """

        return (name in self._interfaces)
    #

    def _request_attribute_change(self, value):
        """
Requests the attribute value to change.

:param value: Value to set

:since: 1.0.0
        """

        asyncio.run_coroutine_threadsafe(self.node.request_attribute_change(self.attribute.name, value, self.attribute.instance),
                                         asyncio.get_event_loop()
                                        )
    #

    @staticmethod
    def from_node(node, attribute):
        """
Returns a new "AttributePropertyInterface" instance for the attribute given.

:param node: Node instance of the attribute
:param attribute: Attribute instance

:return: (object) AttributePropertyInterface instance
:since:  1.0.0
        """

        bases = [ AttributePropertyInterface ]

        interfaces = node.interfaces_implemented

        if ("Battery" in interfaces): bases.append(BatteryMixin)
        if ("SensorBinary" in interfaces): bases.append(SensorBinaryMixin)
        if ("SwitchBinary" in interfaces): bases.append(SwitchBinaryMixin)

        interfaces = set()

        for base in bases:
            interfaces.add(base.__name__)
        #

        dynamic_class = new_class(AttributePropertyInterface.__name__, tuple(bases), { "_interfaces": interfaces })
        return dynamic_class(node, attribute)
    #
#
