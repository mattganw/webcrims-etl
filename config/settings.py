from pathlib import Path
import json
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

def _load_court_codes():
    path = Path(__file__).parent / "data" / "court_codes.json"
    return json.loads(path.read_text())

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    court_name: Optional[str] = None  # None = all courts
    num_days: int = 7
    wait_time: int = 15
    db_connection_string: str

    url: str = "https://iapps.courts.state.ny.us/webcrim_attorney/AttorneyCalendar"
    court_codes: dict = Field(default_factory=_load_court_codes)

    @field_validator('num_days')
    @classmethod
    def validate_num_days(cls, v: int) -> int:
        if v < 0:
            raise ValueError('num_days must be >= 0')
        return v
    
    @field_validator('wait_time')
    @classmethod
    def validate_wait_time(cls, v: int) -> int:
        if v < 15:
            raise ValueError('wait_time must be >= 15')
        return v

    def select_by_name(self, phrase: Optional[str] = None):
        if not phrase or phrase.strip() == "":  # Empty means all courts
            return self.court_codes
        return {
            code: name
            for code, name in self.court_codes.items()
            if phrase.lower() in name.lower()
        }
