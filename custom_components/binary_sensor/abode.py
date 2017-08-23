"""
This component provides HA binary_sensor support for Abode Security System.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.abode/
"""
import logging

from custom_components.abode import AbodeDevice, DATA_ABODE
from homeassistant.components.binary_sensor import BinarySensorDevice


DEPENDENCIES = ['abode']

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up a sensor for an Abode device."""
    abode = hass.data[DATA_ABODE]

    device_types = map_abode_device_class().keys()

    sensors = []
    for sensor in abode.get_devices(type_filter=device_types):
        sensors.append(AbodeBinarySensor(hass, abode, sensor))

    add_devices(sensors)


def map_abode_device_class():
    """Map Abode device types to Home Assistant binary sensor class."""
    import abodepy.helpers.constants as CONST

    return {
        CONST.DEVICE_GLASS_BREAK: 'connectivity',
        CONST.DEVICE_KEYPAD: 'connectivity',
        CONST.DEVICE_DOOR_CONTACT: 'opening',
        CONST.DEVICE_STATUS_DISPLAY: 'connectivity',
        CONST.DEVICE_MOTION_CAMERA: 'motion',
        CONST.DEVICE_WATER_SENSOR: 'moisture'
    }


class AbodeBinarySensor(AbodeDevice, BinarySensorDevice):
    """A binary sensor implementation for Abode device."""

    def __init__(self, hass, controller, device):
        """Initialize a sensor for Abode device."""
        AbodeDevice.__init__(self, hass, controller, device)
        self._device_class = map_abode_device_class().get(self._device.type)

    @property
    def is_on(self):
        """Return True if the binary sensor is on."""
        if self.device_class == 'motion':
            return self._device.get_value('motion_event') == '1'

        return self._device.is_on

    @property
    def device_class(self):
        """Return the class of the binary sensor."""
        return self._device_class
