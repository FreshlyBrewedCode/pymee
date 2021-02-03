# Changelog

<!--next-version-placeholder-->

## v1.4.0 (2021-02-03)
### Feature
* Enable automatic reconnection attempts ([`ee3fb00`](https://github.com/FreshlyBrewedCode/pymee/commit/ee3fb001067bb3ca90c1221584d1893cc7ebe085))

## v1.3.0 (2021-02-03)
### Feature
* Add manual websocket ping handler ([`773caa0`](https://github.com/FreshlyBrewedCode/pymee/commit/773caa0451d6b9353a1dd97ce8a37ad2e609a127))

### Documentation
* Use large badges in README ([`370006b`](https://github.com/FreshlyBrewedCode/pymee/commit/370006b58fb7a793ba130b8f5998b6c941c41bba))

## v1.2.0 (2020-11-10)
### Feature
* Handle `groups`, `nodes`, `group` and `relationship` message types ([`fddac28`](https://github.com/FreshlyBrewedCode/pymee/commit/fddac2831e0185464d2b9991ad04cc52dd28ef5b))
* Manage groups, settings and relationships using model ([`5650375`](https://github.com/FreshlyBrewedCode/pymee/commit/56503756a0ccd006aa57b0bebdbee5d6764173b9))
* Add `HomeeRelationship` model ([`21f2db0`](https://github.com/FreshlyBrewedCode/pymee/commit/21f2db01267bc917a2af568aa109eafa55bea071))
* Add `HomeeOptions` model ([`45efe54`](https://github.com/FreshlyBrewedCode/pymee/commit/45efe54709d2849f56d59fd26d8fb0a2a19f98e4))
* Add `HomeeGroup` model ([`9d3759f`](https://github.com/FreshlyBrewedCode/pymee/commit/9d3759fde70dfe8e9beea83e92f5437e90ea183e))

### Fix
* Decode strings in `HomeeGroup` ([`9db565e`](https://github.com/FreshlyBrewedCode/pymee/commit/9db565e7268f513d4ffd8b974af5116e3da9e6a7))

### Documentation
* Mention Home Assistant homee integration in README ([`d44c6b6`](https://github.com/FreshlyBrewedCode/pymee/commit/d44c6b6caa7ee82a76dff387805f5b7e7294b549))

## v1.1.2 (2020-11-01)
### Fix
* Fix exception handling bug that causes connection to close instantly ([`050d1d0`](https://github.com/FreshlyBrewedCode/pymee/commit/050d1d04c2b8bca243de1c8d50886ecce580aa67))

## v1.1.1 (2020-11-01)
### Fix
* Fix websocket exceptions not getting handled correctly causing websocket to stay open ([`624b383`](https://github.com/FreshlyBrewedCode/pymee/commit/624b383736371d44dfade05fdc803fb6f78c8bcd))

### Documentation
* Add link to websockets library in README ([`5f42af6`](https://github.com/FreshlyBrewedCode/pymee/commit/5f42af6367bea667dca275009cda2010e9e4712e))
* Update examples in README ([`0177066`](https://github.com/FreshlyBrewedCode/pymee/commit/01770668ecdd43ca364c96d6341f47080fc9ced3))

## v1.1.0 (2020-10-24)
### Feature
* Add `add_on_changed_listener()` to `HomeeNode` to support better update handling ([`12cc3d1`](https://github.com/FreshlyBrewedCode/pymee/commit/12cc3d17ea6aa4cc3354b76f97e1833ac7b029a5))

### Fix
* Add error handling to websocket receive and send handlers ([`6e9f021`](https://github.com/FreshlyBrewedCode/pymee/commit/6e9f02191ea2d107563d962a42681d1f18f54c5b))
* Change value type in `set_value()` from `int` to `float` ([`0974bac`](https://github.com/FreshlyBrewedCode/pymee/commit/0974bacd8a78b0103d222d7357b502e6fb63e042))
* Use module relative imports ([`4f33a6f`](https://github.com/FreshlyBrewedCode/pymee/commit/4f33a6f6ae8cde8ac788e1d9e02a2d4ec0d9b666))

## v1.0.1 (2020-10-23)
### Fix
* Bump to v1.0.1 to avoid PyPI conflict ([`573e700`](https://github.com/FreshlyBrewedCode/pymee/commit/573e70054d3711196b3e39d1cc9ba80b4794a13a))

## v1.0.0 (2020-10-23)
### Feature
* Add utility methods for getting nodes and atributes by id ([`f43014c`](https://github.com/FreshlyBrewedCode/pymee/commit/f43014cb77da7a4059695663a093a4acfb3b5d02))
* Support updating/adding nodes after receiving a 'nodes' message ([`535602b`](https://github.com/FreshlyBrewedCode/pymee/commit/535602b8b43696b29f0e1e9d86bcde9e40223dbb))
* Provide async disconnected event ([`c019ef5`](https://github.com/FreshlyBrewedCode/pymee/commit/c019ef5d55306007f98ee2d0154ccee138d2cb25))
* Use coroutines for Homee callbacks ([`99296e6`](https://github.com/FreshlyBrewedCode/pymee/commit/99296e650268467df6370c034d544c10c81530a1))
* Port to websockets package ([`1b578bc`](https://github.com/FreshlyBrewedCode/pymee/commit/1b578bc166cc0d9c6238980aca1a889a2e8ddef2))

### Breaking
* Homee callbacks need to be awaitable, i.e. async functions. Handleing callbacks in the event loop should provide a better development experience since most functions in the Homee api are async now.  ([`99296e6`](https://github.com/FreshlyBrewedCode/pymee/commit/99296e650268467df6370c034d544c10c81530a1))

### Documentation
* Add badges ♥ ([`a7e3a28`](https://github.com/FreshlyBrewedCode/pymee/commit/a7e3a28e7d6d8116c893214cd6e6b24ed5758c0f))

## v0.2.0 (2020-10-23)
### Feature
* Raise unique exceptions while acquiring access token ([`edac67b`](https://github.com/FreshlyBrewedCode/pymee/commit/edac67bad668349ced6d96f8306836f884d05937))

### Documentation
* Add install instructions and bump version ([`f0208a5`](https://github.com/FreshlyBrewedCode/pymee/commit/f0208a565523e63ff0ecf976c5288ffc0d4fc71a))
* Add README ([`8701f0a`](https://github.com/FreshlyBrewedCode/pymee/commit/8701f0ad47120d8291eb5b4f4c441cc151c468b2))
