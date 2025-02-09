from kiosker.api import KioskerAPI, Blackout
import time
import os

host = os.environ["HOST"]
token = os.environ["TOKEN"]

def test_status():
    
    api = KioskerAPI(host, token)

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

    assert api.ping() == True
    
    
def test_blackout():
    
    api = KioskerAPI(host, token)
    
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
    
    time.sleep(10)
    
    print(f'Blackout state: {api.blackout_get()}')