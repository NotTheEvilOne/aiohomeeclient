# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

from ..attribute import ATTRIBUTES

ALTERNATIVE_MAP = { "GustSpeed": [ "CurrentLocalGustSpeed" ],
                    "RelativeHumidity": [ "IndoorRelativeHumidity", "OutdoorRelativeHumidity", "CurrentLocalHumidity" ],
                    "Temperature": [ "DeviceTemperature",
                                     "FeedTemperature",
                                     "IndoorTemperature",
                                     "OutdoorTemperature",
                                     "CurrentLocalTemperature"
                                   ],
                    "WindSpeed": [ "CurrentLocalWindSpeed" ],
                  }
"""
Map of alternative sensor names
"""

class AbstractSensor(object):
    """
The "AbstractSensor" node mixin provides common methods for sensor
implementations.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    def _get_alternative_sensor_type(self, _type):
        """
Returns the alternative sensor type name supported and implemented for the
given one.

:param _type: Sensor type name

:return: (str) Alternative sensor type name implemented; None otherwise
:since:  1.0.0
        """

        if (not self._is_sensor_supported(_type)):
            alternative_type = None

            for alternative_type_candidate in ALTERNATIVE_MAP.get(_type, ( )):
                if (self._is_sensor_supported(alternative_type_candidate)):
                    alternative_type = alternative_type_candidate
                    break
                #
            #

            _type = alternative_type
        #

        return _type
    #

    def get_sensor_count(self, _type):
        """
Returns the number of sensor instances of the given type.

:param _type: Sensor type name

:return: (int) Number of sensor instances
:since:  1.0.0
        """

        if (not self._is_sensor_supported(_type)): _type = self._get_alternative_sensor_type(_type)
        return (0 if (_type is None) else self.get_attribute_instances_count(_type))
    #

    def get_sensor_unit(self, _type, instance = 0):
        """
Returns the unit of the given sensor instance.

:param _type: Sensor type name
:param instance: Sensor instance

:return: (str) Sensor unit; None if not defined
:since:  1.0.0
        """

        if (not self._is_sensor_supported(_type)): _type = self._get_alternative_sensor_type(_type)
        return (None if (_type is None) else self.get_attribute_unit(_type, instance))
    #

    def get_sensor_value(self, _type, instance = 0):
        """
Returns the current value of the given sensor instance.

:param _type: Sensor type name
:param instance: Sensor instance

:return: (mixed) Sensor value; None if not defined
:since:  1.0.0
        """

        if (not self._is_sensor_supported(_type)): _type = self._get_alternative_sensor_type(_type)
        return self.get_attribute_value(_type, instance)
    #

    def is_sensor_editable(self, _type, instance = 0):
        """
Returns true if the sensor instance is editable.

:param _type: Sensor type name
:param instance: Sensor instance

:return: (bool) True if editable
:since:  1.0.0
        """

        if (not self._is_sensor_supported(_type)): _type = self._get_alternative_sensor_type(_type)
        return (False if (_type is None) else self.get_attribute(_type, instance).is_editable)
    #

    def is_sensor_supported(self, _type):
        """
Returns true if the given sensor type or an alternative one is implemented.

:param _type: Sensor type name

:return: (bool) True if implemented
:since:  1.0.0
        """

        if (not self._is_sensor_supported(_type)): _type = self._get_alternative_sensor_type(_type)
        return (_type is not None)
    #

    def _is_sensor_supported(self, _type):
        """
Returns true if the given sensor type is implemented.

:param _type: Sensor type name

:return: (bool) True if implemented
:since:  1.0.0
        """

        return (_type in ATTRIBUTES and ATTRIBUTES[_type] in self._attributes)
    #
#
