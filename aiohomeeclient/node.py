# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

from urllib.parse import unquote
from weakref import proxy

from .attribute_property_interface import AttributePropertyInterface
from .attribute import ATTRIBUTES, Attribute
from .node_interfaces import *

class Node(object):
    """
The "Node" class provides methods for an homee node.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    def __init__(self, node_data, connection):
        """
Constructor __init__(Node)

:param node_data: Node data provided by homee
:param connection: homee connection instance

:since: 1.0.0
        """

        self._attributes = self._filter_attributes(node_data.get("attributes", [ ]))
        """
Sorted and filtered attributes of the node
        """
        self._connection = proxy(connection)
        """
homee connection instance
        """
        self._id = node_data['id']
        """
homee node ID
        """
        self._name = unquote(node_data.get("name", ""))
        """
Node name
        """
    #

    @property
    def id(self):
        """
Returns the homee node ID.

:return: (int) homee node ID
:since:  1.0.0
        """

        return self._id
    #

    @property
    def firmware_version(self):
        """
Returns the firmware version of the node (device) if provided.

:return: (str) Firmware version value
:since:  1.0.0
        """

        return self.get_attribute("FirmwareRevision")
    #

    @property
    def hardware_revision(self):
        """
Returns the hardware revision of the node (device) if provided.

:return: (str) Hardware revision value
:since:  1.0.0
        """

        return self.get_attribute("HardwareRevision")
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

    @property
    def name(self):
        """
Returns the node name.

:return: (str) Node name
:since:  1.0.0
        """

        return self._name
    #

    @property
    def serial_number(self):
        """
Returns the serial number of the node (device) if provided.

:return: (str) Serial number value
:since:  1.0.0
        """

        return self.get_attribute("SerialNumber")
    #

    @property
    def software_version(self):
        """
Returns the software version of the node (device) if provided.

:return: (str) Software version value
:since:  1.0.0
        """

        return self.get_attribute("SoftwareRevision")
    #

    def _filter_attributes(self, attributes):
        """
Returns sorted and filtered attribute instances for the node.

:param attributes: Attributes list of dictionaries

:return: (dict) Sorted and filtered attribute instances
:since:  1.0.0
        """

        _return = { }

        for attribute in attributes:
            if ("instance" not in attribute): attribute['instance'] = 0
            if (attribute['type'] not in _return): _return[attribute['type']] = [ ]

            position = 0

            for existing_attribute in _return[attribute['type']]:
                if (attribute['instance'] < existing_attribute['instance']): break
                position += 1
            #

            _return[attribute['type']].insert(position, Attribute(self, attribute))
        #

        return _return
    #

    def get_attribute(self, name, instance = 0):
        """
Returns the attribute for the given type name and instance.

:param name: Attribute type name
:param instance: Attribute instance

:return: (object) Attribute instance
:since:  1.0.0
        """

        if (instance > 0 and instance >= self.get_attribute_instances_count(name)):
            raise ValueError("Instance number '{0:d}' given for attribute '{1}' is invalid".format(instance, attribute))
        #

        return (None
                if (name is None or name not in ATTRIBUTES or ATTRIBUTES[name] not in self._attributes) else
                self._attributes[ATTRIBUTES[name]][instance]
               )
    #

    def get_attribute_instances_count(self, name):
        """
Returns the number of attribute instances for the given type name.

:param name: Attribute type name

:return: (int) Number of attribute instances
:since:  1.0.0
        """

        return len(self._attributes.get(ATTRIBUTES[name], [ ]))
    #

    def get_attribute_property_interface(self, name, instance = 0):
        """
Returns the attribute property interface instance for the given type name
and instance.

:param name: Attribute type name
:param instance: Attribute instance

:return: (object) Attribute property interface instance
:since:  1.0.0
        """

        attribute = self.get_attribute(name, instance)
        return AttributePropertyInterface.from_node(self, attribute)
    #

    def get_attribute_scale(self, name, instance = 0):
        """
Returns the attribute scale as a tuple of minimum, step and maximum value
for the given type name and instance.

:param name: Attribute type name
:param instance: Attribute instance

