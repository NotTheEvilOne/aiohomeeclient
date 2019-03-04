# -*- coding: utf-8 -*-

"""
(C) Tobias Wolf et al. - All rights reserved

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
"""

from urllib.parse import unquote
import asyncio

try: from collections.abc import Mapping
except ImportError: from collections import Mapping

ATTRIBUTES_TYPE_DICT = [ "None",
                         "OnOff",
                         "DimmingLevel",
                         "CurrentEnergyUse",
                         "AccumulatedEnergyUse",
                         "Temperature",
                         "TargetTemperature",
                         "RelativeHumidity",
                         "BatteryLevel",
                         "StatusLED",
                         "WindowPosition",
                         "Brightness",
                         "FloodAlarm",
                         "Siren",
                         "OpenClose",
                         "Position",
                         "SmokeAlarm",
                         "BlackoutAlarm",
                         "CurrentValvePosition",
                         "BinaryInput",
                         "CO2Level",
                         "Pressure",
                         "Level",
                         "Color",
                         "Saturation",
                         "MotionAlarm",
                         "MotionSensitivity",
                         "MotionInsensitivity",
                         "MotionAlarmCancelationDelay",
                         "WakeUpInterval",
                         "TamperAlarm",
                         "31",
                         "32",
                         "LinkQuality",
                         "InovaAlarmSystemState",
                         "InovaAlarmGroupState",
                         "InovaAlarmIntrusionState",
                         "InovaAlarmErrorState",
                         "InovaAlarmDoorState",
                         "InovaAlarmExternalSensor",
                         "ButtonState",
                         "Hue",
                         "ColorTemperature",
                         "HardwareRevision",
                         "FirmwareRevision",
                         "SoftwareRevision",
                         "LEDState",
                         "LEDStateWhenOn",
                         "LEDStateWhenOff",
                         "49",
                         "50",
                         "51",
                         "HighTemperatureAlarm",
                         "HighTemperatureAlarmTreshold",
                         "LowTemperatureAlarm",
                         "LowTemperatureAlarmTreshold",
                         "TamperSensitivity",
                         "TamperAlarmCancelationDelay",
                         "BrightnessReportInterval",
                         "TemperatureReportInterval",
                         "MotionAlarmIndicationMode",
                         "LEDBrightness",
                         "TamperAlarmIndicationMode",
                         "SwitchType",
                         "TemperatureOffset",
                         "AccumulatedWaterUse",
                         "AccumulatedWaterUseLastMonth",
                         "CurrentDate",
                         "LeakAlarm",
                         "BatteryLowAlarm",
                         "MalfunctionAlarm",
                         "LinkQualityAlarm",
                         "Mode",
                         "73",
                         "74",
                         "Calibration",
                         "PresenceAlarm",
                         "MinimumAlarm",
                         "MaximumAlarm",
                         "OilAlarm",
                         "WaterAlarm",
                         "InovaAlarmInhibition",
                         "InovaAlarmEjection",
                         "InovaAlarmCommercialRef",
                         "SerialNumber",
                         "RadiatorThermostatSummerMode",
                         "InovaAlarmOperationMode",
                         "AutomaticMode",
                         "PollingInterval",
                         "FeedTemperature",
                         "DisplayOrientation",
                         "ManualOperation",
                         "DeviceTemperature",
                         "Sonometer",
                         "AirPressure",
                         "OutdoorRelativeHumidity",
                         "IndoorRelativeHumidity",
                         "OutdoorTemperature",
                         "IndoorTemperature",
                         "VentilationLevel",
                         "VentilationMode",
                         "RainFall",
                         "IntakeMotorRevs",
                         "ExhaustMotorRevs",
                         "OperatingHours",
                         "InovaAlarmSilentAlert",
                         "InovaAlarmPreAlarm",
                         "InovaAlarmDeterrenceAlarm",
                         "InovaAlarmWarning",
                         "InovaAlarmFireAlarm",
                         "UpTime",
                         "DownTime",
                         "ShutterBlindMode",
                         "ShutterSlatPosition",
                         "ShutterSlatTime",
                         "RestartDevice",
                         "SoilMoisture",
                         "WaterPlantAlarm",
                         "MistPlantAlarm",
                         "FertilizePlantAlarm",
                         "CoolPlantAlarm",
                         "HeatPlantAlarm",
                         "PutPlantIntoLightAlarm",
                         "PutPlantIntoShadeAlarm",
                         "ColorMode",
                         "TargetTemperatureLow",
                         "TargetTemperatureHigh",
                         "HVACMode",
                         "Away",
                         "HVACState",
                         "HasLeaf",
                         "SetEnergyConsumption",
                         "COAlarm",
                         "RestoreLastKnownState",
                         "LastImageReceived",
                         "UpDown",
                         "RequestVOD",
                         "InovaDetectorHistory",
                         "SurgeAlarm",
                         "LoadAlarm",
                         "OverloadAlarm",
                         "VoltageDropAlarm",
                         "ShutterOrientation",
                         "OverCurrentAlarm",
                         "SirenMode",
                         "AlarmAutoStopTime",
                         "WindSpeed",
                         "WindDirection",
                         "ComfortTemperature",
                         "EcoTemperature",
                         "ReduceTemperature",
                         "ProtectTemperature",
                         "InovaSystemTime",
                         "InovaCorrespondentProtocol",
                         "InovaCorrespondentID",
                         "InovaCorrespondentListen",
                         "InovaCorrespondentNumber",
                         "InovaCallCycleFireProtection",
                         "InovaCallCycleIntrusion",
                         "InovaCallCycleTechnicalProtect",
                         "InovaCallCycleFaults",
                         "InovaCallCycleDeterrence",
                         "InovaCallCyclePrealarm",
                         "InovaPSTNRings",
                         "InovaDoubleCallRings",
                         "InovaPIN",
                         "InovaPUK",
                         "InovaMainMediaSelection",
                         "RainFallLastHour",
                         "RainFallToday",
                         "IdentificationMode",
                         "ButtonDoubleClick",
                         "SirenTriggerMode",
                         "UV",
                         "SlatSteps",
                         "EcoModeConfig",
                         "ButtonLongRelease",
                         "VisualGong",
                         "AcousticGong",
                         "SurveillanceOnOff",
                         "180",
                         "StorageAlarm",
                         "PowerSupplyAlarm",
                         "NetatmoHome",
                         "NetatmoPerson",
                         "NetatmoLastEventPersonId",
                         "NetatmoLastEventTime",
                         "NetatmoLastEventType",
                         "NetatmoLastEventIsKnownPerson",
                         "NetatmoLastEventIsArrival",
                         "PresenceTimeout",
                         "KnownPersonPresence",
                         "UnknownPersonPresence",
                         "Current",
                         "Frequency",
                         "Voltage",
                         "PresenceAlarmCancelationDelay",
                         "PresenceAlarmDetectionDelay",
                         "PresenceAlarmThreshold",
                         "NetatmoThermostatMode",
                         "NetatmoRelayBoilerConnected",
                         "NetatmoRelayMac",
                         "NetatmoThermostatModeTimeout",
                         "NetatmoThermostatNextChange",
                         "NetatmoThermostatPrograms",
                         "HomeeMode",
                         "ColorWhite",
                         "MovementAlarm",
                         "MovementSensitivity",
                         "VibrationAlarm",
                         "VibrationSensitivity",
                         "AverageEnergyUse",
                         "BinaryInputMode",
                         "DeviceStatus",
                         "DeviceRemainingTime",
                         "DeviceStartTime",
                         "DeviceProgram",
                         "217",
                         "218",
                         "219",
                         "220",
                         "221",
                         "222",
                         "ButtonPressed3Times",
                         "ButtonPressed4Times",
                         "ButtonPressed5Times",
                         "RepeaterMode",
                         "AutoOffTime",
                         "CO2Alarm",
                         "InputEndpointConfiguration",
                         "GustSpeed",
                         "GustDirection",
                         "LockState",
                         "AeotecSmartPlugLEDState",
                         "AlarmDuration",
                         "DewPoint",
                         "Gesture",
                         "GestureSequenceLearningMode",
                         "GestureSequence",
                         "TotalCurrentEnergyUse",
                         "TotalAccumulatedEnergyUse",
                         "SunsetTime",
                         "SunriseTime",
                         "CurrentLocalWeatherCondition",
                         "CurrentLocalTemperature",
                         "CurrentLocalHumidity",
                         "ForecastLocalWeatherCondition",
                         "ForecastLocalTempMin",
                         "ForecastLocalTempMax",
                         "Armed",
                         "Floodlight",
                         "HumanDetected",
                         "VehicleDetected",
                         "AnimalDetected",
                         "VacationMode",
                         "BlinkInterval",
                         "OtherMotionDetected",
                         "IRCodeNumber",
                         "HeatingMode",
                         "DisplayAutoOffTime",
                         "Backlight",
                         "OpenWindowDetectionSensibility",
                         "CurrentLocalWindSpeed",
                         "CurrentLocalGustSpeed",
                         "PowerOutputGrid",
                         "PowerInputGrid",
                         "PowerPV",
                         "PowerLoad",
                         "PowerOutputBattery",
                         "PowerInputBattery",
                         "RelativeAutonomy",
                         "RelativeSelfConsumption",
                         "TotalCurrent",
                         "EnergyStorageLevel",
                         "TotalEnergyLoad",
                         "TotalEnergyProduction",
                         "TotalEnergyOutputGrid",
                         "TotalEnergyInputGrid",
                         "TotalEnergyStored",
                         "TotalEnergyRestored",
                         "280",
                         "281",
                         "282",
                         "283",
                         "284",
                         "285",
                         "286",
                         "287",
                         "288",
                         "ReplaceFilterAlarm"
                       ]
