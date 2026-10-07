# Python wrapper for Kiosker API

This Python library provides a comprehensive wrapper for the Kiosker API, enabling developers to programmatically control and manage Kiosker devices. Kiosker is a professional web kiosk application for iOS that transforms iPads into secure, full-screen web browsers perfect for public displays, interactive kiosks, and digital signage solutions.

The kiosker-python-api package allows you to:
- **Remote Control**: Navigate web pages, refresh content, and control browser functions
- **Device Management**: Monitor device status, battery levels, and system information
- **Content Control**: Manage blackout screens for maintenance or emergency messaging
- **Screen Management**: Control screensaver behavior and Guided Access (Autonomous Single App Mode)
- **Configuration**: Read and update the kiosk settings
- **Printing**: Discover printers and set the default printer for silent printing
- **Client Certificates**: Manage certificates for mutual TLS when browsing
- **System Maintenance**: Clear cookies, cache, and browsing history
- **Network Discovery**: Automatically discover Kiosker devices on your network using ZeroConf

Whether you're managing a single kiosk or deploying a fleet of devices across multiple locations, this library provides the tools needed to integrate Kiosker devices into your existing infrastructure and workflows.

---

### Installation

```shell
pip install kiosker-python-api
```

---

### Setup

```python
KioskerAPI(host, token, port = 8081, ssl = False, verify = False)
```

```python
from kiosker import KioskerAPI
from kiosker import Status, Result, Blackout, ScreensaverState, ASAMState, Printer, Certificate
api = KioskerAPI('10.0.1.100', 'token')
```

#### Constructor Parameters

- **host** (str): IP address or hostname of the Kiosker device
- **token** (str): Authentication token for API access
- **port** (int, optional): Port number (default: 8081)
- **ssl** (bool, optional): Use HTTPS instead of HTTP (default: False)
- **verify** (bool | ssl.SSLContext, optional): TLS certificate verification. `False` accepts any certificate, such as a self-signed one (default), `True` uses the system CA store, or pass an `ssl.SSLContext` to trust a specific certificate

---

### Device Discovery with ZeroConf

Kiosker devices advertise themselves on the local network using ZeroConf (Bonjour/mDNS) autodiscovery. This allows you to automatically discover Kiosker devices without needing to know their IP addresses beforehand.

#### Service Information

Kiosker devices broadcast the following service:
- **Service Type**: `_kiosker._tcp`
- **TXT Records**:
  - `version`: App version (e.g., "25.1.0 (230)")
  - `app`: App name (e.g., "Kiosker Pro")
  - `uuid`: Unique device identifier (e.g., "2904C1F2-93FB-4954-BF85-FAAEFBA814F6")
  - `ssl`: Whether the API uses TLS ("true" or "false")
  - `platform`: Device platform (e.g., "iOS")

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
print(f'Ambient light: {status.ambient_light}')
print(f'App name: {status.app_name}')
print(f'App version: {status.app_version}')
print(f'Last status update: {status.last_update}')
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
**Description**: Prints the current page. Prints silently to the default printer if silent printing is enabled in the app, otherwise the print dialog is shown on the device.

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
**Description**: Clears the web cache and website data on the kiosk.

#### Clear History
```python
result = api.clear_history()
print(f"History cleared: {result}")
```
**Description**: Clears the browsing history on the kiosk.

#### Interact with Screensaver
```python
result = api.screensaver_interact()
print(f"Screensaver interaction result: {result}")
```
**Description**: Simulates a user interaction, hiding the screensaver if it's visible. Unlike a real touch, it doesn't reset the idle timer or the browsing time limit.

#### Set Screensaver State
```python
result = api.screensaver_set_disabled_state(disabled=True)
print(f"Screensaver disabled: {result}")
```
**Description**: Disables (`True`) or enables (`False`) the screensaver. While disabled through the API, the screensaver won't appear.

#### Get Screensaver State
```python
state = api.screensaver_get_state()
print(f"Screensaver state: {state}")
```
**Description**: Retrieves whether the screensaver is disabled through the API and whether it's currently visible.

