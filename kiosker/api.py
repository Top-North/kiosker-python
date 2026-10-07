import ssl
from typing import Any
import httpx
from .data import Printer, Status, Result, Blackout, ScreensaverState, ASAMState, Certificate
from .exceptions import ConnectionError, TLSVerificationError, AuthenticationError, IPAuthenticationError, BadRequestError, PingError, NotFoundError, ConflictError

API_PATH = '/api/v1'

class KioskerAPI:
    """Client for the Kiosker REST API.

    All methods can raise the following exceptions, in addition to the ones listed per method:

    - ConnectionError: The device can't be reached, or it returned an unexpected status code.
    - TLSVerificationError: TLS certificate verification failed (only when ``ssl=True`` and ``verify`` is set).
    - AuthenticationError: The token is missing or invalid (HTTP 401).
    - IPAuthenticationError: The client IP isn't in the device's IP filter whitelist (HTTP 403).
    - BadRequestError: The request was rejected as invalid (HTTP 400). The message contains the device's reason.
    """

    def __init__(self, host, token, port=8081, ssl=False, verify: bool | ssl.SSLContext =False):
        """Create an API client for a Kiosker device.

        Args:
            host: IP address or host name of the device.
            token: The API bearer token, generated in the Kiosker app.
            port: The API port. Defaults to 8081.
            ssl: Connect over HTTPS. Requires TLS to be enabled in the Kiosker app.
            verify: TLS verification. ``False`` (default) accepts any certificate, such as a
                self-signed one, ``True`` uses the system CA store, or pass an ``ssl.SSLContext``
                to trust a specific certificate.
        """
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
                raise TLSVerificationError(e)
            raise ConnectionError(e)
        except Exception as e:
            raise ConnectionError(e)
        return self._handle(r)

    def _post(self, path: str, json=None):
        if json is None:
            json = {}
        try:
            r = httpx.post(f'{self.conf_host}{API_PATH}{path}', headers=self.conf_headers, json=json, verify=self.verify)
        except httpx.ConnectError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e) or "SSL" in str(e):
                raise TLSVerificationError(e)
            raise ConnectionError(e)
        except Exception as e:
            raise ConnectionError(e)
        return self._handle(r)

    def _delete(self, path: str, json=None):
        # httpx.delete() can't send a body, so use request()
        try:
            r = httpx.request('DELETE', f'{self.conf_host}{API_PATH}{path}', headers=self.conf_headers, json=json, verify=self.verify)
        except httpx.ConnectError as e:
            if "CERTIFICATE_VERIFY_FAILED" in str(e) or "SSL" in str(e):
                raise TLSVerificationError(e)
            raise ConnectionError(e)
        except Exception as e:
            raise ConnectionError(e)
        return self._handle(r)

    @staticmethod
    def _reason(r, default: str) -> str:
        try:
            return r.json().get('reason') or default
        except Exception:
            return default

    def _handle(self, r):
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            raise AuthenticationError("Unauthorized")
        elif r.status_code == 403:
            raise IPAuthenticationError("IP not allowed")
        elif r.status_code == 400:
            raise BadRequestError(self._reason(r, "Bad request"))
        elif r.status_code == 404:
            raise NotFoundError(self._reason(r, "Not found"))
        elif r.status_code == 409:
            raise ConflictError(self._reason(r, "Conflict"))
        else:
            raise ConnectionError(r.status_code)

    def status(self):
        """Get the current device status.

        Returns:
            Status: Battery, device, app, and interaction details, such as the last interaction,
            last detected motion, ambient light, and app start time.
        """
        status_data = self._get('/status').get('status')
        return Status.from_dict(status_data)

    def ping(self):
        """Check that the API is reachable and Kiosker is running in the foreground.

        Returns:
            bool: Always ``True``. Failures are raised as exceptions.

        Raises:
            PingError: The device responded but reported an error.
        """
        response_json = self._get('/ping')
        result = Result.from_dict(response_json)
        if result.error is False:
            return True
        else:
            raise PingError(result.reason if result.reason else "Ping failed with unknown error")

    # Navigation
    def navigate_home(self):
        """Navigate to the configured start page.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/navigate/home'))

    def navigate_refresh(self):
        """Reload the current page.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/navigate/refresh'))

    def navigate_forward(self):
        """Navigate forward in the browsing history.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/navigate/forward'))

    def navigate_backward(self):
        """Navigate back in the browsing history.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/navigate/backward'))

    def navigate_url(self, url: str):
        """Navigate to a URL.

        Args:
            url: The URL to load, eg. ``https://example.com``.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/navigate/url', json={'url': url}))

    # Print
    def print(self):
        """Print the current page.

        Uses silent printing to the default printer if it's enabled in the Kiosker app,
        otherwise the print dialog is shown on the device.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/print'))

    # Clear
    def clear_cookies(self):
        """Clear all cookies.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/clear/cookies'))

    def clear_cache(self):
        """Clear the web cache and website data.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/clear/cache'))

    def clear_history(self):
        """Clear the browsing history.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/clear/history'))

    # Screensaver
    def screensaver_interact(self):
        """Simulate a user interaction, hiding the screensaver if it's visible.

        Unlike a real touch, this doesn't reset the idle timer or the browsing time limit.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/screensaver/interact'))

    def screensaver_set_disabled_state(self, disabled: bool):
        """Disable or enable the screensaver.

        Args:
            disabled: ``True`` to stop the screensaver from appearing, ``False`` to allow it again.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/screensaver/state', json={'disabled': disabled}))

    def screensaver_get_state(self):
        """Get the screensaver state.

        Returns:
            ScreensaverState: Whether the screensaver is disabled by the API and whether it's currently visible.
        """
        screensaver_status_data = self._get('/screensaver/state').get('screensaver')
        return ScreensaverState.from_dict(screensaver_status_data)

    # Blackout
    def blackout_set(self, blackout: Blackout):
        """Show a blackout screen, eg. to close the kiosk for maintenance.

        Calling it again while a blackout is shown replaces it.

        Args:
            blackout: The blackout configuration. Only ``visible`` is required; leaving out the
                rest gives a black screen that expires after 24 hours.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/blackout', json=blackout.to_dict()))

    def blackout_get(self):
        """Get the current blackout.

        Returns:
            Blackout | None: The active blackout, with ``expire`` as the remaining seconds,
            or ``None`` if no blackout is set.
        """
        blackout_data = self._get('/blackout/state').get('blackout')
        if blackout_data is None:
            return None
        return Blackout.from_dict(blackout_data)

    def blackout_clear(self):
        """Remove the blackout screen.

        Returns:
            Result: The result of the operation.
        """
        return Result.from_dict(self._post('/blackout', json={'visible': False}))

    # ASAM
    def asam_set_enabled_state(self, enabled: bool):
        """Enable or disable Guided Access (Autonomous Single App Mode).

        The device must be supervised and allow Kiosker to use Autonomous Single App Mode.
        The call returns before iOS has applied the change, so a successful result doesn't
        confirm the new state. Use ``asam_get_state()`` to verify.

        Args:
            enabled: ``True`` to lock the device to Kiosker, ``False`` to unlock it.

        Returns:
            Result: The result of the request.
        """
        return Result.from_dict(self._post('/asam/state', json={'enabled': enabled}))

    def asam_get_state(self):
        """Get the Guided Access (Autonomous Single App Mode) state.

        Returns:
            ASAMState: Whether Guided Access is currently enabled.
        """
        asam_status_data = self._get('/asam/state').get('asam')
        return ASAMState.from_dict(asam_status_data)

    # Settings
    def settings_get(self) -> dict[str, Any]:
        """Get the full settings object.

        The settings contain sensitive values, such as AutoFill values and the settings
        password hash, so we recommend using TLS.

        Returns:
            dict[str, Any]: The settings, keyed by setting name.

        Raises:
            ValueError: The device returned no settings object.
        """
        settings_data = self._get('/settings').get('settings')
        if not isinstance(settings_data, dict):
            raise ValueError(f"unexpected settings payload: {settings_data!r}")
        return settings_data

    def settings_set(self, settings: dict[str, Any]):
        """Merge the given keys into the current settings.

        Keys left out keep their current value, nested objects are merged key by key, and
        arrays and values are replaced. Protected API and MDM keys (``apiActive``, ``apiTLS``,
        ``apiIpFilter``, and ``apiIpWhitelist``) are skipped and listed
        in ``Result.reason``.

        Args:
            settings: One or more keys from the settings object, eg. ``{'url': 'https://example.com'}``.
                See ``settings_get()`` for the available keys.

        Returns:
            Result: The result of the operation. ``reason`` lists any skipped protected keys.

        Raises:
            BadRequestError: A value has the wrong type. The message names the key.
            ConflictError: The settings are managed by MDM.
        """
        return Result.from_dict(self._post('/settings', json=settings))

    def settings_clear(self):
        """Reset all settings to their defaults.

        Warning: the defaults disable the API, so the device stops responding to API calls
        afterwards until the API is enabled again in the Kiosker app.

        Returns:
            Result: The result of the operation.

        Raises:
            ConflictError: The settings are managed by MDM.
        """
        return Result.from_dict(self._delete('/settings'))

    #Printer
    def printer_default_set(self, printer: Printer):
        """Set the default printer used for silent printing.

        Args:
            printer: The printer. Both ``name`` and ``url`` are required. Use ``printers_list()``
                to find available printers.

        Returns:
            Result: The result of the operation.

        Raises:
            BadRequestError: ``name`` or ``url`` is missing or invalid.
        """
        return Result.from_dict(self._post('/printer/default', json=printer.to_dict()))

    def printer_default_get(self):
        """Get the default printer.

        Returns:
            Printer: The default printer. ``name`` and ``url`` are ``None`` if no printer is set.
        """
        printer_data = self._get('/printer/default').get('printer')
        return Printer.from_dict(printer_data)

    def printers_list(self):
        """Discover AirPrint printers on the local network.

        Discovery runs on the device for about 5 seconds before the call returns.

        Returns:
            list[Printer]: The printers found, possibly empty.
        """
        printer_data = self._get('/printer/list').get('printers') or []
        return [Printer.from_dict(p) for p in printer_data]

    # Client certificates
    @staticmethod
    def _certificate_reference(id: str | None, fingerprint: str | None) -> dict[str, str]:
        if id is None and fingerprint is None:
            raise ValueError("id or fingerprint is required")
        reference = {}
        if id is not None:
            reference['id'] = id
        if fingerprint is not None:
            reference['fingerprint'] = fingerprint
        return reference

    def client_certificates_list(self) -> list[Certificate]:
        """List the client certificates used for mutual TLS when browsing.

        Only certificates added on the device or through the API are listed, not ones provided
        by MDM. The certificate data and password are never returned.

        Returns:
            list[Certificate]: The certificates with id, fingerprint, hosts, and metadata.
        """
        certificate_data = self._get('/client_certificate').get('clientCertificates') or []
        return [Certificate.from_dict(c) for c in certificate_data]

    def client_certificate_add(self, base64: str, password: str, hosts: list[str] | None = None):
        """Add a PKCS#12 (.p12) client certificate.

        Only one default certificate is allowed, and a host can only belong to one certificate.

        Args:
            base64: The .p12 file contents, base64 encoded.
            password: The password protecting the .p12 data.
            hosts: Hosts the certificate is used for. Leave out (or empty) to make it the
                default certificate, used for hosts that don't match any other certificate.

        Returns:
            Result: The result of the operation.

        Raises:
            BadRequestError: The data or password is wrong, a host is already used, or a default
                certificate already exists.
            ConflictError: Client certificates are managed by MDM.
        """
        return Result.from_dict(self._post('/client_certificate', json={'base64': base64, 'password': password, 'hosts': hosts or []}))

    def client_certificate_delete(self, id: str | None = None, fingerprint: str | None = None):
        """Delete a client certificate.

        Args:
            id: The certificate id. Used if both id and fingerprint are given.
            fingerprint: The certificate's SHA-256 fingerprint, as lowercase hex.

        Returns:
            Result: The result of the operation.

        Raises:
            ValueError: Neither id nor fingerprint was given.
            NotFoundError: No certificate matches the id or fingerprint.
            ConflictError: Client certificates are managed by MDM.
        """
        return Result.from_dict(self._delete('/client_certificate', json=self._certificate_reference(id, fingerprint)))

    def client_certificate_set_hosts(self, hosts: list[str], id: str | None = None, fingerprint: str | None = None):
        """Replace the hosts a client certificate is used for.

        Args:
            hosts: The new hosts. An empty list makes it the default certificate.
            id: The certificate id. Used if both id and fingerprint are given.
            fingerprint: The certificate's SHA-256 fingerprint, as lowercase hex.

        Returns:
            Result: The result of the operation.

        Raises:
            ValueError: Neither id nor fingerprint was given.
            BadRequestError: A host is already used by another certificate, or a default
                certificate already exists.
            NotFoundError: No certificate matches the id or fingerprint.
            ConflictError: Client certificates are managed by MDM.
        """
        return Result.from_dict(self._post('/client_certificate/hosts', json={**self._certificate_reference(id, fingerprint), 'hosts': hosts}))
