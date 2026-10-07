from kiosker import KioskerAPI, Blackout, NotFoundError
import pytest
import random
import time
import os

def env_flag(name):
    return os.environ.get(name, "false").lower() in ("true", "1", "yes", "on")

host = os.environ["HOST"]
token = os.environ["TOKEN"]
ssl = env_flag("SSL")
verify = env_flag("VERIFY")

api = KioskerAPI(host, token, ssl=ssl, verify=verify)

def test_ping():

    result = api.ping()
    
    print(f'Ping: {result}')
    assert result == True

def test_status():
    
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
    print(f'Last status update: {status.last_update}')
    print(f'App name: {status.app_name}')
    print(f'App version: {status.app_version}')
    print(f'App start: {status.app_start}')
    

    assert api.ping() == True

def test_navigate():
    
    print('Navigating to URL...')
    result = api.navigate_url('https://google.com')
    print(f'Navigate URL: {result}')
    
    time.sleep(5)

    print('Navigating to refresh...')
    result = api.navigate_refresh()
    print(f'Navigate refresh: {result}')

    time.sleep(5)
    
    print('Navigating to home...')
    result = api.navigate_home()
    print(f'Navigate home: {result}')

    time.sleep(5)

    print('Navigating to backward...')
    result = api.navigate_backward()
    print(f'Navigate backward: {result}')
    
    time.sleep(5)
    
    print('Navigating to forward...')
    result = api.navigate_forward()
    print(f'Navigate forward: {result}')

    time.sleep(5)

def test_print():
    
    print('Printing...')
    result = api.print()
    print(f'Print: {result}')

    time.sleep(10)
    
def test_clear():
    
    print('Clearing cookies...')
    result = api.clear_cookies()
    print(f'Clear cookies: {result}')

    time.sleep(5)
    
    print('Clearing cache...')
    result = api.clear_cache()
    print(f'Clear cache: {result}')

    time.sleep(5)

    print('Clearing history...')
    result = api.clear_history()
    print(f'Clear history: {result}')

    time.sleep(5)

def test_screensaver():
    
    print('Interacting with screensaver...')
    result = api.screensaver_interact()
    print(f'Screensaver interact: {result}')

    time.sleep(5)
    
    print('Getting screensaver state...')
    state = api.screensaver_get_state()
    print(f'Screensaver state: {state}')
    
    time.sleep(5)
    
    print('Setting screensaver state to disabled...')
    result = api.screensaver_set_disabled_state(disabled=True)
    print(f'Screensaver set state: {result}')

    time.sleep(5)
    
    print('Getting screensaver state...')
    state = api.screensaver_get_state()
    print(f'Screensaver state: {state}')
    
    time.sleep(5)
    
    print('Setting screensaver state to enabled...')
    result = api.screensaver_set_disabled_state(disabled=False)
    print(f'Screensaver set state: {result}')
    
    time.sleep(5)
    
    print('Getting screensaver state...')
    state = api.screensaver_get_state()
    print(f'Screensaver state: {state}')
        
def test_blackout():
        
    print(f'Blackout state: {api.blackout_get()}')
    
    api.blackout_set(Blackout(visible=True, text='This is a test from Python that should clear', background='#000000', foreground='#FFFFFF', icon='ladybug', expire=20))
    
    time.sleep(5)
    
    print(f'Blackout state: {api.blackout_get()}')
    
    api.blackout_clear()
    
    time.sleep(5)
    
    print(f'Blackout state: {api.blackout_get()}')
    
    time.sleep(1)
    
    api.blackout_set(Blackout(visible=True, text='This is a test from Python', background='#000000', foreground='#FFFFFF', icon='ladybug', expire=20))

    time.sleep(5)
    
    api.blackout_set(Blackout(visible=True, text='This is a change from Python', background='#000000', foreground='#FFFFFF', icon='ladybug', expire=5))

    print(f'Blackout state: {api.blackout_get()}')
    
    time.sleep(7)
    
    print(f'Blackout state: {api.blackout_get()}')
    
    api.blackout_set(Blackout(visible=True, text='This is a test from Python that is dismissible', background='#000000', foreground='#FFFFFF', icon='hand.point.up', expire=25, dismissible=True, buttonBackground='#FA0000', buttonForeground='#FFFFFF', buttonText='Hide me then...', sound="1003"))
    
    time.sleep(5)

