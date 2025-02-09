import httpx
from .data import Status, Result, Blackout

API_PATH = '/api/v1'

class KioskerAPI:
    def __init__(self, host, token, port=8081, ssl=False):
        if ssl:
            self.conf_host = f'https://{host}:{port}'
        else:
            self.conf_host = f'http://{host}:{port}'

        self.conf_headers = {'accept': 'application/json',
                             'Authorization': f'Bearer {token}'}
        
    def _get(self, path: str):
        r = httpx.get(f'{self.conf_host}{API_PATH}{path}', headers=self.conf_headers)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            raise RuntimeError("Unauthorized")
        elif r.status_code == 403:
            raise RuntimeError("IP not allowed")
        else:
            r.raise_for_status()
            
    def _post(self, path: str, json={}):
        r = httpx.post(f'{self.conf_host}{API_PATH}{path}', headers=self.conf_headers, json=json)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            raise RuntimeError("Unauthorized")
        elif r.status_code == 403:
            raise RuntimeError("IP not allowed")
        elif r.status_code == 400:
            print(r.json())
            raise RuntimeError("Bad request")
        else:
            r.raise_for_status()

    def status(self):
        status_data = self._get('/status').get('status')
        return Status(status_data)

    def ping(self):
        response_json = self._get('/ping')
        if response_json.get('error') == False:
            return True
        else:
            raise RuntimeError("Ping error: {}".format(response_json))
    
    # Navigation
    def navigate_home(self):
        return Result(self._post('/navigate/home'))
    
    def navigate_refresh(self):
        return Result(self._post('/navigate/refresh'))
    
    def navigate_forward(self):
        return Result(self._post('/navigate/forward'))
    
    def navigate_backward(self):
        return Result(self._post('/navigate/backward'))
    
    def navigate_url(self, url: str):
        return Result(self._post('/navigate/url', json={'url': url}))
    
    # Print
    def print(self):
        return Result(self._post('/print'))
    
    # Clear
    def clear_cookies(self):
        return Result(self._post('/clear/cookies'))
    
    def clear_cache(self):
        return Result(self._post('/clear/cache'))
    
    # Screensaver
    def screensaver_interact(self):
        return Result(self._post('/screensaver/interact'))
    
    def screensaver_set_state(self, disabled: bool):
        return Result(self._post('/screensaver/state', json={'disabled': disabled}))
    
    def screensaver_get_state(self):
        return self.status().screensaver_pause
    
    # Blackout
    def blackout_set(self, object: Blackout):
        return Result(self._post('/blackout', json=object.to_dict()))
    
    def blackout_get(self):
        blackout_data = self._get('/blackout/state').get('blackOut')
        if blackout_data is None:
            return None
        return Blackout.from_dict(blackout_data)
    
    def blackout_clear(self):
        return Result(self._post('/blackout', json={'visible': False}))