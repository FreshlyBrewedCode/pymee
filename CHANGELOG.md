# CHANGELOG



## v2.1.0 (2024-07-04)

### Feature

* feat: parse warning message
This adds support for the warning message type in shich homee announces events or start and stop of certain modes. ([`86d63f5`](https://github.com/FreshlyBrewedCode/pymee/commit/86d63f57272425a853bafea4e881437530015edd))

### Fix

* fix: order of github release actions ([`5592df0`](https://github.com/FreshlyBrewedCode/pymee/commit/5592df054d262cc00cc60a594eb3910576aa0bcb))

### Unknown

* Merge pull request #29 from Taraman17/master

Add Support for warning message ([`92d3273`](https://github.com/FreshlyBrewedCode/pymee/commit/92d3273290fb6dd433635f2d4780749be5e50180))

* Merge branch &#39;FreshlyBrewedCode:master&#39; into master ([`3238a85`](https://github.com/FreshlyBrewedCode/pymee/commit/3238a85cf9d6a9d886cae67f80c30915ba384c76))


## v2.0.5 (2024-07-03)

### Fix

* fix: deprecation in upload-artifacts action ([`f89de1d`](https://github.com/FreshlyBrewedCode/pymee/commit/f89de1d14e2fd5732578e9b20c181101647c6ab8))

### Unknown

* Merge pull request #28 from Taraman17/master

fix: deprecation in upload-artifacts action ([`3549088`](https://github.com/FreshlyBrewedCode/pymee/commit/35490881478b5716333c7c29ca5b1aeacd7e166d))

* Merge pull request #27 from Taraman17/master

setup new workflow again after fixes on pypi ([`b6b4ddf`](https://github.com/FreshlyBrewedCode/pymee/commit/b6b4ddf529f2a5f3fc705150634441894af3cb09))

* setup new workflow again after fixes on pypi ([`4cabdb1`](https://github.com/FreshlyBrewedCode/pymee/commit/4cabdb17f21afc517cf07780408d26cb88eb2f06))


## v2.0.4 (2024-06-10)

### Fix

* fix: version number for current workflow ([`47a786b`](https://github.com/FreshlyBrewedCode/pymee/commit/47a786b83ef243e9386748a35a1880f3fb473597))

* fix: revert python-smantic-release to v7 ([`4e56b3c`](https://github.com/FreshlyBrewedCode/pymee/commit/4e56b3c55a631093174af818d126ef24de922009))

### Unknown

* Merge pull request #25 from Taraman17/master

fix: version number for current workflow ([`6d71930`](https://github.com/FreshlyBrewedCode/pymee/commit/6d719301105d6cb028a83f58f93e7ed413f7dd4f))

* Merge pull request #24 from Taraman17/master

fix: revert python-smantic-release to v7 ([`8784619`](https://github.com/FreshlyBrewedCode/pymee/commit/8784619b9582796cec0ebf7cf7f0bc5ea8dc460d))


## v2.0.3 (2024-06-10)

### Fix

* fix: add package build to release action ([`f6d3230`](https://github.com/FreshlyBrewedCode/pymee/commit/f6d3230bbba2aacfbc87f9150d5c73e1c685a77f))

### Unknown

* Merge pull request #23 from Taraman17/master

fix: add package build to release action ([`f282bd7`](https://github.com/FreshlyBrewedCode/pymee/commit/f282bd74147324c2a0647e04f5a2668d1db82d87))


## v2.0.2 (2024-06-10)

### Fix

* fix: workflow checkout action ([`75fb990`](https://github.com/FreshlyBrewedCode/pymee/commit/75fb990d075623e9eccc8bef074aed9d77e64629))

### Unknown

* Merge pull request #22 from Taraman17/master

fix: workflow checkout action ([`7698e52`](https://github.com/FreshlyBrewedCode/pymee/commit/7698e5224c692afe5f11043b27358f5c1797a9af))

* Merge pull request #21 from Taraman17/master

fix release workflow pypi token ([`fc93ce2`](https://github.com/FreshlyBrewedCode/pymee/commit/fc93ce2f07b8f4a02ae5b44b5e062e249ed2eadf))

* fix release workflow pypi token ([`06d5103`](https://github.com/FreshlyBrewedCode/pymee/commit/06d5103d06ec9e5227507aaae8ecc04548a69288))


## v2.0.1 (2024-06-10)

### Fix

* fix: permissions for release workflow ([`b063c91`](https://github.com/FreshlyBrewedCode/pymee/commit/b063c9125bb3825b696f09b93db53cc3b167a8a5))

* fix: release workflow 2nd try ([`598e592`](https://github.com/FreshlyBrewedCode/pymee/commit/598e592e2fa2e8224571424b7ada7bdd63680d9a))

* fix: release workflow ([`1d77638`](https://github.com/FreshlyBrewedCode/pymee/commit/1d77638587c72420da5187668a9be13486c7dee6))

### Unknown

* Merge pull request #20 from Taraman17/master

fix: permissions for release workflow ([`99a38d2`](https://github.com/FreshlyBrewedCode/pymee/commit/99a38d2da4bfe376e22dc9fad25ffd11f1880656))

* Merge pull request #19 from Taraman17/master

fix: release workflow 2nd try ([`1b2a98e`](https://github.com/FreshlyBrewedCode/pymee/commit/1b2a98eff9f8e026a2c582e236740f05d022c8af))

* Merge pull request #18 from Taraman17/master

fix: release workflow ([`7fe5760`](https://github.com/FreshlyBrewedCode/pymee/commit/7fe5760ef5af962d1ea2c675232bf3f4d5e22797))


## v2.0.0 (2024-06-10)

### Breaking

* fix: Finalise release.

BREAKING CHANGE: Using IntEnum for constants.

Addressing members changed.
Corrected Names of following NodeProtocol entries:
- WMBUS -&gt; WM_BUS
- HTTPAVM -&gt; HTTP_AVM
- HTTPNETATMO -&gt; HTTP_NETATMO
- HTTPKOUBACHI -&gt; HTTP_KOUBACHI
- HTTPNEST -&gt; HTTP_NEST
- IOCUBE -&gt; IO_CUBE
- HTTPCCU2 -&gt; HTTP_CCU_2
- HTTPUPN_P -&gt; HTTP_UPN_P
- HTTPNUKI -&gt; HTTP_NUKI
- HTTPSEMS -&gt; HTTP_SEMS
- SIGMA_ZWAVE -&gt; ZWAVE_V3
- HTTPWOLF -&gt; HTTP_WOLF
- HTTPMY_STROM -&gt; HTTP_MY_STROM

Refactored code to make it python-standard-conforming:

Homee attributes, that changed names:
- pingInterval -&gt; ping_interval
- reconnectInterval -&gt; reconnect_interval
- maxRetries -&gt; max_retries
- shouldReconnect -&gt; should_reconnect
- deviceId -&gt; device_id
- shouldClose -&gt; should_close

Some methods are now public - the old private versions log deprecation warnings.

Raw data of Homee Classes is now accessible through the .raw_data public attribute i.s.o .raw_data
To update the raw data, the method .set_data(data) is used. ([`e2e1848`](https://github.com/FreshlyBrewedCode/pymee/commit/e2e18484c992848390069129581272b29caf3a3e))

### Ci

* ci: update release workflow to latest versions ([`785749f`](https://github.com/FreshlyBrewedCode/pymee/commit/785749fff9db004f3f6cca6253fb775ef81bb34a))

### Unknown

* Merge pull request #17 from Taraman17/master

refactor: Change const classes to IntEnum, refactor code.

BREAKING CHANGE: Using IntEnum for constants.

Addressing members changed.
Corrected Names of following NodeProtocol entries:

    WMBUS -&gt; WM_BUS
    HTTPAVM -&gt; HTTP_AVM
    HTTPNETATMO -&gt; HTTP_NETATMO
    HTTPKOUBACHI -&gt; HTTP_KOUBACHI
    HTTPNEST -&gt; HTTP_NEST
    IOCUBE -&gt; IO_CUBE
    HTTPCCU2 -&gt; HTTP_CCU_2
    HTTPUPN_P -&gt; HTTP_UPN_P
    HTTPNUKI -&gt; HTTP_NUKI
    HTTPSEMS -&gt; HTTP_SEMS
    SIGMA_ZWAVE -&gt; ZWAVE_V3
    HTTPWOLF -&gt; HTTP_WOLF
    HTTPMY_STROM -&gt; HTTP_MY_STROM

Refactored code to make it python-standard-conforming:

Homee attributes, that changed names:

    pingInterval -&gt; ping_interval
    reconnectInterval -&gt; reconnect_interval
    maxRetries -&gt; max_retries
    shouldReconnect -&gt; should_reconnect
    deviceId -&gt; device_id
    shouldClose -&gt; should_close

Some methods are now public - the old private versions log deprecation warnings.

Raw data of Homee Classes is now accessible through the .raw_data public attribute i.s.o .raw_data
To update the raw data, the method .set_data(data) is used. ([`8a27aa0`](https://github.com/FreshlyBrewedCode/pymee/commit/8a27aa08e342ddec1ee99aa3fab6aa2e2e92087c))

* tackle linter warnings part 3 - exceptions ([`2aa0e07`](https://github.com/FreshlyBrewedCode/pymee/commit/2aa0e07dd3a9a4f4f0a6354811dbc2ffb9154346))

* fix bug in update_attribute ([`04202d7`](https://github.com/FreshlyBrewedCode/pymee/commit/04202d7e3b55f4f1f0822d9b373839573dbe134f))

* tackle linter warnings part 2 ([`dafaf2d`](https://github.com/FreshlyBrewedCode/pymee/commit/dafaf2d9645ea26b3621e8c76f35805d172bf666))

* tackle linter warnings part 1 ([`413ac86`](https://github.com/FreshlyBrewedCode/pymee/commit/413ac86cce1c4fc58c2c263fb3f117b978fb1ee4))

* Use IntEnum for const classes ([`895aa8c`](https://github.com/FreshlyBrewedCode/pymee/commit/895aa8cc7956d45db6e16c703bdc29f17a00cd92))

* fix errors and add new constants from API ([`b55bc5f`](https://github.com/FreshlyBrewedCode/pymee/commit/b55bc5f2f4317c95136f52994746aab59a5d2e70))

* Add logging of unsupported messages

This logs messages that are not understood by pymee, so we can see these and add support easier. ([`e519233`](https://github.com/FreshlyBrewedCode/pymee/commit/e519233e379e210926526ff8bfc99df52f75cdbb))


## v1.11.2 (2024-03-18)

### Fix

* fix: Catch OS Level connection error (#14)

* Remove expicit ping

Removing the ping-handler function and it&#39;s call, since websockets sends pings automatically and the function was causing async_io errors.

* Refine error handling and logging

Narrrow websocket exception hadnling to &#34;ConnectionClosedError&#34; from &#34;ConnectionClosed&#34; where feasible.
some logging changes

* expose attribute_map

Expose _attribute_map as public property, since it is used in hass-homee

* Tackle deprecations and lint warnings

- Replace typing.List with list
- remove unnecessary else:s
- use Callable from collections.abc

* refine logging

- log disconnect and reconnect once as per https://developers.home-assistant.io/docs/integration_quality_scale_index/
- use %s instead of f-strings in Log-statements as per HA style guide: https://developers.home-assistant.io/docs/development_guidelines/#use-new-style-string-formatting

* fix typo

* fix some nits

- make sure disconnect warning is only logged once.
- move logging of reconnect attempts to proper location.

* Deal with attributes without options

If trying to access options if the attribute has none leads to an error.
This fixes it.

* Now really deal with empty options

First attempt had a wrong idea.

* Add catch for OS ConnectionError

If a connection error throws at  OS Level (e.g. 113 -  No route to host), it was not caught. ([`06a15e4`](https://github.com/FreshlyBrewedCode/pymee/commit/06a15e465f42e82c58f9b02bf4b665f6bb09d6d9))


## v1.11.1 (2024-02-06)

### Fix

* fix: Fix error when HomeeAttribute has no options (#13)

* Remove expicit ping

Removing the ping-handler function and it&#39;s call, since websockets sends pings automatically and the function was causing async_io errors.

* Refine error handling and logging

Narrrow websocket exception hadnling to &#34;ConnectionClosedError&#34; from &#34;ConnectionClosed&#34; where feasible.
some logging changes

* expose attribute_map

Expose _attribute_map as public property, since it is used in hass-homee

* Tackle deprecations and lint warnings

- Replace typing.List with list
- remove unnecessary else:s
- use Callable from collections.abc

* refine logging

- log disconnect and reconnect once as per https://developers.home-assistant.io/docs/integration_quality_scale_index/
- use %s instead of f-strings in Log-statements as per HA style guide: https://developers.home-assistant.io/docs/development_guidelines/#use-new-style-string-formatting

* fix typo

* fix some nits

- make sure disconnect warning is only logged once.
- move logging of reconnect attempts to proper location.

* Deal with attributes without options

If trying to access options if the attribute has none leads to an error.
This fixes it.

* Now really deal with empty options

First attempt had a wrong idea. ([`cbb67ae`](https://github.com/FreshlyBrewedCode/pymee/commit/cbb67ae6f6a3f05129a73708a109434078243571))


## v1.11.0 (2024-01-31)

### Feature

* feat: Fix automatic reconnection (#12)

* Remove expicit ping

Removing the ping-handler function and it&#39;s call, since websockets sends pings automatically and the function was causing async_io errors.

* Refine error handling and logging

Narrrow websocket exception hadnling to &#34;ConnectionClosedError&#34; from &#34;ConnectionClosed&#34; where feasible.
some logging changes

* expose attribute_map

Expose _attribute_map as public property, since it is used in hass-homee

* Tackle deprecations and lint warnings

- Replace typing.List with list
- remove unnecessary else:s
- use Callable from collections.abc

* refine logging

- log disconnect and reconnect once as per https://developers.home-assistant.io/docs/integration_quality_scale_index/
- use %s instead of f-strings in Log-statements as per HA style guide: https://developers.home-assistant.io/docs/development_guidelines/#use-new-style-string-formatting

* fix typo

* fix some nits

- make sure disconnect warning is only logged once.
- move logging of reconnect attempts to proper location. ([`2db8f2f`](https://github.com/FreshlyBrewedCode/pymee/commit/2db8f2ff240814bdf2fc7295ffa9bded87b66e5d))


## v1.10.3 (2023-11-12)

### Fix

* fix: &#39;list&#39; object is not an iterator &amp; spaces in homee name (#11)

* add function to get an update for an attribute

* Change get_attribute to update_attribute and add update_node

* Fix invalid state error

* Add manual update functions to readme

* fix list object is not an iterator

* unquote homee_name

closes #7 ([`1a8dcc1`](https://github.com/FreshlyBrewedCode/pymee/commit/1a8dcc16f6dc7b52ce6e3593fb05e65dd02b7993))


## v1.10.2 (2023-11-04)

### Fix

* fix: Fix &#34;&#39;list&#39; object is not an iterator&#34; (#10)

* add function to get an update for an attribute

* Change get_attribute to update_attribute and add update_node

* Fix invalid state error

* Add manual update functions to readme ([`87d90d1`](https://github.com/FreshlyBrewedCode/pymee/commit/87d90d1060b9b8203180f9d6b8e6d5f8721cb7ab))


## v1.10.1 (2023-10-24)

### Fix

* fix: fix version number in setup.py ([`1f8fdb7`](https://github.com/FreshlyBrewedCode/pymee/commit/1f8fdb73f33d91d64f045aec7c59119683c57a46))

* fix: fix workflow and trigger release ([`22e4c58`](https://github.com/FreshlyBrewedCode/pymee/commit/22e4c5825774dec96d42c6c616083f0324d49b3a))


## v1.10.0 (2023-10-24)

### Feature

* feat: change get_attribute to update_attribute and add update_node (#9)

* add function to get an update for an attribute

* Change get_attribute to update_attribute and add update_node ([`750bfef`](https://github.com/FreshlyBrewedCode/pymee/commit/750bfefd32b9f96d0270143bb2de7bf345295cf9))


## v1.9.0 (2023-10-24)

### Feature

* feat: add function to get an update for an attribute (#8) ([`298b5af`](https://github.com/FreshlyBrewedCode/pymee/commit/298b5afa1079ba0e3db5644699c33c3680410646))


## v1.8.0 (2023-06-23)

### Feature

* feat: add attribute options (#6)

Homee Attributes can have options, that will be exposed with this patch.
Options that are not present will have empty values. ([`81f339a`](https://github.com/FreshlyBrewedCode/pymee/commit/81f339aafd36a838e6376066775f9753d10b397e))


## v1.7.1 (2023-06-11)

### Fix

* fix: fix failure to reconnect on remote disconnect (#4) ([`af09a42`](https://github.com/FreshlyBrewedCode/pymee/commit/af09a42dd91c6b6deffbfc30532ff52d57b00537))


## v1.7.0 (2023-05-05)

### Feature

* feat: Change Logging to use nemd logger (#3)

This changes logging, so it uses a logger with (__name__), so logs can be identified easier.

This also will enable log configuration in Home Assistant. ([`40f32c4`](https://github.com/FreshlyBrewedCode/pymee/commit/40f32c462d7a9cec7eef590e4bb77046527213a4))


## v1.6.0 (2023-02-20)

### Feature

* feat: add more constants to allow additional devices / profiles (#2)

- Update const.py
- Add AttributeTypes above 324
- Count up Version number
- v1.5.5 add attributes
- Add more constants
- Added constants found in https://github.com/stfnhmplr/homee-api/blob/main/lib/enums.js
- revert version number - will be done automatically
- revert version 1.5.5. change - will be done automatically. ([`2914835`](https://github.com/FreshlyBrewedCode/pymee/commit/29148354189955caa861704fdf1f875752ae6e80))


## v1.5.4 (2022-09-19)

### Fix

* fix: fixed loop parameter in asyncio + tested (#1) ([`1041e56`](https://github.com/FreshlyBrewedCode/pymee/commit/1041e56f066a6a3a9c90b82e4886fdc222db4bb5))


## v1.5.3 (2021-02-08)

### Fix

* fix: implement reconnects iteratively to avoid recursion problems ([`52c2a6b`](https://github.com/FreshlyBrewedCode/pymee/commit/52c2a6b37cd30a9c3c939c110744222187663d1e))

### Style

* style: remove old comments ([`b54e1d7`](https://github.com/FreshlyBrewedCode/pymee/commit/b54e1d703c85005b2d783abf4ae4cccc3be780f8))


## v1.5.2 (2021-02-07)

### Fix

* fix: turn `on_reconnect` callback into coroutine ([`4fded37`](https://github.com/FreshlyBrewedCode/pymee/commit/4fded37bf7502f7e3d95fb9625506f990585e67d))


## v1.5.1 (2021-02-06)

### Fix

* fix: reuse existing node, group and relationship instances after reconnect ([`ead401b`](https://github.com/FreshlyBrewedCode/pymee/commit/ead401b484e30f7030059bda8538f3436d403411))

### Style

* style: reformat code with black ([`daf3e65`](https://github.com/FreshlyBrewedCode/pymee/commit/daf3e6528af5e80257da3e2421e31be56e92b9db))


## v1.5.0 (2021-02-04)

### Feature

* feat: add working reconnection logic during authentication ([`235ea6f`](https://github.com/FreshlyBrewedCode/pymee/commit/235ea6f33b6f87536c486d794e274e4b8a22dfeb))

### Fix

* fix: improve ping handler shutdown ([`5d69574`](https://github.com/FreshlyBrewedCode/pymee/commit/5d695743615ea7cffaf143939afb4b693b692f88))

* fix: fix syntax and logic errors during reconnection ([`b199f85`](https://github.com/FreshlyBrewedCode/pymee/commit/b199f85ad1f76f1bd1fe38033ee3d5c7b06f7dc2))

* fix: handle all exception types during authentication ([`0da9005`](https://github.com/FreshlyBrewedCode/pymee/commit/0da9005bbd6b109c2dacfaec8610236eee1de012))

* fix: remove legacy reconnection logic in `get_access_token` ([`52dd77a`](https://github.com/FreshlyBrewedCode/pymee/commit/52dd77ab38d95f3ed154947926fcd981335873f5))

* fix: fix unclosed client session error during authentication

Move the check of the access token to the top, so no client session is created if the token is still valid. ([`d7b5ca5`](https://github.com/FreshlyBrewedCode/pymee/commit/d7b5ca5b96b6da14e9e34764c233e118135de6b5))


## v1.4.0 (2021-02-03)

### Feature

* feat: enable automatic reconnection attempts ([`ee3fb00`](https://github.com/FreshlyBrewedCode/pymee/commit/ee3fb001067bb3ca90c1221584d1893cc7ebe085))


## v1.3.0 (2021-02-03)

### Documentation

* docs: use large badges in README ([`370006b`](https://github.com/FreshlyBrewedCode/pymee/commit/370006b58fb7a793ba130b8f5998b6c941c41bba))

### Feature

* feat: add manual websocket ping handler ([`773caa0`](https://github.com/FreshlyBrewedCode/pymee/commit/773caa0451d6b9353a1dd97ce8a37ad2e609a127))


## v1.2.0 (2020-11-10)

### Documentation

* docs: mention Home Assistant homee integration in README ([`d44c6b6`](https://github.com/FreshlyBrewedCode/pymee/commit/d44c6b6caa7ee82a76dff387805f5b7e7294b549))

### Feature

* feat: handle `groups`, `nodes`, `group` and `relationship` message types ([`fddac28`](https://github.com/FreshlyBrewedCode/pymee/commit/fddac2831e0185464d2b9991ad04cc52dd28ef5b))

* feat: manage groups, settings and relationships using model ([`5650375`](https://github.com/FreshlyBrewedCode/pymee/commit/56503756a0ccd006aa57b0bebdbee5d6764173b9))

* feat: add `HomeeRelationship` model ([`21f2db0`](https://github.com/FreshlyBrewedCode/pymee/commit/21f2db01267bc917a2af568aa109eafa55bea071))

* feat: add `HomeeOptions` model ([`45efe54`](https://github.com/FreshlyBrewedCode/pymee/commit/45efe54709d2849f56d59fd26d8fb0a2a19f98e4))

* feat: add `HomeeGroup` model ([`9d3759f`](https://github.com/FreshlyBrewedCode/pymee/commit/9d3759fde70dfe8e9beea83e92f5437e90ea183e))

### Fix

* fix: decode strings in `HomeeGroup` ([`9db565e`](https://github.com/FreshlyBrewedCode/pymee/commit/9db565e7268f513d4ffd8b974af5116e3da9e6a7))

### Unknown

* Merge branch &#39;develop&#39; ([`66f19ea`](https://github.com/FreshlyBrewedCode/pymee/commit/66f19ea5765bf2e663c8893da68613213ed98913))


## v1.1.2 (2020-11-01)

### Fix

* fix: fix exception handling bug that causes connection to close instantly ([`050d1d0`](https://github.com/FreshlyBrewedCode/pymee/commit/050d1d04c2b8bca243de1c8d50886ecce580aa67))


## v1.1.1 (2020-11-01)

### Chore

* chore(Git): add homee json dump to gitignore ([`9234d26`](https://github.com/FreshlyBrewedCode/pymee/commit/9234d26a5c4b06f5ccf7f8a8b2fd70ef16929187))

### Documentation

* docs: add link to websockets library in README ([`5f42af6`](https://github.com/FreshlyBrewedCode/pymee/commit/5f42af6367bea667dca275009cda2010e9e4712e))

* docs: update examples in README ([`0177066`](https://github.com/FreshlyBrewedCode/pymee/commit/01770668ecdd43ca364c96d6341f47080fc9ced3))

### Fix

* fix: fix websocket exceptions not getting handled correctly causing websocket to stay open ([`624b383`](https://github.com/FreshlyBrewedCode/pymee/commit/624b383736371d44dfade05fdc803fb6f78c8bcd))


## v1.1.0 (2020-10-24)

### Chore

* chore(Git): ignore local testing script ([`7dd4a11`](https://github.com/FreshlyBrewedCode/pymee/commit/7dd4a11c461b94ab743562bee7f70404fb5804b4))

### Feature

* feat: add `add_on_changed_listener()` to `HomeeNode` to support better update handling ([`12cc3d1`](https://github.com/FreshlyBrewedCode/pymee/commit/12cc3d17ea6aa4cc3354b76f97e1833ac7b029a5))

### Fix

* fix: add error handling to websocket receive and send handlers ([`6e9f021`](https://github.com/FreshlyBrewedCode/pymee/commit/6e9f02191ea2d107563d962a42681d1f18f54c5b))

* fix: change value type in `set_value()` from `int` to `float` ([`0974bac`](https://github.com/FreshlyBrewedCode/pymee/commit/0974bacd8a78b0103d222d7357b502e6fb63e042))

* fix: use module relative imports ([`4f33a6f`](https://github.com/FreshlyBrewedCode/pymee/commit/4f33a6f6ae8cde8ac788e1d9e02a2d4ec0d9b666))


## v1.0.1 (2020-10-23)

### Fix

* fix: bump to v1.0.1 to avoid PyPI conflict ([`573e700`](https://github.com/FreshlyBrewedCode/pymee/commit/573e70054d3711196b3e39d1cc9ba80b4794a13a))


## v1.0.0 (2020-10-23)

### Breaking

* feat: use coroutines for Homee callbacks

BREAKING CHANGE: Homee callbacks need to be awaitable, i.e. async functions. Handleing callbacks in the event loop should provide a better development experience since most functions in the Homee api are async now. ([`99296e6`](https://github.com/FreshlyBrewedCode/pymee/commit/99296e650268467df6370c034d544c10c81530a1))

### Documentation

* docs: add badges ♥ ([`a7e3a28`](https://github.com/FreshlyBrewedCode/pymee/commit/a7e3a28e7d6d8116c893214cd6e6b24ed5758c0f))

### Feature

* feat: add utility methods for getting nodes and atributes by id ([`f43014c`](https://github.com/FreshlyBrewedCode/pymee/commit/f43014cb77da7a4059695663a093a4acfb3b5d02))

* feat: support updating/adding nodes after receiving a &#39;nodes&#39; message ([`535602b`](https://github.com/FreshlyBrewedCode/pymee/commit/535602b8b43696b29f0e1e9d86bcde9e40223dbb))

* feat: provide async disconnected event

`await Homee.wait_until_disconnected()` can now be used to wait until the connection has been closed. ([`c019ef5`](https://github.com/FreshlyBrewedCode/pymee/commit/c019ef5d55306007f98ee2d0154ccee138d2cb25))

* feat: port to websockets package ([`1b578bc`](https://github.com/FreshlyBrewedCode/pymee/commit/1b578bc166cc0d9c6238980aca1a889a2e8ddef2))

### Unknown

* Merge branch &#39;develop&#39; ([`858ddc2`](https://github.com/FreshlyBrewedCode/pymee/commit/858ddc22573eea4ae6b6ac9b1fa746641ae80607))


## v0.2.0 (2020-10-23)

### Chore

* chore(CI): add version variable to config ([`c34632a`](https://github.com/FreshlyBrewedCode/pymee/commit/c34632a72673f5e32ffefd9538e2dd0190f406ac))

* chore(CI): add workflow for semantic release ([`c174217`](https://github.com/FreshlyBrewedCode/pymee/commit/c1742178ecaefb85dab5487d098159c10f872614))

### Documentation

* docs: add install instructions and bump version ([`f0208a5`](https://github.com/FreshlyBrewedCode/pymee/commit/f0208a565523e63ff0ecf976c5288ffc0d4fc71a))

### Feature

* feat: raise unique exceptions while acquiring access token ([`edac67b`](https://github.com/FreshlyBrewedCode/pymee/commit/edac67bad668349ced6d96f8306836f884d05937))


## v0.0.1 (2020-10-21)

### Chore

* chore: adjust package structure for PyPi release ([`ac0368f`](https://github.com/FreshlyBrewedCode/pymee/commit/ac0368fd239c39f18ada3667ecbfe2f65c9f196d))

* chore: add LICENSE ([`d0ce035`](https://github.com/FreshlyBrewedCode/pymee/commit/d0ce035df70cce12e18b17fc02e3fffa649ea7e7))

### Documentation

* docs: add README ([`8701f0a`](https://github.com/FreshlyBrewedCode/pymee/commit/8701f0ad47120d8291eb5b4f4c441cc151c468b2))

### Refactor

* refactor: remove unused import in model.py ([`695b1f2`](https://github.com/FreshlyBrewedCode/pymee/commit/695b1f2d817ac55a07b4e410953748402f83f8f1))

### Unknown

* initial commit ([`67eb054`](https://github.com/FreshlyBrewedCode/pymee/commit/67eb054f67326b3d60bb04acb30397d1c5c13bfb))
