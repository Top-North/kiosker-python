# Python wrapper for Kiosker API
Python wrapper for Kiosker integration.

### Installation

```shell
pip3 install kiosker-python
```

### Setup

```python
from kiosker.api import KioskerAPI
api = KioskerAPI('10.0.1.100', 'token')
```

### Functions

#### Get status

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

### Objects

### Development
1. Create a virtual environment
```bash
python3 -m venv venv
```

2. Activate the virtual environment
```bash
source venv/bin/activate
```

3. Install dependecies
```bash
pip install wheel
pip install setuptools
pip install twine
```

4. Run test
```bash
HOST="" TOKEN="" pytest -s
```


### API Documentation
[Docs](https://docs.kiosker.io/#/api)
[Definition](https://swagger.kiosker.io)

### Get Kiosker for iOS on the App Store
[Kiosker](https://apps.apple.com/us/app/kiosker-fullscreen-web-kiosk/id1481691530?uo=4&at=11l6hc&ct=fnd)
[Kiosker Pro](https://apps.apple.com/us/app/kiosker-pro-web-kiosk/id1446738885?uo=4&at=11l6hc&ct=fnd)