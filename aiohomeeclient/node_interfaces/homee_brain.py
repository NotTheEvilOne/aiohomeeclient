# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

HOMEE_MODES = [ "Home",
                "Sleeping",
                "Away",
                "Vacation"
              ]

class HomeeBrain(object):
    """
The "HomeeBrain" node mixin provides access to Homee specific values.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    @property
    def homee_mode(self):
        """
Returns the current Homee mode.

:return: (str) Homee mode
:since:  1.0.0
        """

        homee_mode = self.get_attribute_value("HomeeMode")
        return (HOMEE_MODES[homee_mode] if (homee_mode in HOMEE_MODES) else None)
    #

    @property
    def sunrise_time(self):
        """
Returns the current UNIX timestamp for the next sunrise.

:return: (float) Sunrise UNIX timestamp
:since:  1.0.0
        """

        return self.get_attribute_value("SunriseTime")
    #

    @property
    def sunset_time(self):
        """
Returns the current UNIX timestamp for the next sunset.

:return: (float) Sunset UNIX timestamp
:since:  1.0.0
        """

        return self.get_attribute_value("SunsetTime")
    #
#