#### Set Blackout
```python
from kiosker import Blackout

blackout = Blackout(
    visible=True,                   # Required: show blackout screen
    text="Maintenance in progress", # Optional: text to display
    background="#000000",           # Optional: background color (hex)
    foreground="#FFFFFF",           # Optional: foreground/text color (hex)
    icon="warning",                 # Optional: icon name (SF Symbol)
    expire=60,                      # Optional: time in seconds before blackout expires
    dismissible=True,               # Optional: allow user to dismiss blackout with a button
    buttonBackground="#FF0000",     # Optional: button background color (hex)
    buttonForeground="#FFFFFF",     # Optional: button text color (hex)
    buttonText="OK",                # Optional: button label
    sound="1003"                    # Optional: sound to play (SystemSoundID)
)
result = api.blackout_set(blackout)
print(f"Blackout set: {result}")
```
**Description**: Sets a blackout screen with customizable text, colors, expiration time, and optional button/sound options.

#### Get Blackout State
```python
blackout_state = api.blackout_get()
print(f"Blackout state: {blackout_state}")
```
**Description**: Retrieves the active blackout, with `expire` as the remaining seconds, or `None` if no blackout is set.

#### Clear Blackout
```python
result = api.blackout_clear()
print(f"Blackout cleared: {result}")
```
**Description**: Clears the blackout screen.

#### Get Guided Access State
```python
state = api.asam_get_state()
print(f"Guided Access enabled: {state.enabled}")
```
**Description**: Retrieves whether Guided Access (Autonomous Single App Mode) is enabled.

#### Set Guided Access State
```python
result = api.asam_set_enabled_state(enabled=True)
print(f"Guided Access set: {result}")
```
**Description**: Enables or disables Guided Access (Autonomous Single App Mode). The device must be supervised and allow Kiosker to use Autonomous Single App Mode. The call returns before iOS applies the change, so use `asam_get_state()` to verify.

#### Get Settings
```python
settings = api.settings_get()
print(f"Start page: {settings['url']}")
```
**Description**: Retrieves the full settings object as a dictionary. The settings contain sensitive values, so use TLS.

#### Update Settings
```python
result = api.settings_set({'url': 'https://example.com', 'disableScreenSleep': True})
print(f"Settings updated: {result}")
```
**Description**: Merges the given keys into the current settings. Keys you leave out keep their current value. Protected API and MDM keys (eg. `apiActive`) are skipped and listed in `result.reason`. Raises `ConflictError` if the settings are managed by MDM.

#### Clear Settings
```python
result = api.settings_clear()
print(f"Settings cleared: {result}")
```
**Description**: Resets all settings to default. **Warning**: the defaults disable the API, so the device stops responding to API calls afterwards. Raises `ConflictError` if the settings are managed by MDM.

#### Get Default Printer
```python
printer = api.printer_default_get()
print(f"Default printer: {printer.name} ({printer.url})")
```
**Description**: Retrieves the default printer used for silent printing. `name` and `url` are `None` if no printer is set.

#### Set Default Printer
```python
from kiosker import Printer

result = api.printer_default_set(Printer(name='Office Printer', url='ipp://192.168.1.50:631/ipp/print'))
print(f"Default printer set: {result}")
```
**Description**: Sets the default printer. Both name and url are required.

#### List Printers
```python
printers = api.printers_list()
for printer in printers:
    print(f"{printer.name}: {printer.url}")
```
**Description**: Discovers AirPrint printers on the local network. Takes about 5 seconds.

#### List Client Certificates
```python
certificates = api.client_certificates_list()
for certificate in certificates:
    print(f"{certificate.id} {certificate.fingerprint} {certificate.hosts} {certificate.metadata.subject_name}")
```
**Description**: Lists the client certificates added on the device or through the API. Certificates provided by MDM aren't listed.

#### Add Client Certificate
```python
import base64

with open('client.p12', 'rb') as f:
    data = base64.b64encode(f.read()).decode()

result = api.client_certificate_add(base64=data, password='secret', hosts=['example.com'])
print(f"Certificate added: {result}")
```
**Description**: Adds a PKCS#12 (.p12) client certificate for mutual TLS. Leave out `hosts` to make it the default certificate. Raises `BadRequestError` if the data or password is wrong or a host is already used, and `ConflictError` if certificates are managed by MDM.

