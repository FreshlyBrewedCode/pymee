"""Data model for Homees various data items."""

from collections.abc import Callable
import logging
from urllib.parse import unquote

_LOGGER = logging.getLogger(__name__)


class HomeeAttributeOptions:
    """Representation of attributes options."""

    def __init__(self, attribute_options):
        """Initialize options."""
        self._data = attribute_options

    @property
    def can_observe(self) -> list:
        """List (int) of attribute types that this attribute can observe."""
        if "can_observe" in self._data:
            return self._data["can_observe"]

        return []

    @property
    def observes(self) -> list:
        """List (int) of attribute ids that this attribute observes."""
        if "observes" in self._data:
            return self._data["observes"]

        return []

    @property
    def observed_by(self) -> list:
        """List (int) of attribute ids that observe this attribute."""
        if "observed_by" in self._data:
            return self._data["observed_by"]

        return []

    @property
    def automations(self) -> list:
        """List (str) of automations for thie attribute."""
        if "automations" in self._data:
            return self._data["automations"]

        return []

    @property
    def history(self) -> list[dict]:
        """History data for the attribute.

        {'day': int, 'week': int, 'month': int, 'stepped': bool}.
        """
        if "history" in self._data:
            return self._data["history"]

        return {}

    @property
    def reverse_control_ui(self) -> bool:
        """Do up/down controls work in opposite direction."""
        if "reverse_control_ui" in self._data:
            return self._data["reverse_control_ui"]

        return False


class HomeeAttribute:
    """Representation of a Homee attribute."""

    def __init__(self, data: dict) -> None:
        """Initialize the attribute."""
        self._data = data

    @property
    def raw_data(self):
        """Return the raw JSON data of the Attribute."""
        return self._data

    @property
    def id(self) -> int:
        """The unique id of the attribute."""
        return self._data["id"]

    @property
    def node_id(self) -> int:
        """The id of the node the attribute belongs to."""
        return self._data["node_id"]

    @property
    def instance(self) -> int:
        """If more than one attribute of same type is present, they are numbered starting at 1."""
        return self._data["instance"]

    @property
    def minimum(self) -> int:
        """The minimum possible value of the attribute."""
        return self._data["minimum"]

    @property
    def maximum(self) -> int:
        """The maximum possible value of the attribute."""
        return self._data["maximum"]

    @property
    def current_value(self) -> int:
        """The current value of the attribute."""
        return self._data["current_value"]

    @property
    def target_value(self) -> int:
        """The target value of the attribute.

        Only used to change the attribute value.
        In most cases you want to use current_value instead.
        """
        return self._data["target_value"]

    @property
    def last_value(self) -> int:
        """The last value of the attribute. In most cases you want to use current_value instead."""
        return self._data["last_value"]

    @property
    def unit(self) -> str:
        """The decoded unit of the attribute."""
        return unquote(self._data["unit"])

    @property
    def step_value(self) -> int:
        """The step value used for attributes with discret increments."""
        return self._data["step_value"]

    @property
    def editable(self) -> bool:
        """Wether the attribute is editable of read only."""
        return bool(self._data["editable"])

    @property
    def type(self) -> int:
        """The attribute type. Compare with const.AttributeType."""
        return self._data["type"]

    @property
    def state(self) -> int:
        """The attribute state. Compare with const.AttributeState."""
        return self._data["state"]

    @property
    def last_changed(self) -> int:
        """The last time the attribute was changed."""
        return self._data["last_changed"]

    @property
    def changed_by(self) -> int:
        """How the attribute was changed. Compare with const.AttributeChangedBy."""
        return self._data["changed_by"]

    @property
    def changed_by_id(self) -> int:
        """The id of the user/homeegram the attribute was changed by."""
        return self._data["changed_by_id"]

    @property
    def based_on(self) -> int:
        """TODO"""
        return self._data["based_on"]

    @property
    def name(self) -> str:
        """The decoded name of the attribute."""
        return unquote(self._data["name"])

    @property
    def data(self) -> str:
        """The data string of the attribute. Note that the data may be uri encoded."""
        return self._data["data"]

    @property
    def options(self) -> HomeeAttributeOptions:
        """The options collection of the attribute. Optional, not on every attribute."""
        if "options" in self._data:
            return HomeeAttributeOptions(self._data["options"])

        return []

    def set_data(self, data: str):
        """Update data of the attribute."""
        self._data = data


