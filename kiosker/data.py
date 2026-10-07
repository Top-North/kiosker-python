from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Self

@dataclass
class Status:
    """Current status of the Kiosker device, as returned by ``KioskerAPI.status()``.

    Attributes:
        battery_level: Battery level in percent. 0 if the level is unknown.
        battery_state: "Unknown", "Not Charging", "Charging", or "Fully Charged".
        model: Device model, eg. "iPad".
        os_version: Operating system name and version, eg. "iPadOS 26.2".
        app_name: App name, eg. "Kiosker Pro".
        app_version: App version and build, eg. "26.9.1 (287)".
        last_interaction: Time of the last user interaction.
        last_update: The device's clock when the status was created.
        device_id: Unique identifier of the device.
        last_motion: Time of the last detected motion, or None if no motion has been detected
            or motion detection is off.
        ambient_light: Unitless ambient light level from the camera, or None if the camera
            sensor is disabled.
        app_start: Time the app was started, or None if unknown (eg. on older app versions).
    """

    battery_level: int
    battery_state: str
    model: str
    os_version: str
    app_name: str
    app_version: str
    last_interaction: datetime
    last_update: datetime
    device_id: str
    last_motion: Optional[datetime]
    ambient_light: Optional[float]
    app_start: Optional[datetime] = None

    @classmethod
    def from_dict(cls, status_data):
        return cls(battery_level=status_data['batteryLevel'], battery_state=status_data['batteryState'], model=status_data['model'], os_version=status_data['osVersion'], app_name=status_data['appName'], app_version=status_data['appVersion'], last_interaction=datetime.fromisoformat(status_data['lastInteraction']), last_motion=datetime.fromisoformat(status_data['lastMotion']) if status_data.get('lastMotion') else None, last_update=datetime.fromisoformat(status_data['date']), device_id=status_data['deviceId'], ambient_light=status_data.get('ambientLight'), app_start=_parse_dt(status_data.get('appStart')))

@dataclass
class Result:
    """Result of an API operation.

    Attributes:
        error: True if the operation failed.
        reason: Error description when error is True. Can also carry information on success,
            eg. ``KioskerAPI.settings_set()`` lists skipped protected keys here.
        function: The API function that was called, eg. "navigate/url".
    """

    error: bool
    reason: Optional[str]
    function: Optional[str]
    
    @classmethod
    def from_dict(cls, result_data):
        return cls(error=result_data['error'], reason=result_data['reason'] if result_data.get('reason') else None , function=result_data.get('function') if result_data.get('function') else None)

@dataclass
class ScreensaverState:
    """Screensaver state, as returned by ``KioskerAPI.screensaver_get_state()``.

    Attributes:
        visible: Whether the screensaver is currently shown. Can be None if the state is unknown.
        disabled: Whether the screensaver is disabled through the API
            (``KioskerAPI.screensaver_set_disabled_state()``). The screensaver schedule
            configured in the app isn't reflected here.
    """

    visible: bool
    disabled: bool
    
    @classmethod
    def from_dict(cls, state_data):
        return cls(visible=state_data['visible'], disabled=state_data['disabled'])

        
@dataclass
class Blackout:
    """A blackout screen covering the kiosk, eg. for maintenance.

    Field names are camelCase to match the API. Only ``visible`` is required; leaving out the
    rest gives a black screen that expires after 24 hours.

    Attributes:
        visible: True to show the blackout, False to remove it.
        background: Background color as hex, eg. "#000000". Defaults to black.
        foreground: Text and icon color as hex, eg. "#FFFFFF". Defaults to white.
        expire: When setting, seconds until the blackout expires (default 86400). When read
            with ``KioskerAPI.blackout_get()``, the remaining seconds, which can be a decimal.
        text: Text shown on the blackout screen.
        icon: SF Symbol name shown above the text, eg. "wrench.and.screwdriver.fill".
        dismissible: Show a button that lets the user dismiss the blackout. Defaults to False.
        buttonBackground: Dismiss button background color as hex. Defaults to blue.
        buttonForeground: Dismiss button text color as hex. Defaults to white.
        buttonText: Dismiss button label.
        sound: Sound to play when the blackout is shown, as a SystemSoundID, eg. "1003".
    """

    visible: bool
    background: Optional[str] = None
    foreground: Optional[str] = None
    expire: Optional[int] = None
    text: Optional[str] = None
    icon: Optional[str] = None
    dismissible: Optional[bool] = False
    buttonBackground: Optional[str] = None
    buttonForeground: Optional[str] = None
    buttonText: Optional[str] = None
    sound: Optional[str] = None

    def to_dict(self):
        return {
            'visible': self.visible,
            'background': self.background,
            'foreground': self.foreground,
            'expire': self.expire,
            'text': self.text,
            'icon': self.icon,
            'dismissible': self.dismissible,
            'buttonBackground': self.buttonBackground,
            'buttonForeground': self.buttonForeground,
            'buttonText': self.buttonText,
            'sound': self.sound,
        }

    @classmethod
    def from_dict(cls, blackout_data):
        return cls(
            visible=blackout_data['visible'],
            background=blackout_data['background'],
            foreground=blackout_data['foreground'],
            expire=blackout_data['expire'],
            text=blackout_data.get('text'),
            icon=blackout_data.get('icon'),
            dismissible=blackout_data.get('dismissible', False),
            buttonBackground=blackout_data.get('buttonBackground'),
            buttonForeground=blackout_data.get('buttonForeground'),
            buttonText=blackout_data.get('buttonText'),
            sound=blackout_data.get('sound'),
        )

