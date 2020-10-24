from typing import Callable, List
from urllib.parse import unquote


class HomeeAttribute:
    def __init__(self, data: dict) -> None:
        self._data = data

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
        """TODO"""
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
        """The target value of the attribute. Only used to change the attribute value. In most cases you want to use current_value instead."""
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
        """How the attribute was changed. Compare with const.AttributeChangedBy"""
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


class HomeeNode:
    def __init__(self, data: dict) -> None:
        self._data = data
        self.attributes: List[HomeeAttribute] = []
        for a in self.attributes_raw:
            self.attributes.append(HomeeAttribute(a))
        self._attribute_map: dict = None
        self._remap_attributes()
        self._onChangedListeners = []

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
        return self._data["protocol"]

    @property
    def routing(self) -> int:
        return self._data["routing"]

    @property
    def state(self) -> int:
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
        return self._data["cube_type"]

    @property
    def note(self) -> str:
        return unquote(self._data["note"])

    @property
    def services(self) -> int:
        return self._data["services"]

    @property
    def phonetic_name(self) -> str:
        return unquote(self._data["phonetic_name"])

    @property
    def owner(self) -> int:
        return self._data["owner"]

    @property
    def security(self) -> int:
        return self._data["security"]

    @property
    def attributes_raw(self) -> List[dict]:
        return self._data["attributes"]

    def get_attribute_index(self, attributeId: int) -> int:
        return next(
            (i for i, a in enumerate(self.attributes) if a.id == attributeId), -1
        )

    def get_attribute_by_type(self, type: int) -> HomeeAttribute:
        return self._attribute_map[type]

    def get_attribute_by_id(self, attributeId: int) -> HomeeAttribute:
        index = self.get_attribute_index(attributeId)
        return self.attributes[index] if index != -1 else None

    def add_on_changed_listener(self, listener: Callable) -> Callable:
        self._onChangedListeners.append(listener)

        def remove_listener():
            self._onChangedListeners.remove(listener)

        return remove_listener

    def _update_attribute(self, attribute_data: dict):
        attribute = self.get_attribute_by_id(attribute_data["id"])
        if attribute != None:
            attribute._data = attribute_data
            result = [
                listener(self, attribute) for listener in self._onChangedListeners
            ]

    def _update_attributes(self, attributes: List[dict]):
        for attr in attributes:
            self._update_attribute(attr)

    def _remap_attributes(self):
        if self._attribute_map != None:
            self._attribute_map.clear()
        else:
            self._attribute_map = {}
        for a in self.attributes:
            self._attribute_map[a.type] = a