class HomeeNode:
    """Representation of a node in Homee."""

    def __init__(self, data: dict) -> None:
        """Initialize a Homee node."""
        self._data = data
        self.attributes: list[HomeeAttribute] = []
        for a in self.attributes_raw:
            self.attributes.append(HomeeAttribute(a))
        self._attribute_map: dict = None
        self.remap_attributes()
        self._on_changed_listeners = []
        self.groups: list[HomeeGroup] = []

    @property
    def raw_data(self):
        """Return Raw JSON Data of the node."""
        return self._data

    @property
    def id(self) -> int:
        """The unique id of the node."""
        return self._data["id"]

    @property
    def name(self) -> str:
        """The decoded primary name of the node."""
        return unquote(self._data["name"])

    @property
    def profile(self) -> int:
        """The NodeProfile of this node."""
        return self._data["profile"]

    @property
    def image(self) -> str:
        return self._data["image"]

    @property
    def favorite(self) -> int:
        return self._data["favorite"]

    @property
    def order(self) -> int:
        return self._data["order"]

    @property
    def protocol(self) -> int:
        """The network protocol of the node."""
        return self._data["protocol"]

    @property
    def routing(self) -> int:
        return self._data["routing"]

    @property
    def state(self) -> int:
        """State of availability."""
        return self._data["state"]

    @property
    def state_changed(self) -> int:
        return self._data["state_changed"]

    @property
    def added(self) -> int:
        return self._data["added"]

    @property
    def history(self) -> int:
        return self._data["history"]

    @property
    def cube_type(self) -> int:
        """Type of the Homee cube the node is part of."""
        return self._data["cube_type"]

    @property
    def note(self) -> str:
        """Text Note describing the node."""
        return unquote(self._data["note"])

    @property
    def services(self) -> int:
        return self._data["services"]

    @property
    def phonetic_name(self) -> str:
        """Name of the node."""
        return unquote(self._data["phonetic_name"])

    @property
    def owner(self) -> int:
        return self._data["owner"]

    @property
    def security(self) -> int:
        return self._data["security"]

    @property
    def attribute_map(self) -> dict | None:
        """Dict containing all attributes with attributeType as key."""
        return self._attribute_map

    @property
    def attributes_raw(self) -> list[dict]:
        """Return raw JSON of all the node's attributes."""
        return self._data["attributes"]

    def set_data(self, data: str) -> None:
        """Update data of the node."""
        self._data = data

    def get_attribute_index(self, attribute_id: int) -> int:
        """Find and return attribute for a given index."""
        return next(
            (i for i, a in enumerate(self.attributes) if a.id == attribute_id), -1
        )

    def get_attribute_by_type(self, attribute_type: int) -> HomeeAttribute:
        """Find and return attribute by attributeType."""
        return self._attribute_map[attribute_type]

    def get_attribute_by_id(self, attribute_id: int) -> HomeeAttribute:
        """Find and return attribute for a given id."""
        index = self.get_attribute_index(attribute_id)
        return self.attributes[index] if index != -1 else None

    def add_on_changed_listener(self, listener: Callable) -> Callable:
        """Add on_changed listener to node."""
        self._on_changed_listeners.append(listener)

        def remove_listener():
            self._on_changed_listeners.remove(listener)

        return remove_listener

    def _update_attribute(self, attribute_data: dict):
        # TODO: Remove in a future release.
        _LOGGER.warning(
            "_update_attribute() is deprecated - use update_attribute() instead"
        )
        self.update_attribute(attribute_data)

    def update_attribute(self, attribute_data: dict):
        """Update a single attribute of a node."""
        attribute = self.get_attribute_by_id(attribute_data["id"])
        if attribute is not None:
            attribute.set_data(attribute_data)
            for listener in self._on_changed_listeners:
                listener(self, attribute)

    def _update_attributes(self, attributes: list[dict]):
        # TODO: Remove in a future release.
        _LOGGER.warning(
            "_update_attributes() is deprecated - use update_attributes() instead"
        )
        self.update_attributes(attributes)

    def update_attributes(self, attributes: list[dict]):
        """Update the given attributes."""
        for attr in attributes:
            self.update_attribute(attr)

    def _remap_attributes(self):
        # TODO: Remove in a future release.
        _LOGGER.warning(
            "_remap_attributes() is deprecated - use remap_attributes() instead"
        )
        self.remap_attributes()

    def remap_attributes(self):
        """Remap the node's attributes."""
        if self._attribute_map is not None:
            self._attribute_map.clear()
        else:
            self._attribute_map = {}
        for a in self.attributes:
            self._attribute_map[a.type] = a