@dataclass
class ASAMState:
    """Guided Access (Autonomous Single App Mode) state.

    Attributes:
        enabled: True if Guided Access is enabled and the device is locked to Kiosker.
    """

    enabled: bool
    
    @classmethod
    def from_dict(cls, state_data):
        return cls(enabled=state_data['enabled'])

@dataclass
class Printer:
    """A printer, as used for silent printing.

    Attributes:
        name: The printer's display name. None if no default printer is set.
        url: The printer's URL, eg. "ipp://192.168.1.50:631/ipp/print". None if no default
            printer is set.
    """

    name: Optional[str]
    url: Optional[str]

    def to_dict(self):
        return {'name': self.name, 'url': self.url}

    @classmethod
    def from_dict(cls, state_data):
        return cls(name=state_data.get('name'), url=state_data.get('url'))

@dataclass
class CertificateMetadata:
    """Subject, issuer, and validity details of a client certificate.

    All fields are None if the certificate doesn't contain them.

    Attributes:
        subject_name: Subject common name (CN).
        subject_organization: Subject organization (O).
        subject_location: Subject locality (L).
        subject_state: Subject state or province (ST).
        subject_country: Subject country (C).
        issuer_name: Issuer common name (CN).
        issuer_organization: Issuer organization (O).
        issuer_location: Issuer locality (L).
        issuer_state: Issuer state or province (ST).
        issuer_country: Issuer country (C).
        not_valid_before: Start of the validity period.
        not_valid_after: End of the validity period.
    """

    subject_name: str | None = None
    subject_organization: str | None = None
    subject_location: str | None = None
    subject_state: str | None = None
    subject_country: str | None = None
    issuer_name: str | None = None
    issuer_organization: str | None = None
    issuer_location: str | None = None
    issuer_state: str | None = None
    issuer_country: str | None = None
    not_valid_before: datetime | None = None
    not_valid_after: datetime | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            subject_name=data.get("subjectName"),
            subject_organization=data.get("subjectOrganization"),
            subject_location=data.get("subjectLocation"),
            subject_state=data.get("subjectState"),
            subject_country=data.get("subjectCountry"),
            issuer_name=data.get("issuerName"),
            issuer_organization=data.get("issuerOrganization"),
            issuer_location=data.get("issuerLocation"),
            issuer_state=data.get("issuerState"),
            issuer_country=data.get("issuerCountry"),
            not_valid_before=_parse_dt(data.get("notValidBefore")),
            not_valid_after=_parse_dt(data.get("notValidAfter")),
        )


@dataclass
class Certificate:
    """A client certificate used for mutual TLS when browsing, as returned by
    ``KioskerAPI.client_certificates_list()``.

    Attributes:
        id: Certificate identifier.
        hosts: Hosts the certificate is used for. Empty for the default certificate, which is
            used for hosts that don't match any other certificate.
        metadata: Subject, issuer, and validity details.
        password: Always None when listing; the password is never returned by the API.
        base64: Always None when listing; the certificate data is never returned by the API.
        fingerprint: SHA-256 fingerprint of the certificate as lowercase hex.
    """

    id: str
    hosts: list[str] = field(default_factory=list)
    metadata: CertificateMetadata = field(default_factory=CertificateMetadata)
    password: str | None = None
    base64: str | None = None
    fingerprint: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data["id"],
            fingerprint=data.get("fingerprint"),
            hosts=list(data.get("hosts") or []),
            metadata=CertificateMetadata.from_dict(data.get("metadata") or {}),
            password=data.get("password"),
            base64=data.get("base64"),
        )


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
