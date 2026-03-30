#!/usr/bin/env python3
"""
Get the last logbook entry.

Usage:
    # Get last logbook entry
    python -m scripts.last_entry
    
    # Get last N entries
    python -m scripts.last_entry --count 5
    
    # Get just the date
    python -m scripts.last_entry --date-only
    
    # Get full details
    python -m scripts.last_entry --full
"""

import sys
import json
import argparse
import asyncio
from typing import Dict, Any

from core.api.logbook_service import LogbookService
from core.session_manager import SessionManager


async def get_last_entries(count: int = 1) -> list:
    """Get the last N logbook entries."""
    session = SessionManager()
    await session.get_api_client()
    
    service = LogbookService(session)
    result = await service.list_logbooks()
    await session.close()
    
    entries = result.get('data', [])
    return entries[:count]


def format_entry(entry: Dict[str, Any], full: bool = False) -> str:
    """Format a single entry for display."""
    date = entry.get('selected_date', 'N/A').split('T')[0]
    project = entry.get('project', 'N/A')
    work_mode = entry.get('work_mode', 'N/A')
    
    detail = entry.get('detail', [{}])[0] if entry.get('detail') else {}
    activity_info = detail.get('activity', [{}])[0] if detail.get('activity') else {}
    activity = activity_info.get('value', 'N/A') if activity_info else 'N/A'
    progress = activity_info.get('progress', {}) if activity_info else {}
    percentage = progress.get('percentage', 'N/A')
    ptype = progress.get('type', 'N/A')
    
    if full:
        return json.dumps(entry, indent=2)
    
    return f"""Date: {date}
Project: {project}
Activity: {activity}
Progress: {ptype} ({percentage}%)
Work mode: {work_mode}"""


async def async_main():
    parser = argparse.ArgumentParser(description="Get last logbook entry")
    parser.add_argument("--count", type=int, default=1, help="Number of entries to retrieve")
    parser.add_argument("--date-only", action="store_true", help="Only show the date")
    parser.add_argument("--full", action="store_true", help="Show full JSON output")
    
    args = parser.parse_args()
    
    entries = await get_last_entries(args.count)
    
    if not entries:
        print("No logbook entries found")
        return
    
    if args.date_only:
        for entry in entries:
            print(entry.get('selected_date', 'N/A').split('T')[0])
    elif args.full:
        print(json.dumps(entries, indent=2))
    else:
        for i, entry in enumerate(entries, 1):
            if args.count > 1:
                print(f"--- Entry {i} ---")
            print(format_entry(entry))
            if args.count > 1:
                print()


if __name__ == "__main__":
    asyncio.run(async_main())