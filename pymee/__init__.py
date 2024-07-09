"""Library for interacting with the homee smart home/home automation platform."""

import asyncio
from datetime import datetime
import hashlib
import json
import logging
import re

import aiohttp
import aiohttp.client_exceptions
from aiohttp.helpers import BasicAuth
import websockets

from .const import DeviceApp, DeviceOS, DeviceType
from .model import (
    HomeeDevice,
    HomeeGroup,
    HomeeNode,
    HomeeRelationship,
    HomeeSettings,
    HomeeUser,
    HomeeWarning,
)

_LOGGER = logging.getLogger(__name__)


class Homee:
    """Representation of a Homee system."""

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        device: str = "pymee",
        ping_interval: int = 30,
        reconnect_interval: int = 5,
        reconnect: bool = True,
        max_retries: int = 5,
    ) -> None:
        """Initialize the virtual Homee."""
        self.host = host
        self.user = user
        self.password = password

        self.device = device
        self.ping_interval = ping_interval
        self.should_reconnect = reconnect
        self.reconnect_interval = reconnect_interval
        self.max_retries = max_retries

        self.device_id = str(device).lower().replace(" ", "-")

        self.devices: list[HomeeDevice] = []
        self.groups: list[HomeeGroup] = []
        self.nodes: list[HomeeNode] = []
        self.relationships: list[HomeeRelationship] = []
        self.settings: HomeeSettings = None
        self.users: list[HomeeUser] = []
        self.warning: HomeeWarning = None
        self.token = ""
        self.expires = 0
        self.connected = False
        self.retries = 0
        self.should_close = False

        self._message_queue = asyncio.Queue()
        self._connected_event = asyncio.Event()
        self._disconnected_event = asyncio.Event()

    async def get_access_token(self):
        """Try asynchronously to get an access token from homee using username and password."""

        # Check if current token is still valid
        if self.token is not None and self.expires > datetime.now().timestamp():
            return self.token

        client = aiohttp.ClientSession()
        auth = BasicAuth(
            self.user, hashlib.sha512(self.password.encode("utf-8")).hexdigest()
        )
        url = f"{self.url}/access_token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "device_name": self.device,
            "device_hardware_id": self.device_id,
            "device_os": DeviceOS.LINUX,
            "device_type": DeviceType.NONE,
            "device_app": DeviceApp.HOMEE,
        }

        try:
            req = await client.post(
                url, auth=auth, data=data, headers=headers, timeout=5
            )
        except aiohttp.client_exceptions.ClientError as e:
            await client.close()
            raise AuthenticationFailedException from e

        try:
            req_text = await req.text()
            regex = r"^access_token=([0-z]+)&.*&expires=(\d+)$"
            matches = re.match(regex, req_text)

            self.token = matches[1]
            self.expires = datetime.now().timestamp() + int(matches[2])

            self.retries = 0

        except aiohttp.client_exceptions.ClientError as e:
            await client.close()
            raise AuthenticationFailedException from e

        await client.close()
        return self.token

    async def run(self):
        """Connect to homee after acquiring an access token and runs until the connection is closed.

        Should be used in combination with asyncio.create_task.
        """

        self.should_close = False
        initial_connect = True

        # Reconnect loop to avoid recursive reconnects
        while initial_connect or (
            not self.should_close
            and self.should_reconnect
            and self.retries < self.max_retries
        ):
            initial_connect = False

            # Sleep after reconnect
            if self.retries > 0:
                await asyncio.sleep(self.reconnect_interval * self.retries)
                _LOGGER.info(
                    "Attempting to reconnect in %s seconds",
                    self.reconnect_interval * self.retries,
                )

            try:
                await self.get_access_token()
            except AuthenticationFailedException:
                # Reconnect
                self.retries += 1
                continue

            await self.open_ws()

        # Handle max retries
        if self.retries >= self.max_retries:
            await self.on_max_retries()

    def start(self):
        """Wrap run() with asyncio.create_task() and returns the resulting task."""
        return asyncio.create_task(self.run())

    async def open_ws(self):
        """Open the websocket connection assuming an access token was already received.

        Runs until connection is closed again.
        """

        _LOGGER.info("Opening websocket")

        if self.retries > 0:
            await self.on_reconnect()

        try:
            async with websockets.connect(
                uri=f"{self.ws_url}/connection?access_token={self.token}",
                subprotocols=["v2"],
            ) as ws:
                await self._ws_on_open()

                while (not self.should_close) and self.connected:
                    try:
                        receive_task = asyncio.ensure_future(
                            self._ws_receive_handler(ws)
                        )
                        send_task = asyncio.ensure_future(self._ws_send_handler(ws))
                        done, pending = await asyncio.wait(
                            [receive_task, send_task],
                            return_when=asyncio.FIRST_COMPLETED,
                        )

                        exceptions = []

                        # Kill pending tasks
                        for task in pending:
                            task.cancel()

                        # Check if we finished with an exception
                        exceptions.extend(task.exception() for task in done)

                        if exceptions and exceptions[0] is not None:
                            raise exceptions[0]

                    except websockets.exceptions.ConnectionClosedError as e:
                        self.connected = False
                        await self.on_disconnected(e)
        except websockets.exceptions.WebSocketException as e:
            await self._ws_on_error(e)
        except TimeoutError:
            _LOGGER.info("Connection Timeout")
        except ConnectionError as e:
            _LOGGER.info("Connection Error: %s", e)

        self.retries += 1
        await self._ws_on_close()

    async def _ws_receive_handler(self, ws: websockets.WebSocketClientProtocol):
        try:
            msg = await ws.recv()
            await self._ws_on_message(msg)
        except websockets.exceptions.ConnectionClosedOK:
            return
        except websockets.exceptions.ConnectionClosedError as e:
            if not self.should_close:
                self.connected = False
                raise e

    async def _ws_send_handler(self, ws: websockets.WebSocketClientProtocol):
        try:
            msg = await self._message_queue.get()
            if self.connected and not self.should_close:
                await ws.send(msg)
        except websockets.exceptions.ConnectionClosed as e:
            if not self.should_close:
                self.connected = False
                raise e

    async def _ws_on_open(self):
        """Websocket on_open callback."""

        _LOGGER.info("Connection to websocket successfull")

        self.connected = True

        await self.on_connected()
        self.retries = 0

        await self.send("GET:all")

    async def _ws_on_message(self, msg: str):
        """Websocket on_message callback."""

        await self._handle_message(json.loads(msg))

    async def _ws_on_close(self):
        """Websocket on_close callback."""
        # if not self.should_close and self.retries <= 1:

        if self.connected:
            self.connected = False
            self._disconnected_event.set()

            await self.on_disconnected()

    async def _ws_on_error(self, error):
        """Websocket on_error callback."""

        await self.on_error(error)

    async def send(self, msg: str):
        """Send a raw string message to homee."""

        if not self.connected or self.should_close:
            return

        await self._message_queue.put(msg)

    async def reconnect(self):
        """Start a reconnection attempt."""

        await self.run()

    def disconnect(self):
        """Disconnect from homee by closing the websocket connection."""

        self.should_close = True

    async def _handle_message(self, msg: dict):
        """Handle incoming homee messages."""

        msg_type = None

        try:
            msg_type = list(msg)[0]
        except TypeError:
            _LOGGER.warning("Invalid message: %s", msg)
            await self.on_error()
            return

        _LOGGER.debug(msg)

        if msg_type == "all":
            self.settings = HomeeSettings(msg["all"]["settings"])

            # Create / Update nodes
            if len(self.nodes) <= 0:
                # Since there might be lots of nodes, we don't want to check for
                # all in the next step, so if we start up, just add all nodes.
                self.nodes = [HomeeNode(node_data) for node_data in msg["all"]["nodes"]]
            else:
                for node_data in msg["all"]["nodes"]:
                    self._update_or_create_node(node_data)

            # Create / Update groups
            for group_data in msg["all"]["groups"]:
                self._update_or_create_group(group_data)

            # Create / Update users
            for user_data in msg["all"]["users"]:
                self._update_or_create_user(user_data)

            self._update_or_create_relationships(msg["all"]["relationships"])

            self._remap_relationships()
            self._connected_event.set()

        elif msg_type == "attribute":
            await self._handle_attribute_change(msg["attribute"])
        # Not sure, if devices can be sent alone or only with user, but just in case...
        elif msg_type == "device":
            self._update_or_create_device(msg["device"])
        elif msg_type == "devices":
            for data in msg["devices"]:
                self._update_or_create_device(data)
        elif msg_type == "group":
            self._update_or_create_group(msg["group"])
        elif msg_type == "groups":
            for data in msg["groups"]:
                self._update_or_create_group(data)
        elif msg_type == "node":
            self._update_or_create_node(msg["node"])
        elif msg_type == "nodes":
            for data in msg["nodes"]:
                self._update_or_create_node(data)
        elif msg_type == "relationship":
            self._update_or_create_relationship(msg["relationship"])
        elif msg_type == "relationships":
            self._update_or_create_relationships(msg["relationships"])
            self._remap_relationships()
        elif msg_type == "user":
            self._update_or_create_user(msg["user"])
        elif msg_type == "users":
            for data in msg["users"]:
                self._update_or_create_user(data)
        elif msg_type == "warning":
            await self._update_warning(msg["warning"])
        else:
            _LOGGER.info(
                "Unknown/Unsupported message type: %s.\nMessage: %s", msg_type, msg
            )

        await self.on_message(msg)

    async def _handle_attribute_change(self, attribute_data: dict):
        """Handle an attribute changed message."""

        _LOGGER.info("Updating attribute %s", attribute_data["id"])

        attr_node_id = attribute_data["node_id"]
        node = self.get_node_by_id(attr_node_id)
        if node is not None:
            node.update_attribute(attribute_data)
            await self.on_attribute_updated(attribute_data, node)

    def _update_or_create_node(self, node_data: dict):
        existing_node = self.get_node_by_id(node_data["id"])
        if existing_node is not None:
            existing_node.set_data(node_data)
            existing_node.update_attributes(node_data["attributes"])
        else:
            self.nodes.append(HomeeNode(node_data))
            self._remap_relationships()

    def _update_or_create_group(self, data: dict):
        group = self.get_group_by_id(data["id"])
        if group is not None:
            group.set_data(data)
        else:
            self.groups.append(HomeeGroup(data))
            self._remap_relationships()

    def _update_or_create_relationship(self, data: dict):
        relationship: HomeeRelationship = next(
            (r for r in self.relationships if r.id == data["id"]), None
        )

        if relationship is not None:
            relationship.set_data(data)
        else:
            self.relationships.append(HomeeRelationship(data))
        self._remap_relationships()

    def _update_or_create_relationships(self, data: dict):
        if len(self.relationships) <= 0:
            self.relationships = [
                HomeeRelationship(relationship_data) for relationship_data in data
            ]
        else:
            for relationship_data in data:
                self._update_or_create_relationship(relationship_data)

    def _remap_relationships(self):
        """Remap the relationships between nodes and groups defined by the relationships list."""

        # Clear existing relationships
        for n in self.nodes:
            n.groups.clear()
        for g in self.groups:
            g.nodes.clear()

        for r in self.relationships:
            node = self.get_node_by_id(r.node_id)
            group = self.get_group_by_id(r.group_id)

            if node is not None and group is not None:
                node.groups.append(group)
                group.nodes.append(node)

    def _update_or_create_user(self, data: dict):
        """Create a user or update if already exists."""
        user = self.get_user_by_id(data["id"])
        if user is not None:
            user.set_data(data)
        else:
            self.users.append(HomeeUser(data))

        # Create / Update the devices of the user
        for device in data["devices"]:
            self._update_or_create_device(device)

    def _update_or_create_device(self, data: dict):
        """Create a device or update if already exists."""
        device = self.get_device_by_id(data["id"])
        if device is not None:
            device.set_data(data)
        else:
            self.devices.append(HomeeDevice(data))

    async def _update_warning(self, data: dict):
        """Set the warning to the latest one received."""
        self.warning = HomeeWarning(data)
        await self.on_warning()

    def get_node_index(self, node_id: int) -> int:
        """Return the index of the node with the given id or -1 if none exists."""
        return next((i for i, node in enumerate(self.nodes) if node.id == node_id), -1)

    def get_node_by_id(self, node_id: int) -> HomeeNode:
        """Return the node with the given id or 'None' if none exists."""
        index = self.get_node_index(node_id)
        return self.nodes[index] if index != -1 else None

    def get_group_index(self, group_id: int) -> int:
        """Return the index of the group with the given id or -1 if none exists."""
        return next(
            (i for i, group in enumerate(self.groups) if group.id == group_id), -1
        )

    def get_group_by_id(self, group_id: int) -> HomeeGroup:
        """Return the group with the given id or 'None' if no group with the given id exists."""
        index = self.get_group_index(group_id)
        return self.groups[index] if index != -1 else None

    def get_user_by_id(self, user_id: int) -> HomeeUser:
        """Return the user with the given id or 'None' if no user with the given id exists."""
        index = next((i for i, user in enumerate(self.users) if user.id == user_id), -1)
        return self.users[index] if index != -1 else None

    def get_device_by_id(self, device_id: int) -> HomeeDevice:
        """Return the device with the given id or 'None' if no device with the given id exists."""
        index = next(
            (i for i, device in enumerate(self.devices) if device.id == device_id), -1
        )
        return self.devices[index] if index != -1 else None

    async def set_value(self, device_id: int, attribute_id: int, value: float):
        """Set the target value of an attribute of a device."""

        _LOGGER.info(
            "Set value: Device: %s Attribute: %s To: %s", device_id, attribute_id, value
        )
        await self.send(
            f"PUT:/nodes/{device_id}/attributes/{attribute_id}?target_value={value}"
        )

    async def update_node(self, node_id: int):
        """Request current data for a node."""
        _LOGGER.info("Request current data for node %s", node_id)
        await self.send(f"GET:/nodes/{node_id}/")

    async def update_attribute(self, node_id: int, attribute_id: int):
        """Request current data for an attribute."""
        _LOGGER.info(
            "Request current data for attribute %s of device %s", attribute_id, node_id
        )
        await self.send(f"GET:/nodes/{node_id}/attributes/{attribute_id}")

    async def play_homeegram(self, homeegram_id: int):
        """Invoke a homeegram."""

        await self.send(f"PUT:homeegrams/{homeegram_id}?play=1")

    @property
    def url(self):
        """Local homee url."""

        return f"http://{self.host}:7681"

    @property
    def ws_url(self):
        """Local homee websocket url."""

        return f"ws://{self.host}:7681"

    def wait_until_connected(self):
        """Return a coroutine that runs until a connection has been established."""
        return self._connected_event.wait()

    def wait_until_disconnected(self):
        """Return a coroutine that runs until the connection has been closed."""
        return self._disconnected_event.wait()

    async def on_reconnect(self):
        """Execute right before a reconnection attempt is started."""
        _LOGGER.info("Homee %s Reconnecting", self.device)

    async def on_max_retries(self):
        """Execute if the maximum amount of retries was reached."""
        _LOGGER.warning(
            "Could not reconnect Homee %s after %s retries",
            self.device,
            self.max_retries,
        )

    async def on_connected(self):
        """Execute once the websocket connection has been established."""
        if self.retries > 0:
            _LOGGER.warning(
                "Homee %s Reconnected after %s retries", self.device, self.retries
            )

    async def on_disconnected(self, error=None):
        """Execute after the websocket connection has been closed."""
        if not self.should_close:
            _LOGGER.warning("Homee %s Disconnected. Error: %s", self.device, error)

    async def on_error(self, error: str | None = None):
        """Execute after an error has occurred."""
        _LOGGER.error("An error occurred: %s", error)

    async def on_message(self, msg: dict):
        """Execute when the websocket receives a message.

        The message is automatically parsed from json into a dictionary.
        """

    async def on_warning(self):
        """Execute when a warning message is received."""

    async def on_attribute_updated(self, attribute_data: dict, node: HomeeNode):
        """Execute when an 'attribute' message was received and an attribute was updated.

        Contains the parsed json attribute data and the corresponding node instance.
        """


class HomeeException(Exception):
    """Base class for all errors thrown by this library."""


class AuthenticationFailedException(HomeeException):
    """Raised if no valid access token could be acquired."""
