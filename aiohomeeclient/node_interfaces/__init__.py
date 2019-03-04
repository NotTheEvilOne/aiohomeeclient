# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

try: from collections.abc import Mapping, Sequence
except ImportError: from collections import Mapping, Sequence

from ..attribute import ATTRIBUTES

from .battery import Battery as BatteryMixin
from .homee_brain import HomeeBrain as HomeeBrainMixin
from .homee_brain import HOMEE_MODES
from .sensor_binary import SensorBinary as SensorBinaryMixin
from .sensor_multilevel import SensorMultilevel as SensorMultilevelMixin
from .switch_binary import SwitchBinary as SwitchBinaryMixin

INTERFACE_BATTERY = 1
INTERFACE_BATTERY_MAP = [ ATTRIBUTES['BatteryLevel'] ]

INTERFACE_CLOCK = 1 << 2
INTERFACE_CLOCK_MAP = [ ATTRIBUTES['CurrentDate'] ]

INTERFACE_HOMEE_BRAIN = 1 << 3
INTERFACE_HOMEE_BRAIN_MAP = [ ATTRIBUTES['HomeeMode'] ]

INTERFACE_SWITCH_BINARY = 1 << 4
INTERFACE_SWITCH_BINARY_MAP = [ ATTRIBUTES['OnOff'] ]

INTERFACE_SWITCH_COLOR = 1 << 5
INTERFACE_SWITCH_COLOR_MAP = [ ATTRIBUTES['Color'] ]

INTERFACE_SWITCH_MULTILEVEL = 1 << 6
INTERFACE_SWITCH_MULTILEVEL_MAP = [ ATTRIBUTES['DimmingLevel'] ]

INTERFACE_SENSOR_BINARY = 1 << 7

INTERFACE_SENSOR_BINARY_MAP = [ ATTRIBUTES['BinaryInput'],
                                ATTRIBUTES['OpenClose'],
                              ]

INTERFACE_SENSOR_MULTILEVEL = 1 << 8

INTERFACE_SENSOR_MULTILEVEL_MAP = [ ATTRIBUTES['AirPressure'],
                                    ATTRIBUTES['AccumulatedEnergyUse'],
                                    ATTRIBUTES['AverageEnergyUse'],
                                    ATTRIBUTES['BatteryLevel'],
                                    ATTRIBUTES['Brightness'],
                                    ATTRIBUTES['CO2Level'],
                                    ATTRIBUTES['Current'],
                                    ATTRIBUTES['CurrentEnergyUse'],
                                    ATTRIBUTES['CurrentLocalGustSpeed'],
                                    ATTRIBUTES['CurrentLocalHumidity'],
                                    ATTRIBUTES['CurrentLocalTemperature'],
                                    ATTRIBUTES['CurrentLocalWeatherCondition'],
                                    ATTRIBUTES['CurrentLocalWindSpeed'],
                                    ATTRIBUTES['CurrentValvePosition'],
                                    ATTRIBUTES['DeviceTemperature'],
                                    ATTRIBUTES['DewPoint'],
                                    ATTRIBUTES['EnergyStorageLevel'],
                                    ATTRIBUTES['FeedTemperature'],
                                    ATTRIBUTES['ForecastLocalTempMax'],
                                    ATTRIBUTES['ForecastLocalTempMin'],
                                    ATTRIBUTES['ForecastLocalWeatherCondition'],
                                    ATTRIBUTES['Frequency'],
                                    ATTRIBUTES['GustDirection'],
                                    ATTRIBUTES['GustSpeed'],
                                    ATTRIBUTES['IndoorRelativeHumidity'],
                                    ATTRIBUTES['IndoorTemperature'],
                                    ATTRIBUTES['OutdoorRelativeHumidity'],
                                    ATTRIBUTES['OutdoorTemperature'],
                                    ATTRIBUTES['Position'],
                                    ATTRIBUTES['PowerInputBattery'],
                                    ATTRIBUTES['PowerInputGrid'],
                                    ATTRIBUTES['PowerLoad'],
                                    ATTRIBUTES['PowerOutputBattery'],
                                    ATTRIBUTES['PowerOutputGrid'],
                                    ATTRIBUTES['PowerPV'],
                                    ATTRIBUTES['Pressure'],
                                    ATTRIBUTES['RainFall'],
                                    ATTRIBUTES['RainFallLastHour'],
                                    ATTRIBUTES['RainFallToday'],
                                    ATTRIBUTES['RelativeAutonomy'],
                                    ATTRIBUTES['RelativeHumidity'],
                                    ATTRIBUTES['RelativeSelfConsumption'],
                                    ATTRIBUTES['SetEnergyConsumption'],
                                    ATTRIBUTES['SoilMoisture'],
                                    ATTRIBUTES['Sonometer'],
                                    ATTRIBUTES['Temperature'],
                                    ATTRIBUTES['TotalAccumulatedEnergyUse'],
                                    ATTRIBUTES['TotalCurrent'],
                                    ATTRIBUTES['TotalCurrentEnergyUse'],
                                    ATTRIBUTES['TotalEnergyInputGrid'],
                                    ATTRIBUTES['TotalEnergyLoad'],
                                    ATTRIBUTES['TotalEnergyProduction'],
                                    ATTRIBUTES['TotalEnergyRestored'],
                                    ATTRIBUTES['TotalEnergyStored'],
                                    ATTRIBUTES['TotalEnergyOutputGrid'],
                                    ATTRIBUTES['UV'],
                                    ATTRIBUTES['Voltage'],
                                    ATTRIBUTES['WindDirection'],
                                    ATTRIBUTES['WindowPosition'],
                                    ATTRIBUTES['WindSpeed']
                                  ]

class Mapper(object):
    @staticmethod
    def get_interfaces_for_attributes_list(attributes):
        if (not isinstance(attributes, Sequence)): attributes = [ ]

        _return = 0

        for attribute in attributes:
            if (not isinstance(attribute, Mapping)): continue

            type_id = attribute.get("type", 0)

            if (type_id in INTERFACE_BATTERY_MAP): _return |= INTERFACE_BATTERY
            if (type_id in INTERFACE_CLOCK_MAP): _return |= INTERFACE_CLOCK
            if (type_id in INTERFACE_HOMEE_BRAIN_MAP): _return |= INTERFACE_HOMEE_BRAIN
            if (type_id in INTERFACE_SENSOR_BINARY_MAP): _return |= INTERFACE_SENSOR_BINARY
            if (type_id in INTERFACE_SENSOR_MULTILEVEL_MAP): _return |= INTERFACE_SENSOR_MULTILEVEL
            if (type_id in INTERFACE_SWITCH_BINARY_MAP): _return |= INTERFACE_SWITCH_BINARY
            if (type_id in INTERFACE_SWITCH_COLOR_MAP): _return |= INTERFACE_SWITCH_COLOR
            if (type_id in INTERFACE_SWITCH_MULTILEVEL_MAP): _return |= INTERFACE_SWITCH_MULTILEVEL
        #

        return _return
    #

    def get_attribute_type_id(value):
        return ATTRIBUTES[value]
    #
#
