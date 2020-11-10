# pymee
![PyPI](https://img.shields.io/pypi/v/pymee?style=for-the-badge)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymee?color=blue&logo=python&logoColor=yellow&style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/FreshlyBrewedCode/pymee?style=for-the-badge)

> pymee is the backbone of the [Home Assistant homee integration](https://github.com/FreshlyBrewedCode/hacs-homee).

pymee is an unofficial python library for interacting with the [homee](https://hom.ee) smart home/home automation platform. It uses the [websockets](https://github.com/aaugustin/websockets) library to connect to a local homee cube and maintains a list of nodes (devices), attributes, groups and more that are updated whenever new data arrives from homee.

Large parts of this library are directly ported from the awesome [homeeApi](https://github.com/stfnhmplr/homee-api) javascript library.

## Installation

Install from [PyPI](https://pypi.org/project/pymee/):
```
pip install pymee
```

## Usage

### Getting started

pymee should be used with `asyncio`:
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
    
    # Connect and start listening on a new task
    homeeTask = asyncio.create_task(homee.run())
    
    # Wait until the connection is live and all data has been received
    await homee.wait_until_connected()
    
    # Do something here...
    
    # Close the connection and wait until we are disconnected
    homee.disconnect()
    await homee.wait_until_disconnected()
    
# Start our entry point function
asyncio.run(main())
```
### Access devices and attributes

Devices are represented as "nodes" in the api. All nodes are available in the list `Homee.nodes` and are represented by the `HomeeNode` class.
Each node has a list of attributes accessible from `HomeeNode.attributes`. The attributes on a node represent the different attributes on a device, i.e. if a light is turned on or the target temperature of a thermostat. Attributes can be identified by the `HomeeAttribute.type` property. You can compare the type with the values from `pymee.const.AttributeType` to figure out what each attribute represents. The value can be accessed with the `HomeeAttribute.current_value` property.

If you need to change the value of an attribute you can use `Homee.set_value()`:
```python
# Get some node, for example using get_node_by_id
node = homee.get_node_by_id(5)

# Turn on the device. You need to pass the id of the node and the attribute as well as the value.
# Using get_attribute_by_type you can quickly find the desired attribute.
await homee.set_value(node.id, node.get_attribute_by_type(AttributeType.ON_OFF).id, 1)
```

### Receiving updates

The `Homee` class can be inherited to receive events:
```python
class MyHomee(Homee):
    # Called once the websocket connection has been established.
    async def on_connected(self):
        pass

    # Called after the websocket connection has been closed.
    async def on_disconnected(self):
        pass
        
    # Called after an error has occurred.
    async def on_error(self, error: str):
        pass

    # Called when the websocket receives a message. 
    # The message is automatically parsed from json into a dictionary.
    async def on_message(self, msg: dict):
        pass

    # Called when an 'attribute' message was received and an attribute was updated. 
    # Contains the parsed json attribute data and the corresponding node instance.
    async def on_attribute_updated(self, attribute_data: dict, node: HomeeNode):
        pass
```

You can also add a listener to specific nodes to receive attribute updates:
```python
# A listener is just a function that takes a node and an attribute
def my_node_handler(node: HomeeNode, attribute: HomeeAttribute):
    logging.info(f"Attribute {attribute.id} of node {node.name} was updated!")

node = homee.get_node_by_id(5)

# Adding the listener will return a function that can be called to remove the listener again
remove_listener = node.add_on_changed_listener(my_node_handler)

# If you don't need the listener anymore...
remove_listener()
```

### More examples

Example implementation that dumps all info into a json file and logs whenever a light is turned on or off:
```python
from pymee.const import NodeProfile, AttributeType
from pymee.model import HomeeAttribute

class JsonHomee(Homee):
    async def on_message(self, msg: dict):
        # Homee sends an "all" message at the beginning of each connection
        # or after 'GET:all' was send.
        if list(msg)[0] == "all":
            f = open("homee.json", "w")
            f.write(json.dumps(msg))
            f.close()

    async def on_attribute_updated(self, attribute_data, node):
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
