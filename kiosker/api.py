import ssl
import httpx
from .data import Status, Result, Blackout, ScreensaverState
from .exceptions import ConnectionError, TLSVerificationFailed, InvalidResponseError, AuthenticationError, IPAuthenticationFailed, BadRequestError, PingError

API_PATH = '/api/v1'

class KioskerAPI:
    def __init__(self, host, token, port=8081, ssl=False, verify: bool | ssl.SSLContext =False):
        if ssl:
            self.conf_host = f'https://{host}:{port}'
        else:
            self.conf_host = f'http://{host}:{port}'

        self.conf_headers = {'accept': 'application/json',
                             'Authorization': f'Bearer {token}'}
        
        self.verify = verify
        
    def _get(self, path: str):
        try:
            r = httpx.get(f'{self.conf_host}{API_PATH}{path}', headers=self.conf_headers, verify=self.verify)
        except httpx.ConnectError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e) or "SSL" in str(e):
                raise TLSVerificationFailed(f"TLS verification failed: {e}")
            raise ConnectionError(f"Connection failed: {e}")
        except (httpx.TimeoutException, httpx.NetworkError) as e:
            raise ConnectionError(f"Connection failed: {e}")
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            raise AuthenticationError("Unauthorized")
        elif r.status_code == 403:
            raise IPAuthenticationFailed("IP not allowed")
        else:
            r.raise_for_status()
            
    def _post(self, path: str, json=None):
        if json is None:
            json = {}
        try:
            r = httpx.post(f'{self.conf_host}{API_PATH}{path}', headers=self.conf_headers, json=json, verify=self.verify)
        except httpx.ConnectError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e) or "SSL" in str(e):
                raise TLSVerificationFailed(f"TLS verification failed: {e}")
            raise ConnectionError(f"Connection failed: {e}")
        except (httpx.TimeoutException, httpx.NetworkError) as e:
            raise ConnectionError(f"Connection failed: {e}")
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            raise AuthenticationError("Unauthorized")
        elif r.status_code == 403:
            raise IPAuthenticationFailed("IP not allowed")
        elif r.status_code == 400:
            raise BadRequestError("Bad request")
        else:
            r.raise_for_status()

    def status(self):
        status_data = self._get('/status').get('status')
        return Status.from_dict(status_data)

    def ping(self):
        response_json = self._get('/ping')
        result = Result.from_dict(response_json)
        if result.error is False:
            return True
        else:
            raise PingError(result.reason if result.reason else "Ping failed with unknown error")
    
    # Navigation
    def navigate_home(self):
        return Result.from_dict(self._post('/navigate/home'))
    
    def navigate_refresh(self):
        return Result.from_dict(self._post('/navigate/refresh'))
    
    def navigate_forward(self):
        return Result.from_dict(self._post('/navigate/forward'))
    
    def navigate_backward(self):
        return Result.from_dict(self._post('/navigate/backward'))
    
    def navigate_url(self, url: str):
        return Result.from_dict(self._post('/navigate/url', json={'url': url}))
    
    # Print
    def print(self):
        return Result.from_dict(self._post('/print'))
    
    # Clear
    def clear_cookies(self):
        return Result.from_dict(self._post('/clear/cookies'))
    
    def clear_cache(self):
        return Result.from_dict(self._post('/clear/cache'))
    
    # Screensaver
    def screensaver_interact(self):
        return Result.from_dict(self._post('/screensaver/interact'))
    
    def screensaver_set_disabled_state(self, disabled: bool):
        return Result.from_dict(self._post('/screensaver/state', json={'disabled': disabled}))
    
    def screensaver_get_state(self):
        screensaver_status_data = self._get('/screensaver/state').get('screensaver')
        return ScreensaverState.from_dict(screensaver_status_data)
    
    # Blackout
    def blackout_set(self, blackout: Blackout):
        return Result.from_dict(self._post('/blackout', json=blackout.to_dict()))
    
    def blackout_get(self):
        blackout_data = self._get('/blackout/state').get('blackout')
        if blackout_data is None:
            return None
        return Blackout.from_dict(blackout_data)
    
    def blackout_clear(self):
        return Result.from_dict(self._post('/blackout', json={'visible': False}))