def test_asam():

    state = api.asam_get_state()
    print(f'ASAM state: {state}')

def test_printer():

    printer = api.printer_default_get()
    print(f'Default printer: {printer}')

    printers = api.printers_list()
    print(f'Printers: {printers}')

def test_settings():

    settings = api.settings_get()
    print(f'Settings keys: {list(settings.keys())}')

    assert isinstance(settings, dict)

def test_client_certificates():

    certificates = api.client_certificates_list()
    for certificate in certificates:
        print(f'Certificate: {certificate.id} {certificate.fingerprint} {certificate.hosts} {certificate.metadata.subject_name}')

# Opt-in tests that change the device. Enable with SETTINGS=true, PRINTER=true, or CLIENT_CERTS=true.

@pytest.mark.skipif(not env_flag("SETTINGS"), reason="Set SETTINGS=true to run (changes the start page url)")
def test_settings_set():

    url = 'https://example.com'

    print(f'Setting url to {url}...')
    result = api.settings_set({'url': url})
    print(f'Settings set: {result}')
    assert result.error is False

    time.sleep(3)

    settings = api.settings_get()
    print(f'Settings url: {settings.get("url")}')
    assert settings.get('url') == url

@pytest.mark.skipif(not env_flag("PRINTER"), reason="Set PRINTER=true to run (changes the default printer)")
def test_printer_set():

    printers = api.printers_list()
    print(f'Printers: {printers}')
    if not printers:
        pytest.skip('No printers available')

    printer = random.choice(printers)
    print(f'Setting default printer to {printer}...')
    result = api.printer_default_set(printer)
    print(f'Printer set: {result}')
    assert result.error is False

    default_printer = api.printer_default_get()
    print(f'Default printer: {default_printer}')
    assert default_printer.name == printer.name
    assert default_printer.url == printer.url

# Public test client certificate from https://badssl.com, not a secret.
BADSSL_P12_PASSWORD = 'badssl.com'
BADSSL_P12_BASE64 = (
    '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'
)

@pytest.mark.skipif(not env_flag("CLIENT_CERTS"), reason="Set CLIENT_CERTS=true to run (adds and removes a test client certificate)")
def test_client_certificate_lifecycle():

    print('Adding client certificate for badssl.com...')
    result = api.client_certificate_add(BADSSL_P12_BASE64, BADSSL_P12_PASSWORD, hosts=['badssl.com'])
    print(f'Certificate added: {result}')
    assert result.error is False

    cert = None
    try:
        certificates = api.client_certificates_list()
        cert = next((c for c in certificates if c.hosts == ['badssl.com']), None)
        print(f'Added certificate: {cert}')
        assert cert is not None
        assert cert.id
        assert cert.fingerprint

        print('Setting hosts to example.com...')
        result = api.client_certificate_set_hosts(['example.com'], id=cert.id)
        print(f'Hosts set: {result}')
        assert result.error is False

        certificates = api.client_certificates_list()
        updated = next((c for c in certificates if c.id == cert.id), None)
        print(f'Updated certificate: {updated}')
        assert updated is not None
        assert updated.hosts == ['example.com']

        print('Deleting certificate by fingerprint...')
        result = api.client_certificate_delete(fingerprint=cert.fingerprint)
        print(f'Certificate deleted: {result}')
        assert result.error is False

        certificates = api.client_certificates_list()
        assert all(c.id != cert.id for c in certificates)
    finally:
        # Clean up if an assertion failed before the certificate was deleted
        if cert is not None:
            try:
                api.client_certificate_delete(id=cert.id)
            except NotFoundError:
                pass