"""
Attribute type names list
"""
ATTRIBUTES = { key: index for key, index in zip(ATTRIBUTES_TYPE_DICT, range(0, len(ATTRIBUTES_TYPE_DICT))) }
"""
Map of attribute type names and corresponding homee IDs
"""

class Attribute(Mapping):
    """
The "Attribute" class provides access to node attribute properties.

:author:     Tobias Wolf et al.
:copyright:  Tobias Wolf et al. - All rights reserved
:package:    aiohomee
:subpackage: client
:since:      1.0.0
:license:    Mozilla Public License, v. 2.0
    """

    def __init__(self, node, attribute_dict):
        """
Constructor __init__(Attribute)

:param node: Node instance of the attribute
:param attribute_dict: Attribute dictionary

:since: 1.0.0
        """

        if (type(attribute_dict.get("data")) is str): attribute_dict['data'] = unquote(attribute_dict['data'])
        if (type(attribute_dict.get("name")) is str): attribute_dict['name'] = unquote(attribute_dict['name'])
        if (type(attribute_dict.get("unit")) is str): attribute_dict['unit'] = unquote(attribute_dict['unit'])

        self._data = attribute_dict
        self._node = node
    #

    def __iter__(self):
        """
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  1.0.0
        """

        return iter(self._data)
    #

    def __getitem__(self, key):
        """
python.org: Called to implement evaluation of self[key].

:param key: Key

:return: (mixed) Value
:since:  1.0.0
        """

        return self._data[key]
    #

    def __len__(self):
        """
python.org: Called to implement the built-in function len().

:return: (int) Number of attribute items
:since:  1.0.0
        """

        return len(self._data)
    #

    def __repr__(self):
        """
python.org: Called by the repr() built-in function and by string conversions
(reverse quotes) to compute the "official" string representation of an
object.

:return: (str) String representation
:since:  1.0.0
        """

        return repr(self._data)
    #

    @property
    def id(self):
        """
Returns the homee attribute ID.

:return: (int) homee attribute ID
:since:  1.0.0
        """

        return self._data.get("id")
    #

    @property
    def instance(self):
        """
Returns the homee attribute instance.

:return: (int) homee attribute instance
:since:  1.0.0
        """

        return self._data.get("instance")
    #

    @property
    def is_editable(self):
        """
Returns true if the attribute is editable.

:return: (bool) True if editable
:since:  1.0.0
        """

        return bool(self._data.get("editable", 0))
    #

    @property
    def max(self):
        """
Returns the maximum value allowed.

:return: (mixed) Maximum value allowed
:since:  1.0.0
        """

        return self._data.get("max")
    #

    @property
    def min(self):
        """
Returns the minimum value allowed.

:return: (mixed) Minimum value allowed
:since:  1.0.0
        """

        return self._data.get("min")
    #

    @property
    def name(self):
        """
Returns the attribute name.

:return: (str) Attribute name
:since:  1.0.0
        """

        return ATTRIBUTES_TYPE_DICT[self._data['type']]
    #

    @property
    def node_id(self):
        """
Returns the homee node ID.

:return: (int) homee node ID
:since:  1.0.0
        """

        return self._data.get("node_id")
    #

    @property
    def scale(self):
        """
Returns the attribute scale as a tuple of minimum, step and maximum value.

:return: (tuple) Attribute scale
:since:  1.0.0
        """

        return ( self._data.get("min"), self._data.get("step_value"), self._data.get("max") )
    #

    @property
    def step_value(self):
        """
Returns the attribute step value.

:return: (mixed) Attribute step value
:since:  1.0.0
        """

        return self._data.get("step_value")
    #

    @property
    def unit(self):
        """
Returns the attribute measurement unit.

:return: (str) Attribute unit
:since:  1.0.0
        """

        return self._data.get("unit")
    #

    @property
    def value(self):
        """
Returns the attribute value.

:return: (mixed) Attribute value
:since:  1.0.0
        """

        return self._data.get("current_value")
    #

    @value.setter
    def value(self, value):
        """
Sets the attribute value.

:param value: Attribute value to set

:since: 1.0.0
        """

        if (self.is_editable and self.value != value):
            asyncio.run_coroutine_threadsafe(self._node.request_attribute_change(self.name, value, self.instance),
                                             asyncio.get_event_loop()
                                            )
        #
    #

    def _set_value(self, value):
        """
Sets the attribute value(s).

:param value: Attribute value(s) to set

:since: 1.0.0
        """

        if (type(value) is dict):
            for key in value:
                if (self._data[key] != value[key]): self._data[key] = value[key]
            #
        else: self._data['current_value'] = value
    #
#
