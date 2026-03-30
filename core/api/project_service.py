import asyncio
from typing import List

from core.config import Config
from core.utils import Utils
from core.model.project_model import Project, UseCase

class ProjectService:
    def __init__(self, session):
        self.session = session
        self.origin = Config().auth()["origin_url"]

    async def _get_client(self):
        return await self.session.get_api_client()

    # --- 1. LIST PROJECTS ---
    async def list_projects(self):
        client = await self._get_client()
        # Filter by the current user
        params = {"user_id": self.session._user_id}
        resp = await client.get(f"{self.origin}/api/projects", params=params)
        return resp.json()

    # --- 2. ADD PROJECT ---
    async def add_project(self, project: Project):
        """
        Sends the full payload including fid, user_id, created_at.
        """
        # Ensure timestamps and user_id are set
        project.user_id = self.session._user_id
        project.created_at = Utils.get_now_iso()
        project.updated_at = Utils.get_now_iso()
        
        client = await self._get_client()
        
        # Dump everything (exclude_none strips null IDs)
        payload = project.model_dump(by_alias=True, exclude_none=True)
        
        resp = await client.post(f"{self.origin}/api/projects", json=payload)
        resp.raise_for_status()
        return resp.json()

    # --- 3. EDIT PROJECT (Syncs Use Cases) ---
    async def edit_project(self, project: Project):
        """
        Sends ONLY mutable fields: name, usecases, updated_at.
        Handles Add/Edit/Delete of UseCases automatically based on the list content.
        """
        if not project.fid:
            raise ValueError("Cannot edit a project without an ID (project.id).")
            
        # Update timestamp
        project.updated_at = Utils.get_now_iso()

        client = await self._get_client()
        
        # We explicitly select ONLY the fields allowed in your Edit JSON
        # exclude_none=True is CRITICAL here:
        # - It removes '_id' from new UseCases (triggering Add)
        # - It keeps '_id' for existing UseCases (triggering Edit)
        payload = project.model_dump(
            mode='json',
            by_alias=True, 
            exclude_none=True,
            include={'name', 'usecases', 'updated_at'} 
        )

        # Send to PUT endpoint
        resp = await client.put(f"{self.origin}/api/projects/{project.fid}", json=payload)
        resp.raise_for_status()
        return resp.json()

    # --- 4. DELETE PROJECT (Optional) ---
    async def delete_project(self, project_id: str):
        client = await self._get_client()
        resp = await client.delete(f"{self.origin}/api/projects/{project_id}")
        resp.raise_for_status()
        return resp.json()