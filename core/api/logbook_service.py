import asyncio
import uuid
from datetime import datetime, timezone, date
from typing import List

from core.config import Config
from core.utils import Utils
# ONLY IMPORT THE NEW MODEL
from core.model.logbook_model import LogbookEntry, LogbookDetail, Activity, Tool

class LogbookService:
    def __init__(self, session):
        self.session = session
        self.origin = Config().auth()["origin_url"]

    # --- HELPER: Metadata Fetcher ---
    async def _get_metadata(self):
        client = await self._get_client()
        resps = await asyncio.gather(
            client.get(f"{self.origin}/api/projects", params={"user_id": self.session._user_id}),
            client.get(f"{self.origin}/api/tools"),
            client.get(f"{self.origin}/api/progress")
        )
        for r in resps: r.raise_for_status()
        return {
            "projects": {p["name"]: p for p in resps[0].json()["data"]},
            "tools": {t["name"]: t for t in resps[1].json()["data"]},
            "progress": [pg["name"] for pg in resps[2].json()["data"]]
        }

    # --- ADD (BATCH) ---
    async def add_logbooks_batch(self, entries: List[LogbookEntry]):
        client = await self._get_client()
        results = []
        for entry in entries:
            # Simple dump. The dates are already strings inside 'entry'
            payload = entry.model_dump(by_alias=True, exclude_none=True)
            
            resp = await client.post(f"{self.origin}/api/logbooks", json=payload)
            resp.raise_for_status()
            results.append(resp.json())
        return results  

    # --- EDIT ---
    async def edit_logbook(self, entry: LogbookEntry):
        if not entry.fid:
            raise ValueError("Cannot edit a logbook without an ID.")
            
        # Update timestamp using Utils format before sending
        entry.updated_at = Utils.get_now_iso()

        client = await self._get_client()
        payload = entry.model_dump(by_alias=True, exclude_none=True)

        resp = await client.put(f"{self.origin}/api/logbooks/{entry.fid}", json=payload)
        resp.raise_for_status()
        return resp.json()

    async def _get_client(self):
        return await self.session.get_api_client()

    # --- GET METHODS ---
    async def list_logbooks(self, sort="desc"):
        client = await self._get_client()
        params = {"user_id": self.session._user_id, "sort": sort}
        resp = await client.get(f"{self.origin}/api/logbooks", params=params)
        return resp.json()

    async def list_presences(self, sort="desc"):
        client = await self._get_client()
        params = {"user_id": self.session._user_id, "sort": sort}
        resp = await client.get(f"{self.origin}/api/presences", params=params)
        return resp.json()

    async def list_tools(self):
        client = await self._get_client()
        resp = await client.get(f"{self.origin}/api/tools")
        return resp.json()

    async def list_progress_types(self):
        client = await self._get_client()
        resp = await client.get(f"{self.origin}/api/progress")
        return resp.json()