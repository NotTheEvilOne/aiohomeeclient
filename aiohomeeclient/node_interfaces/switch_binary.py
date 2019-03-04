# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

class SwitchBinary(object):
    """
The "SensorMultilevel" node mixin provides access to sensor values.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    def get_switch_state(self, _type, instance = -1):
        """
Returns the true if the switch state is on.

:param _type: Switch type name
:param instance: Switch instance

:return: (bool) True if on
:since:  1.0.0
        """

        _return = False

        if (instance < 0):
            instances_count = self.get_attribute_instances_count(_type)

            for instance in range(0, instances_count):
                if (self.get_attribute_value(_type, instance, 0) != 0):
                    _return = True
                    break
                #
            #
        else: _return = (self.get_attribute_value(_type, instance, 0) != 0)

        return _return
    #

    def set_switch_state(self, _type, state, instance = 0):
        """
Sets the switch state.

:param _type: Switch type name
:param state: True to switch on
:param instance: Switch instance

:since: 1.0.0
        """

        self.request_attribute_change(_type, (self.attribute.step_value if (state) else 0), instance)
    #
#
