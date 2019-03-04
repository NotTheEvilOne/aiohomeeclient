# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

class Battery(object):
    """
The "Battery" properties mixin provides access to the current charge level.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    @property
    def battery_level(self):
        """
Returns the current charge level.

:return: (float) Charge level
:since:  1.0.0
        """

        return self.attribute.value
    #
#
