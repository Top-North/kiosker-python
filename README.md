# Python wrapper for Kiosker API
Python wrapper for Kiosker API-integration.

---

### Installation

```shell
pip3 install kiosker-python
```

---

### Setup

```python
from kiosker.api import KioskerAPI
api = KioskerAPI('10.0.1.100', 'token')
```

---

### Functions

#### Get Status
```python
status = api.status()

print('Status:')
print(f'Device ID: {status.device_id}')
print(f'Model: {status.model}')
print(f'OS version: {status.os_version}')
print(f'Battery level: {status.battery_level}%')
print(f'Battery state: {status.battery_state}')
print(f'Last interaction: {status.last_interaction}')
print(f'Last motion: {status.last_motion}')
print(f'Last status update: {status.last_update}')
print(f'Screensaver pause: {status.screensaver_pause}')
```
**Description**: Retrieves the current status of the kiosk.

#### Ping the API
```python
result = api.ping()
print(f"Ping successful: {result}")
```
**Description**: Checks if the API is reachable. Returns `True` if successful, otherwise raises an error.

#### Navigate to a URL
```python
result = api.navigate_url('https://example.com')
print(f"Navigation result: {result}")
```
**Description**: Navigates the kiosk to the specified URL.

#### Refresh the Page
```python
result = api.navigate_refresh()
print(f"Refresh result: {result}")
```
**Description**: Refreshes the current page on the kiosk.

#### Navigate Home
```python
result = api.navigate_home()
print(f"Home navigation result: {result}")
```
**Description**: Navigates the kiosk to the home page.

#### Navigate Forward
```python
result = api.navigate_forward()
print(f"Navigate forward result: {result}")
```
**Description**: Navigates forward in the browser's history.

#### Navigate Backward
```python
result = api.navigate_backward()
print(f"Navigate backward result: {result}")
```
**Description**: Navigates backward in the browser's history.

#### Print
```python
result = api.print()
print(f"Print result: {result}")
```
**Description**: Sends a print command to the kiosk.

#### Clear Cookies
```python
result = api.clear_cookies()
print(f"Cookies cleared: {result}")
```
**Description**: Clears all cookies stored on the kiosk.

#### Clear Cache
```python
result = api.clear_cache()
print(f"Cache cleared: {result}")
```
**Description**: Clears the cache on the kiosk.

#### Interact with Screensaver
```python
result = api.screensaver_interact()
print(f"Screensaver interaction result: {result}")
```
**Description**: Simulates user interaction with the screensaver to prevent it from activating.

#### Set Screensaver State
```python
result = api.screensaver_set_state(disabled=True)
print(f"Screensaver disabled: {result}")
```
**Description**: Enables or disables the screensaver.

#### Get Screensaver State
```python
state = api.screensaver_get_state()
print(f"Screensaver state: {state}")
```
**Description**: Retrieves the current state of the screensaver (enabled or disabled).

#### Set Blackout
```python
from kiosker.data import Blackout

blackout = Blackout(
    visible=True,
    text="Maintenance in progress",
    background="#000000",
    foreground="#FFFFFF",
    icon="warning",
    expire=60
)
result = api.blackout_set(blackout)
print(f"Blackout set: {result}")
```
**Description**: Sets a blackout screen with customizable text, colors, and expiration time.

#### Get Blackout State
```python
blackout_state = api.blackout_get()
print(f"Blackout state: {blackout_state}")
```
**Description**: Retrieves the current state of the blackout screen.

#### Clear Blackout
```python
result = api.blackout_clear()
print(f"Blackout cleared: {result}")
```
**Description**: Clears the blackout screen.

---

### Objects

#### `Status`
Represents the current status of the kiosk.

**Attributes**:
- `battery_level` (int): Battery percentage.
- `battery_state` (str): Current battery state (e.g., charging, discharging).
- `model` (str): Device model.
- `os_version` (str): Operating system version.
- `last_interaction` (datetime): Timestamp of the last user interaction.
- `last_motion` (Optional[datetime]): Timestamp of the last detected motion.
- `last_update` (datetime): Timestamp of the last status update.
- `device_id` (str): Unique identifier for the device.
- `screensaver_pause` (Optional[bool]): Whether the screensaver is paused.

#### `Result`
Represents the result of an API operation.

**Attributes**:
- `error` (bool): Indicates if an error occurred.
- `reason` (Optional[str]): Reason for the error, if any.
- `function` (Optional[str]): Name of the function that caused the error.

#### `Blackout`
Represents a blackout screen configuration.

**Attributes**:
- `visible` (bool): Whether the blackout screen is visible.
- `text` (Optional[str]): Text to display on the blackout screen.
- `background` (str): Background color in hex format.
- `foreground` (str): Foreground color in hex format.
- `icon` (Optional[str]): Icon to display on the blackout screen.
- `expire` (int): Time in seconds before the blackout screen expires.

---

### Development
1. Clone the project

2. Create a virtual environment
```shell
python3 -m venv venv
```

3. Activate the virtual environment
```shell
source venv/bin/activate
```

4. Install dependencies
```shell
pip install wheel
pip install setuptools
pip install twine
```

5. Run tests
```shell
HOST="" TOKEN="" pytest -s
```

6. Build the library
```shell
python setup.py bdist_wheel
```

---

### API Documentation
- [Docs](https://docs.kiosker.io/#/api)
- [Definition](https://swagger.kiosker.io)

---

### Get Kiosker for iOS on the App Store
- [Kiosker](https://apps.apple.com/us/app/kiosker-fullscreen-web-kiosk/id1481691530?uo=4&at=11l6hc&ct=fnd)
- [Kiosker Pro](https://apps.apple.com/us/app/kiosker-pro-web-kiosk/id1446738885?uo=4&at=11l6hc&ct=fnd)