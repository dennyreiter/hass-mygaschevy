"""Support for MyChevy sensors."""
import logging

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.const import PERCENTAGE
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.util import slugify

from . import (
    DOMAIN as MYGASCHEVY_DOMAIN,
    ERROR_TOPIC,
    MYCHEVY_ERROR,
    MYCHEVY_SUCCESS,
    UPDATE_TOPIC,
    GVSensorConfig,
)

_LOGGER = logging.getLogger(__name__)


SENSORS = [
    GVSensorConfig("Mileage", "totalMiles", "miles", "mdi:speedometer"),
    GVSensorConfig("Gas Range", "gasRange", "miles", "mdi:speedometer"),
    GVSensorConfig("Fuel Economy", "fuelEconomy", "mpg"),
    GVSensorConfig("Fuel Percentage", "gasFuelLevelPercentage", "%", "mdi:gas-station"),
]


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the MyChevy sensors."""
    if discovery_info is None:
        return

    hub = hass.data[MYGASCHEVY_DOMAIN]
    sensors = [MyChevyStatus()]
    for sconfig in SENSORS:
        for car in hub.cars:
            sensors.append(GVSensor(hub, sconfig, car.vid))

    add_entities(sensors)


class MyChevyStatus(Entity):
    """A string representing the charge mode."""

    _name = "MyGasChevy Status"
    _icon = "mdi:car-info"

    def __init__(self):
        """Initialize sensor with car connection."""
        self._state = None

    async def async_added_to_hass(self):
        """Register callbacks."""
        self.async_on_remove(
            self.hass.helpers.dispatcher.async_dispatcher_connect(
                UPDATE_TOPIC, self.success
            )
        )

        self.async_on_remove(
            self.hass.helpers.dispatcher.async_dispatcher_connect(
                ERROR_TOPIC, self.error
            )
        )

    @callback
    def success(self):
        """Update state, trigger updates."""
        if self._state != MYCHEVY_SUCCESS:
            _LOGGER.debug("Successfully connected to mychevy website")
            self._state = MYCHEVY_SUCCESS
        self.async_write_ha_state()

    @callback
    def error(self):
        """Update state, trigger updates."""
        _LOGGER.error(
            "Connection to mychevy website failed. "
            "This probably means the mychevy to OnStar link is down"
        )
        self._state = MYCHEVY_ERROR
        self.async_write_ha_state()

    @property
    def icon(self):
        """Return the icon."""
        return self._icon

    @property
    def name(self):
        """Return the name."""
        return self._name

    @property
    def state(self):
        """Return the state."""
        return self._state

    @property
    def should_poll(self):
        """Return the polling state."""
        return False


class GVSensor(Entity):
    """Base GVSensor class.

    The only real difference between sensors is which units and what
    attribute from the car object they are returning. All logic can be
    built with just setting subclass attributes.
    """

    def __init__(self, connection, config, car_vid):
        """Initialize sensor with car connection."""
        self._conn = connection
        self._name = config.name
        self._attr = config.attr
        self._extra_attrs = config.extra_attrs
        self._unit_of_measurement = config.unit_of_measurement
        self._icon = config.icon
        self._state = None
        self._state_attributes = {}
        self._car_vid = car_vid

        self.entity_id = f"{SENSOR_DOMAIN}.{MYGASCHEVY_DOMAIN}_{slugify(self._car.name)}_{slugify(self._name)}"

    async def async_added_to_hass(self):
        """Register callbacks."""
        self.hass.helpers.dispatcher.async_dispatcher_connect(
            UPDATE_TOPIC, self.async_update_callback
        )

    @property
    def _car(self):
        """Return the car."""
        return self._conn.get_car(self._car_vid)

    @property
    def icon(self):
        """Return the icon."""
        return self._icon

    @property
    def name(self):
        """Return the name."""
        return self._name

    @callback
    def async_update_callback(self):
        """Update state."""
        if self._car is not None:
            self._state = getattr(self._car, self._attr, None)
            if self._unit_of_measurement == "miles" or self._unit_of_measurement == "mpg":
                self._state = round(self._state)
            for attr in self._extra_attrs:
                self._state_attributes[attr] = getattr(self._car, attr)
            self.async_write_ha_state()

    @property
    def state(self):
        """Return the state."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return all the state attributes."""
        return self._state_attributes

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement the state is expressed in."""
        return self._unit_of_measurement

    @property
    def should_poll(self):
        """Return the polling state."""
        return False
