# config/settings.py
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional


class BotSettings:
    """
    Lightweight settings container for your application.
    Loads:
      - environment settings (you define defaults here)
      - court codes from JSON
    """

    def __init__(
        self,
        *,
        court_codes_path: Optional[str] = None, 
        num_days: int = 7,
        wait_time: int = 15
    ):
        self.num_days = num_days

        # Determine JSON location
        if court_codes_path is None:
            court_codes_path = (
                Path(__file__).resolve().parent / "data" / "court_codes.json"
            )

        self.court_codes_path = Path(court_codes_path)

        # Load dict from JSON file
        self.court_codes = self._load_court_codes()
        self.wait_time = wait_time

    def _load_court_codes(self) -> Dict[str, str]:
        """Loads court_codes.json and returns a dictionary."""
        if not self.court_codes_path.exists():
            raise FileNotFoundError(
                f"court_codes.json not found at {self.court_codes_path}. "
                "Run SeleniumScraper() first."
            )

        return json.loads(self.court_codes_path.read_text(encoding="utf-8"))

    def select_by_name(self, phrase: str) -> List[str]:
        """Return codes that match a keyword ('Suffolk', 'District', etcphrase = phrase.lower()"""
        return [
            code
            for code, name in self.court_codes.items()
            if phrase.lower() in name.lower()
        ]