#### Set Client Certificate Hosts
```python
result = api.client_certificate_set_hosts(['example.com', 'example.org'], id='A1D89309-F004-40E2-B8DE-A9EC00FA112B')
print(f"Hosts updated: {result}")
```
**Description**: Replaces the hosts of a certificate, referenced by `id` or `fingerprint`. An empty list makes it the default certificate. Raises `NotFoundError` if the certificate doesn't exist.

#### Delete Client Certificate
```python
result = api.client_certificate_delete(fingerprint='3f1c2a9b8e7d...')
print(f"Certificate deleted: {result}")
```
**Description**: Deletes a certificate by `id` or `fingerprint`. Raises `NotFoundError` if the certificate doesn't exist.

---

### Objects

#### `Status`
Represents the current status of the kiosk.

**Attributes**:
- `battery_level` (int): Battery level in percent. 0 if the level is unknown.
- `battery_state` (str): "Unknown", "Not Charging", "Charging", or "Fully Charged".
- `model` (str): Device model, e.g. "iPad".
- `os_version` (str): Operating system name and version, e.g. "iPadOS 26.2".
- `app_name` (str): App name, e.g. "Kiosker Pro".
- `app_version` (str): App version and build, e.g. "26.9.1 (287)".
- `last_interaction` (datetime): Time of the last user interaction.
- `last_motion` (Optional[datetime]): Time of the last detected motion, or `None` if no motion has been detected or motion detection is off.
- `ambient_light` (Optional[float]): Unitless ambient light level from the camera, or `None` if the camera sensor is disabled.
- `last_update` (datetime): The device's clock when the status was created.
- `device_id` (str): Unique identifier for the device.
- `app_start` (Optional[datetime]): Time the app was started, or `None` if unknown (e.g. on older app versions).

#### `Result`
Represents the result of an API operation.

**Attributes**:
- `error` (bool): `True` if the operation failed.
- `reason` (Optional[str]): Error description when `error` is `True`. Can also carry information on success, e.g. `settings_set()` lists skipped protected keys here.
- `function` (Optional[str]): The API function that was called, e.g. "navigate/url".

#### `Blackout`
Represents a blackout screen configuration.

Field names are camelCase to match the API. Only `visible` is required; leaving out the rest gives a black screen that expires after 24 hours.

**Attributes**:
- `visible` (bool): `True` to show the blackout, `False` to remove it.
- `background` (Optional[str]): Background color in hex format.
- `foreground` (Optional[str]): Foreground/text color in hex format.
- `expire` (Optional[int]): When setting, seconds until the blackout expires (default 86400). When read with `blackout_get()`, the remaining seconds, which can be a decimal.
- `text` (Optional[str]): Text to display on the blackout screen.
- `icon` (Optional[str]): SF Symbol name shown above the text, e.g. "wrench.and.screwdriver.fill".
- `dismissible` (Optional[bool]): Allow user to dismiss blackout with a button.
- `buttonBackground` (Optional[str]): Button background color (hex).
- `buttonForeground` (Optional[str]): Button text color (hex).
- `buttonText` (Optional[str]): Button label.
- `sound` (Optional[str]): Sound to play (SystemSoundID).

#### `ScreensaverState`
Represents the state of the screensaver.

**Attributes**:
- `visible` (bool): Whether the screensaver is currently shown. Can be `None` if the state is unknown.
- `disabled` (bool): Whether the screensaver is disabled through the API (`screensaver_set_disabled_state()`). The screensaver schedule configured in the app isn't reflected here.

#### `ASAMState`
Represents the Guided Access (Autonomous Single App Mode) state.

**Attributes**:
- `enabled` (bool): Whether Guided Access is enabled and the device is locked to Kiosker.

#### `Printer`
Represents a printer.

**Attributes**:
- `name` (Optional[str]): Printer display name.
- `url` (Optional[str]): Printer URL, eg. `ipp://192.168.1.50:631/ipp/print`.

#### `Certificate`
Represents a client certificate.

