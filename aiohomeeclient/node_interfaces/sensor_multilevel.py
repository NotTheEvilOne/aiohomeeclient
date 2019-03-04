# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

from numbers import Number

from .abstract_sensor import AbstractSensor

class SensorMultilevel(AbstractSensor):
    """
The "SensorMultilevel" node mixin provides access to sensor values.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    def get_sensor_value(self, _type, instance = -1):
        """
Returns the current value of the given sensor instance.

:param _type: Sensor type name
:param instance: Sensor instance

:return: (mixed) Sensor value; None if not defined
:since:  1.0.0
        """

        if (not self._is_sensor_supported(_type)): _type = self._get_alternative_sensor_type(_type)

        _return = None

        if (_type is not None):
            if (instance < 0):
                instances_count = self.get_attribute_instances_count(_type)
                _return = 0

                for instance in range(0, instances_count):
                    instance_value = self.get_attribute_value(_type, instance, 0)

                    if (not isinstance(instance_value, Number)): raise TypeError("Can't aggregate non-numeric sensor values")
                    _return += instance_value
                #

                if (instances_count > 1): _return /= instances_count
            else: _return = self.get_attribute_value("BatteryLevel", instance, 0)
        #

        return _return
    #
#
