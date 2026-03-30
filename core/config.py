import os
import hashlib
import base64
from pathlib import Path
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()  # loads .env once


def _derive_fernet_key(password: str) -> bytes:
    """Derive a Fernet key from password using PBKDF2."""
    # Use a fixed salt - consistent derivation for same password
    salt = b"sv_logbook_session_v1"
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, 32)
    return base64.urlsafe_b64encode(key)


class Config:
    def __init__(self):
        self.login_url = os.getenv("LOGIN_URL")
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASS")
        self.referer_url = os.getenv("REFERER_URL")
        self.origin_url = os.getenv("ORIGIN_URL")
        self.domain = os.getenv("DOMAIN", "new-timesheet.sharingvisionjakarta.com")
        
        # Fernet instance for session encryption (lazy)
        self._fernet: Fernet | None = None
    
    @property
    def fernet(self) -> Fernet:
        """Get Fernet instance for session encryption."""
        if self._fernet is None:
            key = _derive_fernet_key(self.password)
            self._fernet = Fernet(key)
        return self._fernet


    def auth(self):
        return {
            "login_url": self.login_url,
            "email": self.email,
            "password": self.password,
            "referer_url": self.referer_url,
            "origin_url": self.origin_url,
        }
