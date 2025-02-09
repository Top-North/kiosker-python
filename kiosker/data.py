from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class Status:
    battery_level: int
    battery_state: str
    model: str
    os_version: str
    last_interaction: datetime
    last_update: datetime
    device_id: str
    last_motion: Optional[datetime.datetime]
    screensaver_pause: Optional[bool]
    
    def __init__(self, status_data):
        self.battery_level = status_data['batteryLevel']
        self.battery_state = status_data['batteryState']
        self.model = status_data['model']
        self.os_version = status_data['osVersion']
        self.last_interaction = datetime.datetime.fromisoformat(status_data['lastInteraction'])
        self.last_motion = datetime.datetime.fromisoformat(status_data['lastMotion']) if status_data.get('lastMotion') else None
        self.last_update = datetime.datetime.fromisoformat(status_data['date'])
        self.device_id = status_data['deviceId']
        self.screensaver_pause = status_data['screensaverPause'] if status_data.get('screensaverPause') else None

@dataclass
class Result:
    error: bool
    reason: str
    function: Optional[str]

    def __init__(self, result_data):
        self.error = result_data['error']
        self.function = result_data['function']
        self.reason = result_data['reason'] if result_data.get('reason') else None
        
@dataclass
class Blackout:
    visible: bool
    background: str
    foreground: str
    expire: int
    text: Optional[str] = None
    icon: Optional[str] = None
    
    def to_dict(self):
        return {'visible': self.visible, 'text': self.text, 'background': self.background, 'foreground': self.foreground, 'icon': self.icon, 'expire': self.expire}
    
    @classmethod
    def from_dict(cls, blackout_data):
        return cls(visible=blackout_data['visible'], text=blackout_data.get('text'), background=blackout_data['background'], foreground=blackout_data['foreground'], icon=blackout_data.get('icon'), expire=blackout_data['expire'])