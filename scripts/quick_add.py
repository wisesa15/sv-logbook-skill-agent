#!/usr/bin/env python3
"""
Add a single logbook entry quickly.

Usage:
    # Quick add (uses defaults from preferences)
    python -m scripts.quick_add --activity "Development: implementing feature X" --project "Project Name"
    
    # With all options
    python -m scripts.quick_add \
        --date 2026-03-30 \
        --project "Project Name" \
        --tool "Python" \
        --activity "Development: feature X" \
        --work-mode WFO \
        --progress 1 \
        --percentage 50
"""

import sys
import json
import argparse
import asyncio
from datetime import datetime
from typing import Dict, Any

from core.api.logbook_service import LogbookService
from core.session_manager import SessionManager
from core.config import Config


async def get_user_info() -> Dict[str, Any]:
    """Get user info from session."""
    session = SessionManager()
    await session.get_api_client()
    
    # Get user_id and team from decoded token
    user_id = session._user_id
    team = session._user_team
    
    await session.close()
    
    return {
        "user_id": user_id,
        "team": team
    }


async def search_tool_fId(query: str) -> str:
    """Search for tool FID by name."""
    from core.api.logbook_service import LogbookService
    
    session = SessionManager()
    await session.get_api_client()
    service = LogbookService(session)
    
    result = await service.search_tools(query)
    await session.close()
    
    if result.get('tools'):
        return result['tools'][0]['fid']
    return None


async def async_main():
    parser = argparse.ArgumentParser(description="Quick add logbook entry")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="Date (YYYY-MM-DD), default: today")
    parser.add_argument("--project", type=str, required=True, help="Project name (will search for FID)")
    parser.add_argument("--tool", type=str, default=None, help="Tool name (will search for FID)")
    parser.add_argument("--activity", type=str, required=True, help="Activity description")
    parser.add_argument("--work-mode", type=str, default="WFO", help="Work mode (WFO/WFH/WFA/Workshop)")
    parser.add_argument("--progress", type=int, default=1, help="Progress value (1 = completed step)")
    parser.add_argument("--percentage", type=int, default=None, help="Progress percentage (for ongoing tasks)")
    parser.add_argument("--next-activity", type=str, default="-", help="Next activity (default: '-')")
    parser.add_argument("--dry-run", action="store_true", help="Print entry without submitting")
    
    args = parser.parse_args()
    
    # Get user info
    user_info = await get_user_info()
    
    # Search for project FID
    # Note: For now, we'll need the exact project name. In future, add project search.
    # For simplicity, assume user provides project FID directly or we need a mapping
    
    print(f"Looking up: project='{args.project}', tool='{args.tool}'...", file=sys.stderr)
    
    # For now, print what would be submitted
    entry = {
        "date": args.date,
        "project_name": args.project,  # This should be project FID
        "tool_fid": None,  # Would need to search
        "activity": args.activity,
        "work_mode": args.work_mode,
        "progress": {
            "value": args.progress,
            "type": "Development",  # Default
            "percentage": args.percentage if args.percentage else 100
        },
        "next_activities": [args.next_activity],
        "user_id": user_info["user_id"],
        "team": user_info["team"]
    }
    
    if args.dry_run:
        print(json.dumps(entry, indent=2))
        return
    
    # TODO: Implement actual submission
    print("Note: Actual submission requires project FID and tool FID.", file=sys.stderr)
    print("Use add_logbook_batch for full control.", file=sys.stderr)
    print(json.dumps(entry, indent=2))


if __name__ == "__main__":
    asyncio.run(async_main())