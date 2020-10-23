# pymee
![PyPI](https://img.shields.io/pypi/v/pymee)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymee?color=blue&logo=python&logoColor=yellow)
![GitHub last commit](https://img.shields.io/github/last-commit/FreshlyBrewedCode/pymee)

pymee is an unofficial python library for interacting with the [homee](https://hom.ee) smart home/home automation platform. It uses [websocket-client's](https://github.com/websocket-client/websocket-client) `websocket.WebsocketApp` to connect to a local homee cube and maintains a list of nodes (devices), attributes, groups and more that are updated whenever new data arrives from homee.

Large parts of this library are directly ported from the awesome [homeeApi](https://github.com/stfnhmplr/homee-api) javascript library.

## Installation

Install from [PyPI](https://pypi.org/project/pymee/):
```
pip install pymee
```

## Usage

pymee can be used with `asyncio`:
```python
from pymee import Homee
import asyncio
import logging

# Set debug level so we get verbose logs
logging.getLogger().setLevel(logging.DEBUG)

# Define a simple async entry point function
async def main():
    # Create an instance of Homee
    homee = Homee("<HOMEE IP>", "<USERNAME>", "<PASSWORD>")
    
    # Connect and wait until connection is closed again
    await homee.run()


# Start our entry point function
asyncio.run(main())
```

After that you can access devices and attributes using `homee.nodes` and `homee.get_node_index(id)` and modify attributes using `homee.set_value(nodeId, attributeId, value)`.


The `Homee` class can also be inherited to receive events:
```python
class MyHomee(Homee):
    # Called once the websocket connection has been established.
    def on_connected(self):
        pass

    # Called after the websocket connection has been closed.
    def on_disconnected(self):
        pass
        
    # Called after an error has occurred.
    def on_error(self, error: str):
        pass

    # Called when the websocket receives a message. 
    # The message is automatically parsed from json into a dictionary.
    def on_message(self, msg: dict):
        pass

    # Called when an 'attribute' message was received and an attribute was updated. 
    # Contains the parsed json attribute data and the corresponding node instance.
    def on_attribute_updated(self, attribute_data: dict, node: HomeeNode):
        pass
```

Example implementation that dumps all info into a json file and logs whenever a light is turned on or off:
```python
from pymee.const import NodeProfile, AttributeType
from pymee.model import HomeeAttribute

class JsonHomee(Homee):
    def on_message(self, msg: dict):
        # Homee sends an "all" message at the beginning of each connection
        # or after 'GET:all' was send.
        if list(msg)[0] == "all":
            f = open("homee.json", "w")
            f.write(json.dumps(msg))
            f.close()

    def on_attribute_updated(self, attribute_data, node):
        # Wrap the attribute data with the HomeeAttribute class for easier access
        attribute = HomeeAttribute(attribute_data)
        
        # We only care for changes
        if attribute.current_value == attribute.target_value:
            return
        
        # Check node profile (the type of device) and attribute type
        if (
            node.profile == NodeProfile.DIMMABLE_EXTENDED_COLOR_LIGHT
            and attribute.type == AttributeType.ON_OFF
        ):
            self._log(
                f"[Light] {node.name} turned {'on' if attribute.target_value == 1 else 'off'}"
            )
```

## License
MIT