**Attributes**:
- `id` (str): Certificate identifier.
- `fingerprint` (Optional[str]): SHA-256 fingerprint of the certificate as lowercase hex.
- `hosts` (list[str]): Hosts the certificate is used for. Empty for the default certificate.
- `metadata` (`CertificateMetadata`): Subject, issuer, and validity details.
- `password` (Optional[str]): Always `None` when listing; the password is never returned by the API.
- `base64` (Optional[str]): Always `None` when listing; the certificate data is never returned by the API.

#### `CertificateMetadata`
Subject, issuer, and validity details of a client certificate. All fields are `None` if the certificate doesn't contain them.

**Attributes**:
- `subject_name`, `issuer_name` (Optional[str]): Common name (CN).
- `subject_organization`, `issuer_organization` (Optional[str]): Organization (O).
- `subject_location`, `issuer_location` (Optional[str]): Locality (L).
- `subject_state`, `issuer_state` (Optional[str]): State or province (ST).
- `subject_country`, `issuer_country` (Optional[str]): Country (C).
- `not_valid_before`, `not_valid_after` (Optional[datetime]): Validity period.

---

### Exception Handling

The kiosker-python-api defines custom exceptions to provide clear error handling for different failure scenarios:

#### Exception Hierarchy

All custom exceptions inherit from the base `KioskerException` class:

```python
from kiosker.exceptions import (
    KioskerException,
    ConnectionError,
    AuthenticationError,
    IPAuthenticationError,
    TLSVerificationError,
    BadRequestError,
    NotFoundError,
    ConflictError,
    PingError
)
```

#### Exception Types

- **`KioskerException`**: Base exception for all Kiosker API errors
- **`ConnectionError`**: Raised when connection to the Kiosker device fails
- **`AuthenticationError`**: Raised when authentication fails
- **`IPAuthenticationError`**: Raised when IP-list authentication fails
- **`TLSVerificationError`**: Raised when TLS verification fails
- **`BadRequestError`**: Raised when the request is invalid
- **`NotFoundError`**: Raised when the referenced object (eg. a client certificate) doesn't exist
- **`ConflictError`**: Raised when the operation is blocked because the setting is managed by MDM
- **`PingError`**: Raised when ping operation fails

#### Usage Example

```python
from kiosker import KioskerAPI
from kiosker.exceptions import ConnectionError, AuthenticationError

try:
    api = KioskerAPI('10.0.1.100', 'invalid_token')
    result = api.ping()
except ConnectionError:
    print("Could not connect to the Kiosker device")
except AuthenticationError:
    print("Authentication failed - check your token")
except KioskerException as e:
    print(f"Kiosker API error: {e}")
```

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
pip install build wheel setuptools twine pytest httpx
```

5. Run tests against a device. Set `SSL=true` to use HTTPS and `VERIFY=true` to verify its certificate.
```shell
HOST="0.0.0.0" TOKEN="" pytest -s
```
Tests that change the device are skipped unless enabled:
- `SETTINGS=true`: sets the start page url to `https://example.com`.
- `PRINTER=true`: sets a random discovered printer as the default printer.
- `CLIENT_CERTS=true`: adds, updates, and removes the public badssl.com test client certificate.
```shell
HOST="0.0.0.0" TOKEN="" SETTINGS=true PRINTER=true CLIENT_CERTS=true pytest -s
```

6. Build the library
```shell
python -m build
```

7. Install as local development dependency
```shell
uv pip install -e /path/to/kiosker-python
```

8. Upload to test
```shell
twine upload --repository testpypi dist/*
```

9. Upload to prod
```shell
twine upload dist/*
```

---

### API Documentation
- [Docs](https://docs.kiosker.io/#/api)
- [Definition](https://swagger.kiosker.io)

---

### Get Kiosker for iOS on the App Store
- [Kiosker](https://apps.apple.com/us/app/kiosker-fullscreen-web-kiosk/id1481691530?uo=4&at=11l6hc&ct=fnd)
- [Kiosker Pro](https://apps.apple.com/us/app/kiosker-pro-web-kiosk/id1446738885?uo=4&at=11l6hc&ct=fnd)