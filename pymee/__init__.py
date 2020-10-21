import asyncio
import hashlib
import json
from typing import List
import aiohttp
from aiohttp.helpers import BasicAuth
import websocket
from datetime import datetime
from pymee.const import DeviceApp, DeviceOS, DeviceType
from pymee.model import HomeeNode
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
        self.ws = None
        self.token = ""
        self.expires = 0
        self.connected = False
        self.retries = 0
        self.shouldClose = False

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
            raise AuthenticationFailedException()

        await client.close()
        return self.token

    async def run(self):
        """Connects to homee after acquiring an access token and runs until the connection is closed. Should be used in combination with asyncio.create_task."""

        self.shouldClose = False

        try:
            await self.get_access_token()
        except:
            raise Exception("Unable to connect. Authentication failed.")

        self.open_ws()

    def start(self):
        """Wraps run() with asyncio.create_task() and returns the resulting task."""
        return asyncio.create_task(self.run())

    def open_ws(self):
        """Opens the websocket connection assuming an access token was already received. Runs until connection is closed again."""

        self._log("Opening websocket...")

        if self.retries > 0:
            self.on_reconnect()

        self.retries += 1
        if self.retries > self.maxRetries:
            self.on_max_retries()
            return

        try:
            self.ws = websocket.WebSocketApp(
                url=f"{self.ws_url}/connection?access_token={self.token}",
                subprotocols=["v2"],
                on_open=self._ws_on_open,
                on_message=self._ws_on_message,
                on_close=self._ws_on_close,
                on_error=self._ws_on_error,
            )
            self.ws.run_forever(origin=self.url)
        except:
            # TODO retry logic
            raise Exception("Unable to connect due to a websocket error")

    def _ws_on_open(self):
        """Websocket on_open callback."""

        self._log("Connection to websocket successfull")

        self.connected = True
        self.retries = 1

        self.on_connected()
        self.send("GET:all")

    def _ws_on_message(self, msg: str):
        """Websocket on_message callback."""

        self._handle_message(json.loads(msg))

    def _ws_on_close(self):
        """Websocket on_close callback."""
        # if not self.shouldClose and self.retries <= 1:

        self.connected = False
        self.ws = None

        self.on_disconnected()
        # if self.shouldReconnect and not self.shouldClose:
        # self.reconnect()

    def _ws_on_error(self, error):
        """Websocket on_error callback."""

        self._log(f"An error occurred: {error}")
        self.on_error(error)

    def send(self, msg: str):
        """Send a raw string message to homee."""

        if not self.connected or self.ws == None:
            return

        self.ws.send(msg)

    async def reconnect(self):
        """TODO"""

        await asyncio.sleep(self.reconnectInterval * self.retries)
        await self.open_ws()

    def disconnect(self):
        """Disconnect from homee by closing the websocket connection."""

        self.shouldClose = True

        if self.ws != None:
            self.ws.close()
        self._log("Connection closed")
        self.on_disconnected()

    def _handle_message(self, msg: dict):
        """Internal handleing of incoming homee messages."""

        msgType = None

        try:
            msgType = list(msg)[0]
        except:
            self._log(f"Invalid message: {msg}")
            self.on_error()
            return

        self._log(msg)

        if msgType == "all":
            self.nodes = list(map(lambda n: HomeeNode(n), msg["all"]["nodes"]))
            self.groups = msg["all"]["groups"]
            self.relationships = msg["all"]["relationships"]
        elif msgType == "attribute":
            self._handle_attribute_change(msg["attribute"])
        elif msgType == "groups":
            self.groups = msg["groups"]
        elif msgType == "node":
            self._update_node(msg["node"])
        elif msgType == "nodes":
            self.nodes = msg["nodes"]
        elif msgType == "relationships":
            self.relationships = msg["relationships"]
        else:
            self._log(f"Unknown/Unsupported message type: {msgType}")

        self.on_message(msg)

    def _handle_attribute_change(self, attribute_data: dict):
        """Internal handleling of an attribute changed message."""

        self._log(f"Updating attribute {attribute_data['id']}")

        # try:
        attrNodeId = attribute_data["node_id"]
        nodeIndex = self.get_node_index(attrNodeId)
        attrIndex = next(
            i
            for i, attr in enumerate(self.nodes[nodeIndex].attributes)
            if attr.id == attribute_data["id"]
        )
        self.nodes[nodeIndex]._update_attribute(attribute_data)
        self.on_attribute_updated(attribute_data, self.nodes[nodeIndex])
        # except:
        #     self._log("Unable to update attribute")

    def _update_node(self, node: dict):
        pass

    def get_node_index(self, nodeId: int):
        return next((i for i, node in enumerate(self.nodes) if node.id == nodeId), -1)

    def set_value(self, deviceId: int, attributeId: int, value: int):
        """Set the target value of an attribute of a device."""

        self._log(f"Set value: Device: {deviceId} Attribute: {attributeId} To: {value}")
        self.send(
            f"PUT:/nodes/{deviceId}/attributes/{attributeId}?target_value={value}"
        )

    def play_homeegram(self, homeegramId: int):
        """Invoke a homeegram."""

        self.send(f"PUT:homeegrams/{homeegramId}?play=1")

    @property
    def url(self):
        """Local homee url."""

        return f"http://{self.host}:7681"

    @property
    def ws_url(self):
        """Local homee websocket url."""

        return f"ws://{self.host}:7681"

    def on_reconnect(self):
        """TODO"""
        pass

    def on_max_retries(self):
        """Called if the maximum amount of retries was reached."""

    def on_connected(self):
        """Called once the websocket connection has been established."""

    def on_disconnected(self):
        """Called after the websocket connection has been closed."""

    def on_error(self, error: str):
        """Called after an error has occurred."""

    def on_message(self, msg: dict):
        """Called when the websocket receives a message. The message is automatically parsed from json into a dictionary."""

    def on_attribute_updated(self, attribute_data: dict, node: HomeeNode):
        """Called when an 'attribute' message was received and an attribute was updated. Contains the parsed json attribute data and the corresponding node instance."""

    def _log(self, msg: str):
        logging.info(msg)


class HomeeException(Exception):
    """Base class for all errors thrown by this library"""


class AuthenticationFailedException(HomeeException):
    """Raised if no valid access token could be acquired."""