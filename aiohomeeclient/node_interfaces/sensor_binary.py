# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

from .abstract_sensor import AbstractSensor

class SensorBinary(AbstractSensor):
    """
The "SensorBinary" node mixin provides access to binary sensor states.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    def is_sensor_active(self, _type, instance = -1):
        """
Returns the true if any sensor state or the given instance one is set to
active.

:param instance: Sensor instance

:return: (bool) True if active
:since:  1.0.0
        """

        _return = False

        if (not self._is_sensor_supported(_type)): _type = self._get_alternative_sensor_type(_type)

        if (_type is not None):
            if (instance < 0):
                instances_count = self.get_attribute_instances_count(_type)

                for instance in range(0, instances_count):
                    if (self.get_attribute_value(_type, instance, 0) != 0):
                        _return = True
                        break
                    #
                #
            else: _return = (self.get_attribute_value(_type, instance, 0) != 0)
        #

        return _return
    #
#