class HomeeGroup:
    """Representation of a Homee group."""

    def __init__(self, data) -> None:
        """Initialize a Homee group."""
        self._data = data
        self.nodes: list[HomeeNode] = []

    @property
    def id(self) -> int:
        """Id of the group, unique in Homee."""
        return self._data["id"]

    @property
    def name(self) -> str:
        """Decoded user given name of the group."""
        return unquote(self._data["name"])

    @property
    def image(self) -> str:
        return self._data["image"]

    @property
    def order(self) -> int:
        return self._data["order"]

    @property
    def added(self) -> int:
        return self._data["added"]

    @property
    def state(self) -> int:
        return self._data["state"]

    @property
    def category(self) -> int:
        return self._data["category"]

    @property
    def phonetic_name(self) -> str:
        return unquote(self._data["phonetic_name"])

    @property
    def note(self) -> str:
        """Note describing the group."""
        return self._data["note"]

    @property
    def services(self) -> int:
        return self._data["services"]

    @property
    def owner(self) -> int:
        return self._data["owner"]

    def set_data(self, data: str) -> None:
        """Update data of the group."""
        self._data = data


class HomeeSettings:
    """Representation of the settings object passed by Homee."""

    def __init__(self, data: dict) -> None:
        """Initialize settings."""
        self._data = data

    @property
    def address(self) -> str:
        """Street set by user."""
        return self._data["address"]

    @property
    def city(self) -> str:
        """City set by user."""
        return self._data["city"]

    @property
    def zip(self) -> str:
        """Zip code set by user."""
        return self._data["zip"]

    @property
    def state(self) -> str:
        """State set by user."""
        return self._data["state"]

    @property
    def latitude(self) -> float:
        """Latitude of set position of Homee."""
        return self._data["latitude"]

    @property
    def longitude(self) -> float:
        """Longitude of set position of Homee."""
        return self._data["longitude"]

    @property
    def country(self) -> str:
        """Country set by user."""
        return self._data["country"]

    @property
    def language(self) -> str:
        """Frontend language."""
        return self._data["language"]

    @property
    def remote_access(self) -> int:
        """Remote access enabled or not."""
        return self._data["remote_access"]

    @property
    def beta(self) -> int:
        """Is user accepting beta releases of firmware."""
        return self._data["beta"]

    @property
    def webhooks_key(self) -> str:
        """Key used for webhooks."""
        return self._data["webhooks_key"]

    @property
    def automatic_location_detection(self) -> int:
        return self._data["automatic_location_detection"]

    @property
    def polling_interval(self) -> float:
        """Standard polling interval set in Homee."""
        return self._data["polling_interval"]

    @property
    def timezone(self) -> str:
        """Timezone of Homee."""
        return self._data["timezone"]

    @property
    def enable_analytics(self) -> int:
        """Send analytical data back home."""
        return self._data["enable_analytics"]

    @property
    def homee_name(self) -> str:
        """Decoded name of Homee."""
        return unquote(self._data["homee_name"])

    @property
    def LastMissingCubeNotification(self) -> str:
        return self._data["LastMissingCubeNotification"]

    @property
    def local_ssl_enabled(self) -> bool:
        return self._data["local_ssl_enabled"]

    @property
    def wlan_enabled(self) -> int:
        return self._data["wlan_enabled"]

    @property
    def wlan_ssid(self) -> str:
        return self._data["wlan_ssid"]

    @property
    def wlan_mode(self) -> int:
        return self._data["wlan_mode"]

    @property
    def internet_access(self) -> bool:
        return self._data["internet_access"]

    @property
    def lan_enabled(self) -> int:
        return self._data["lan_enabled"]

    @property
    def lan_ip_address(self) -> str:
        return self._data["lan_ip_address"]

    @property
    def available_ssids(self) -> list[str]:
        return self._data["available_ssids"]

    @property
    def time(self) -> int:
        return self._data["time"]

    @property
    def civil_time(self) -> str:
        return self._data["civil_time"]

    @property
    def version(self) -> str:
        return self._data["version"]

    @property
    def uid(self) -> str:
        return self._data["uid"]

    @property
    def cubes(self) -> list[dict]:
        """List of cubes attached to this Homee."""
        return self._data["cubes"]

    @property
    def extensions(self) -> list[dict]:
        return self._data["extensions"]


class HomeeRelationship:
    """Representation of a Homee relationship."""

    def __init__(self, data):
        """Initialize the relationship."""
        self._data = data

    @property
    def id(self) -> int:
        """Id unique to this Homee."""
        return self._data["id"]

    @property
    def group_id(self) -> int:
        return self._data["group_id"]

    @property
    def node_id(self) -> int:
        return self._data["node_id"]

    @property
    def homeegram_id(self) -> int:
        return self._data["homeegram_id"]

    @property
    def order(self) -> int:
        return self._data["order"]

    def set_data(self, data: str) -> None:
        """Update data of the relationship."""
        self._data = data


# JSON to Python regex:
# Match: "([^"]*)":[^,]*,
# Replace: @property\ndef $1(self):\n\treturn self._data["$1"]\n
