#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils import find_packages, setup
#

setup(name = "aiohomeeclient",
      version = "1.0.0",
      description = "Asyncio homee API Client",
      url = "https://github.com/NotTheEvilOne/aiohomeeclient",
      author = "Tobias Wolf et al.",
      license = "MPL2",

      platforms = [ "any" ],

      packages = find_packages()
     )
