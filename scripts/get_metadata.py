#!/usr/bin/env python3
import sys
import json
import asyncio
import argparse
from typing import Dict, Any

from core.api.logbook_service import LogbookService 
from core.session_manager import SessionManager 
from core.api.project_service import ProjectService
from core.model.logbook_model import WorkModeType

async def main():
    parser = argparse.ArgumentParser(description="Fetch metadata with filtering and search.")
    parser.add_argument("--type", choices=["all", "projects", "tools", "progress"], default="all", help="Filter metadata by type.")
    parser.add_argument("--search", type=str, help="Search pattern for names.")
    args = parser.parse_args()

    try:
        session = SessionManager()
        await session.get_api_client()
        log_service = LogbookService(session)
        proj_service = ProjectService(session)

        metadata = {}

        # Fetch based on type
        if args.type in ["all", "projects"]:
            res = await proj_service.list_projects()
            metadata["projects"] = res.get("data", [])
        
        if args.type in ["all", "tools"]:
            res = await log_service.list_tools()
            metadata["tools"] = res.get("data", [])

        if args.type in ["all", "progress"]:
            res = await log_service.list_progress_types()
            metadata["progress_types"] = res.get("data", [])

        if args.type == "all":
            import typing
            metadata["work_modes"] = list(typing.get_args(WorkModeType))

        # Apply search filter if provided
        if args.search:
            search_lower = args.search.lower()
            for key in ["projects", "tools", "progress_types"]:
                if key in metadata:
                    metadata[key] = [
                        item for item in metadata[key] 
                        if search_lower in item.get("name", "").lower()
                    ]

        print(json.dumps(metadata, indent=2))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(main())
