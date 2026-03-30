import os
import json
import time
import asyncio
import jwt
from typing import Optional
from core.config import Config

import httpx
from playwright.async_api import async_playwright, Browser, BrowserContext
from pathlib import Path
import base64

SESSION_DIR = Path.home() / ".sv_logbook"
SESSION_FILE = SESSION_DIR / "session.enc"  # encrypted session



class SessionManager:
    def __init__(self):
        self.config = Config()
        self.login_url = self.config.login_url
        self.email = self.config.email
        self.password = self.config.password
        self.domain = self.config.domain

        self._token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._user_id: Optional[str] = None
        self._user_team: Optional[str] = None
        self._token_exp: Optional[int] = None
        self._payload: Optional[dict] = None

        self._http: Optional[httpx.AsyncClient] = None

        self._playwright = None
        self._browser: Optional[Browser] = None
        self._browser_context: Optional[BrowserContext] = None

        self._lock = asyncio.Lock()

    # -------------------------
    # Public API
    # -------------------------

    async def get_api_client(self) -> httpx.AsyncClient:
        await self._ensure_logged_in()
        return self._http

    async def get_browser_context(self) -> BrowserContext:
        await self._ensure_logged_in()
        await self._init_browser_context()  # Lazy init only when needed
        return self._browser_context

    # -------------------------
    # Core logic
    # -------------------------
            
    async def _ensure_logged_in(self):
        async with self._lock:
            # 1️⃣ already in memory and valid
            if self._token and not self._token_expiring():
                return

            # 2️⃣ try disk reuse
            if self._load_session_from_disk():
                return  # Browser context init deferred to get_browser_context()

            # 3️⃣ full login
            await self._login_api()
            self._save_session_to_disk()
            # Browser context init deferred to get_browser_context()

    async def _login_api(self):
        print("Authenticating via API...")

        async with httpx.AsyncClient(follow_redirects=True) as tmp:
            # 1. Perform Login
            resp = await tmp.post(
                self.login_url,
                data={
                    "email": self.email,
                    "password": self.password,
                },
            )

            if resp.status_code != 200:
                raise RuntimeError(f"Login failed: {resp.status_code}")

            data = resp.json()
            self._token = data["data"]["access_token"]
            self._refresh_token = data["data"]["refresh_token"]

            # 2. Decode JWT for basic info
            payload = jwt.decode(self._token, options={"verify_signature": False})
            self._payload = payload
            self._user_id = payload.get("user_id")
            self._token_exp = payload.get("exp")

            # 3. Fetch Full User Profile to get team info
            # We use the 'tmp' client or a new one with the token we just got
            profile_url = f"{Config().auth()['origin_url']}/api/users/{self._user_id}"
            profile_resp = await tmp.get(
                profile_url, 
                headers={"Authorization": f"Bearer {self._token}"}
            )

            if profile_resp.status_code == 200:
                user_data = profile_resp.json().get("data", {})
                # Extract team name safely
                self._user_team = user_data.get("team", {}).get("name")
                if self._user_team == None:
                    raise ValueError(f"User {self._user_id} has no assigned team. Team is required for logbook entries.")
            else:
                raise ValueError(f"Profile fetch failed with status code: {profile_resp.status_code}")

        # 4. Initialize persistent API client
        self._http = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {self._token}"},
            follow_redirects=True,
        )

    async def _init_browser_context(self):
        if not self._playwright:
            self._playwright = await async_playwright().start()

        if not self._browser:
            self._browser = await self._playwright.chromium.launch(headless=True)  # Headless for server

        # 1️⃣ try cookie-based hydration
        self._browser_context = await self._browser.new_context()

        # Add cookies BEFORE navigation
        encoded_access = base64.b64encode(self._token.encode()).decode()
        encoded_refresh = base64.b64encode(self._refresh_token.encode()).decode()
        await self._browser_context.add_cookies([
            {
                "name": "access_token",
                "value": encoded_access,
                "domain": self.domain,
                "path": "/",
                "sameSite": "Lax",
            },
            {
                "name": "refresh_token",
                "value": encoded_refresh,
                "domain": self.domain,
                "path": "/",
                "sameSite": "Lax",
            },
        ])


        # 2️⃣ inject token for frontend JS (safe even if unused)
        if self._payload:
            auth_user_json = json.dumps(self._payload)

            await self._browser_context.add_init_script(
                f"""
                (() => {{
                    sessionStorage.setItem("isFirstLogin", "true");
                    sessionStorage.setItem("authUser", JSON.stringify({auth_user_json}));
                }})();
                """
            )
            



    # -------------------------
    # Helpers
    # -------------------------
    def _load_session_from_disk(self) -> bool:
        if not SESSION_FILE.exists():
            return False

        try:
            # Read and decrypt
            encrypted_data = SESSION_FILE.read_bytes()
            decrypted_data = self.config.fernet.decrypt(encrypted_data)
            data = json.loads(decrypted_data.decode())
            
            token = data.get("token")
            refresh_token = data.get("refresh_token")
            user_id = data.get("user_id")
            exp = data.get("exp")
            user_team = data.get("user_team")


            if not token:
                return False

            payload = jwt.decode(token, options={"verify_signature": False})
            self._payload = payload

            if not exp or time.time() > exp:
                return False

            self._token = token
            self._refresh_token = refresh_token
            self._token_exp = exp
            self._user_id = user_id
            self._user_team = user_team


            self._http = httpx.AsyncClient(
                headers={"Authorization": f"Bearer {self._token}"},
                follow_redirects=True,
            )

            print("Reused existing token")
            return True

        except Exception as e:
            print(f"Session load error: {e}")
            return False


    def _save_session_to_disk(self):
        SESSION_DIR.mkdir(parents=True, exist_ok=True)
        
        # Encrypt session data
        session_data = json.dumps(
            {
                "token": self._token,
                "refresh_token": self._refresh_token,
                "user_id": self._user_id,
                "exp": self._token_exp,
                "user_team": self._user_team,
            }
        )
        encrypted_data = self.config.fernet.encrypt(session_data.encode())
        SESSION_FILE.write_bytes(encrypted_data)

    def _token_expiring(self, buffer_seconds: int = 60) -> bool:
        if not self._token_exp:
            return True
        return time.time() > (self._token_exp - buffer_seconds)

    async def _export_api_cookies(self) -> Optional[dict]:
        """
        If backend sets cookies during API login, export them
        so Playwright can reuse the session.
        """
        if not self._http:
            return None

        cookies = []
        for cookie in self._http.cookies.jar:
            cookies.append(
                {
                    "name": cookie.name,
                    "value": cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path,
                    "httpOnly": True,
                    "secure": True,
                    "sameSite": "Lax",
                }
            )
        print(self._http.cookies.jar)
        if not cookies:
            return None

        return {
            "cookies": cookies,
            "origins": [],
        }

    # -------------------------
    # Cleanup
    # -------------------------

    async def close(self):
        if self._http:
            await self._http.aclose()

        if self._browser_context:
            await self._browser_context.close()

        if self._browser:
            await self._browser.close()

        if self._playwright:
            await self._playwright.stop()
