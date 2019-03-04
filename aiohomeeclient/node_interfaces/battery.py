# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

from ..attribute import ATTRIBUTES

class Battery(object):
    """
The "Battery" node mixin provides access to batteries.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    def get_battery_level(self, instance = -1):
        """
Returns the current charge level.

:param instance: Battery instance

:return: (float) Charge level
:since:  1.0.0
        """

        _return = 0

        if (instance < 0):
            instances_count = self.get_attribute_instances_count("BatteryLevel")

            for instance in range(0, instances_count):
                _return += self.get_attribute_value("BatteryLevel", instance, 0)
            #

            if (instances_count > 1): _return /= instances_count
        else: _return = self.get_attribute_value("BatteryLevel", instance, 0)

        return _return
    #
#
