# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

class SensorBinary(object):
    """
The "SensorBinary" properties mixin provides access to the current state.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    @property
    def is_sensor_active(self):
        """
Returns the true if the sensor state is set to active.

:return: (bool) True if active
:since:  1.0.0
        """

        return (self.attribute.value != 0)
    #
#