:return: (tuple) Attribute scale
:since:  1.0.0
        """

        attribute = self.get_attribute(name, instance)
        return (None if (attribute is None) else attribute.scale)
    #

    def get_attribute_step_value(self, name, instance = 0):
        """
Returns the attribute step value for the given type name and instance.

:param name: Attribute type name
:param instance: Attribute instance

:return: (mixed) Attribute step value
:since:  1.0.0
        """

        attribute = self.get_attribute(name, instance)
        return (None if (attribute is None) else attribute.step_value)
    #

    def get_attribute_unit(self, name, instance = 0):
        """
Returns the attribute measurement unit for the given type name and instance.

:param name: Attribute type name
:param instance: Attribute instance

:return: (str) Attribute unit
:since:  1.0.0
        """

        attribute = self.get_attribute(name, instance)
        return ("" if (attribute is None) else attribute.unit)
    #

    def get_attribute_value(self, name, instance = 0, default = None):
        """
Returns the attribute value for the given type name and instance.

:param name: Attribute type name
:param instance: Attribute instance
:param default: Default value if attribute is not defined

:return: (mixed) Attribute value
:since:  1.0.0
        """

        attribute = self.get_attribute(name, instance)
        return (default if (attribute is None) else attribute.value)
    #

    def is_interface_implemented(self, name):
        """
Returns true if the given interface name is implemented for this node
instance.

:param name: Interface name

:return: (bool) True if implemented
:since:  1.0.0
        """

        return (name in self._interfaces)
    #

    async def request_attribute_change(self, name, value, instance = 0):
        """
Requests the attribute value to change for the given type name and instance.

:param name: Attribute type name
:param value: Value to set
:param instance: Attribute instance

:since: 1.0.0
        """

        attribute = self.get_attribute(name, instance)

        if (attribute is None or (not attribute.is_editable)):
            raise ValueError("Attribute '{0}' instance '{1:d}' is not editable".format(name, instance))
        #

        await self._connection.send("PUT:/nodes/{0}/attributes/{1:d}?target_value={2}".format(self.id, attribute.id, value))
    #

    def _update_attribute_value(self, _id, value):
        """
Updates the attribute value for the given ID.

:param _id: homee attribute ID
:param value: Attribute value

:since: 1.0.0
        """

        is_attribute_found = False
        is_value_changed = False

        for attribute_type in self._attributes:
            for attribute in self._attributes[attribute_type]:
                if (attribute.id == _id):
                    is_attribute_found = True

                    if (attribute.value != value):
                        is_value_changed = True
                        attribute._set_value(value)
                    #

                    break
                #
            #

            if (is_attribute_found): break
        #

        if (is_attribute_found):
            if (is_value_changed):
                pass
            #
        #
    #

    @staticmethod
    def from_dict(node_data, connection):
        """
Returns a new "Node" instance for the node data given.

:param node_data: Node data provided by homee
:param connection: homee connection instance

:return: (object) Node instance
:since:  1.0.0
        """

        bases = [ Node ]

        interfaces = Mapper.get_interfaces_for_attributes_list(node_data.get("attributes"))

        if (interfaces & INTERFACE_BATTERY): bases.append(BatteryMixin)
        if (interfaces & INTERFACE_HOMEE_BRAIN): bases.append(HomeeBrainMixin)
        if (interfaces & INTERFACE_SENSOR_BINARY): bases.append(SensorBinaryMixin)
        if (interfaces & INTERFACE_SENSOR_MULTILEVEL): bases.append(SensorMultilevelMixin)
        if (interfaces & INTERFACE_SWITCH_BINARY): bases.append(SwitchBinaryMixin)
        #if (interfaces & INTERFACE_SWITCH_COLOR): bases.append(SwitchColorInterface)
        #if (interfaces & INTERFACE_SWITCH_MULTILEVEL): bases.append(SwitchMultilevelInterface)

        interfaces = set()

        for base in bases:
            interfaces.add(base.__name__)
        #

        dynamic_class = type(Node.__name__,
                             tuple(bases),
                             { "_interfaces": interfaces }
                            )

        return dynamic_class(node_data, connection)
    #
#
