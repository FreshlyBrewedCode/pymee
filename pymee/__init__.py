import asyncio
import hashlib
import json
from typing import List
import aiohttp
from aiohttp.helpers import BasicAuth
import websockets
from datetime import datetime
from .const import DeviceApp, DeviceOS, DeviceType
from .model import HomeeAttribute, HomeeNode
import re
import logging


class Homee:
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        device: str = "pymee",
        reconnectInterval: int = 5000,
        reconnect: bool = True,
        maxRetries: int = 5,
        loop: asyncio.AbstractEventLoop = None,
    ) -> None:

        self.host = host
        self.user = user
        self.password = password

        self.device = device
        self.shouldReconnect = reconnect
        self.reconnectInterval = reconnectInterval
        self.maxRetries = maxRetries

        self.deviceId = str(device).lower().replace(" ", "-")

        self.nodes: List[HomeeNode] = []
        self.groups = []
        self.relationships = []
        self.token = ""
        self.expires = 0
        self.connected = False
        self.retries = 0
        self.shouldClose = False

        self._message_queue = asyncio.Queue(loop=loop)
        self._connected_event = asyncio.Event(loop=loop)
        self._disconnected_event = asyncio.Event(loop=loop)

    async def get_access_token(self):
        """Asynchronously attempts to get an access token from the homee host using username and password."""

        client = aiohttp.ClientSession()
        auth = BasicAuth(
            self.user, hashlib.sha512(self.password.encode("utf-8")).hexdigest()
        )
        url = f"{self.url}/access_token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "device_name": self.device,
            "device_hardware_id": self.deviceId,
            "device_os": DeviceOS.LINUX,
            "device_type": DeviceType.NONE,
            "device_app": DeviceApp.HOMEE,
        }

        if self.token != None and self.expires > datetime.now().timestamp():
            return self.token

        if self.retries > 0:
            self.reconnect()

        self.retries += 1
        if self.retries > self.maxRetries:
            raise Exception("max retries reached")

        try:
            req = await client.post(
                url, auth=auth, data=data, headers=headers, timeout=5
            )
        except asyncio.TimeoutError as e:
            await client.close()
            raise e

        try:
            reqText = await req.text()
            regex = r"^access_token=([0-z]+)&.*&expires=(\d+)$"
            matches = re.match(regex, reqText)

            self.token = matches[1]
            self.expires = datetime.now().timestamp() + int(matches[2])

            self.retries = 0

        except:
            await client.close()
            raise AuthenticationFailedException

        await client.close()
        return self.token

    async def run(self):
        """Connects to homee after acquiring an access token and runs until the connection is closed. Should be used in combination with asyncio.create_task."""

        self.shouldClose = False

        try:
            await self.get_access_token()
        except:
            raise AuthenticationFailedException

        await self.open_ws()

    def start(self):
        """Wraps run() with asyncio.create_task() and returns the resulting task."""
        return asyncio.create_task(self.run())

    async def open_ws(self):
        """Opens the websocket connection assuming an access token was already received. Runs until connection is closed again."""

        self._log("Opening websocket...")

        if self.retries > 0:
            self.on_reconnect()

        self.retries += 1
        if self.retries > self.maxRetries:
            self.on_max_retries()
            return

        try:
            async with websockets.connect(
                uri=f"{self.ws_url}/connection?access_token={self.token}",
                subprotocols=["v2"],
            ) as ws:
                await self._ws_on_open()
                while not self.shouldClose:
                    receive_task = asyncio.ensure_future(self._ws_receive_handler(ws))
                    send_task = asyncio.ensure_future(self._ws_send_handler(ws))
                    done, pending = await asyncio.wait(
                        [receive_task, send_task],
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                    for task in pending:
                        task.cancel()
        except Exception as e:
            # TODO retry logic
            await self._ws_on_error(e)
            raise e

        await self._ws_on_close()

    async def _ws_receive_handler(self, ws: websockets.WebSocketClientProtocol):
        try:
            msg = await ws.recv()
            await self._ws_on_message(msg)
        except Exception as e:
            if not self.shouldClose:
                raise e

    async def _ws_send_handler(self, ws: websockets.WebSocketClientProtocol):
        try:
            msg = await self._message_queue.get()
            if self.connected and not self.shouldClose:
                await ws.send(msg)
        except Exception as e:
            if not self.shouldClose:
                raise e

    async def _ws_on_open(self):
        """Websocket on_open callback."""

        self._log("Connection to websocket successfull")

        self.connected = True
        self.retries = 1

        await self.on_connected()
        await self.send("GET:all")

    async def _ws_on_message(self, msg: str):
        """Websocket on_message callback."""

        await self._handle_message(json.loads(msg))

    async def _ws_on_close(self):
        """Websocket on_close callback."""
        # if not self.shouldClose and self.retries <= 1:

        self.connected = False
        self._disconnected_event.set()

        await self.on_disconnected()
        # if self.shouldReconnect and not self.shouldClose:
        # self.reconnect()

    async def _ws_on_error(self, error):
        """Websocket on_error callback."""

        self._log(f"An error occurred: {error}")
        await self.on_error(error)

    async def send(self, msg: str):
        """Send a raw string message to homee."""

        if not self.connected or self.shouldClose:
            return

        await self._message_queue.put(msg)

    async def reconnect(self):
        """TODO"""

        await asyncio.sleep(self.reconnectInterval * self.retries)
        await self.open_ws()

    def disconnect(self):
        """Disconnect from homee by closing the websocket connection."""

        self.shouldClose = True

    async def _handle_message(self, msg: dict):
        """Internal handleing of incoming homee messages."""

        msgType = None

        try:
            msgType = list(msg)[0]
        except:
            self._log(f"Invalid message: {msg}")
            await self.on_error()
            return

        self._log(msg)

        if msgType == "all":
            self.nodes = list(map(lambda n: HomeeNode(n), msg["all"]["nodes"]))
            self.groups = msg["all"]["groups"]
            self.relationships = msg["all"]["relationships"]
            self._connected_event.set()
        elif msgType == "attribute":
            await self._handle_attribute_change(msg["attribute"])
        elif msgType == "groups":
            self.groups = msg["groups"]
        elif msgType == "node":
            self._update_or_create_node(msg["node"])
        elif msgType == "nodes":
            self.nodes = msg["nodes"]
        elif msgType == "relationships":
            self.relationships = msg["relationships"]
        else:
            self._log(f"Unknown/Unsupported message type: {msgType}")

        await self.on_message(msg)

    async def _handle_attribute_change(self, attribute_data: dict):
        """Internal handleling of an attribute changed message."""

        self._log(f"Updating attribute {attribute_data['id']}")

        # try:
        attrNodeId = attribute_data["node_id"]
        node = self.get_node_by_id(attrNodeId)
        if node != None:
            node._update_attribute(attribute_data)
            await self.on_attribute_updated(attribute_data, node)
        # except:
        #     self._log("Unable to update attribute")

    def _update_or_create_node(self, node_data: dict):
        existingNode = self.get_node_by_id(node_data["id"])
        if existingNode != None:
            existingNode._data = node_data
            existingNode._update_attributes(node_data["attributes"])
        else:
            self.nodes.append(HomeeNode(node_data))

    def get_node_index(self, nodeId: int) -> int:
        """Returns the index of the node with the given id or -1 if no node with the given id exists."""
        return next((i for i, node in enumerate(self.nodes) if node.id == nodeId), -1)

    def get_node_by_id(self, nodeId: int) -> HomeeNode:
        """Returns the node with the given id or `None` if no node with the given id exists."""
        index = self.get_node_index(nodeId)
        return self.nodes[index] if index != -1 else None

    async def set_value(self, deviceId: int, attributeId: int, value: float):
        """Set the target value of an attribute of a device."""

        self._log(f"Set value: Device: {deviceId} Attribute: {attributeId} To: {value}")
        await self.send(
            f"PUT:/nodes/{deviceId}/attributes/{attributeId}?target_value={value}"
        )

    async def play_homeegram(self, homeegramId: int):
        """Invoke a homeegram."""

        await self.send(f"PUT:homeegrams/{homeegramId}?play=1")

    @property
    def url(self):
        """Local homee url."""

        return f"http://{self.host}:7681"

    @property
    def ws_url(self):
        """Local homee websocket url."""

        return f"ws://{self.host}:7681"

    def wait_until_connected(self):
        """"Returns a coroutine that runs until a connection has been established and the initial data has been received."""
        return self._connected_event.wait()

    def wait_until_disconnected(self):
        """Returns a coroutine that runs until the connection has been closed."""
        return self._disconnected_event.wait()

    def on_reconnect(self):
        """TODO"""
        pass

    def on_max_retries(self):
        """Called if the maximum amount of retries was reached."""

    async def on_connected(self):
        """Called once the websocket connection has been established."""

    async def on_disconnected(self):
        """Called after the websocket connection has been closed."""

    async def on_error(self, error: str = None):
        """Called after an error has occurred."""

    async def on_message(self, msg: dict):
        """Called when the websocket receives a message. The message is automatically parsed from json into a dictionary."""

    async def on_attribute_updated(self, attribute_data: dict, node: HomeeNode):
        """Called when an 'attribute' message was received and an attribute was updated. Contains the parsed json attribute data and the corresponding node instance."""

    def _log(self, msg: str):
        logging.debug(msg)


class HomeeException(Exception):
    """Base class for all errors thrown by this library"""


class AuthenticationFailedException(HomeeException):
    """Raised if no valid access token could be acquired."""
