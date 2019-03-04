# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

class SwitchBinary(object):
    """
The "SwitchBinary" properties mixin provides access to the switch state.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    @property
    def is_switch_on(self):
        """
Returns the true if the switch state is on.

:return: (bool) True if on
:since:  1.0.0
        """

        return (self.attribute.value != 0)
    #

    @property
    def switch_state(self):
        """
Returns the true if the switch state is on.

:return: (bool) True if on
:since:  1.0.0
        """

        return (self.attribute.value != 0)
    #

    @switch_state.setter
    def switch_state(self, state):
        """
Sets the switch state.

:param state: True to switch on

:since: 1.0.0
        """

        self._request_attribute_change(self.attribute.step_value if (state) else 0)
    #
#
