#!/usr/bin/env python3
"""
List logbook entries for a date range, or find missing dates.

Usage:
    # List entries in date range
    python -m scripts.list_dates --start 2026-03-01 --end 2026-03-15
    
    # Find missing dates (no logbook entry)
    python -m scripts.list_dates --missing --start 2026-03-01 --end 2026-03-15
    
    # Find missing dates excluding weekends and Indonesian holidays
    python -m scripts.list_dates --missing --start 2026-03-01 --end 2026-03-15 --exclude-weekends --exclude-holidays
"""

import sys
import json
import argparse
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any

from core.api.logbook_service import LogbookService
from core.session_manager import SessionManager


# Indonesian public holidays 2024-2026 (common ones)
INDONESIAN_HOLIDAYS = {
    # 2024
    "2024-01-01": "Tahun Baru",
    "2024-02-08": "Imlek",
    "2024-03-11": "Nyepi",
    "2024-03-29": "Wafat Isa Almasih",
    "2024-04-10": "Idul Fitri",
    "2024-04-11": "Idul Fitri",
    "2024-05-01": "Hari Buruh",
    "2024-05-09": "Kenaikan Isa Almasih",
    "2024-05-23": "Hari Pantun",
    "2024-06-01": "Hari Lahir Pancasila",
    "2024-06-17": "Idul Adha",
    "2024-07-07": "Tahun Baru Islam",
    "2024-08-17": "Hari Kemerdekaan",
    "2024-09-16": "Maulid Nabi",
    "2024-12-25": "Natal",
    
    # 2025
    "2025-01-01": "Tahun Baru",
    "2025-01-29": "Imlek",
    "2025-03-29": "Nyepi",
    "2025-03-31": "Idul Fitri",
    "2025-04-01": "Idul Fitri",
    "2025-05-01": "Hari Buruh",
    "2025-05-12": "Wafat Isa Almasih",
    "2025-05-29": "Kenaikan Isa Almasih",
    "2025-06-01": "Hari Lahir Pancasila",
    "2025-06-06": "Idul Adha",
    "2025-06-27": "Tahun Baru Islam",
    "2025-08-17": "Hari Kemerdekaan",
    "2025-09-05": "Maulid Nabi",
    "2025-12-25": "Natal",
    
    # 2026
    "2026-01-01": "Tahun Baru",
    "2026-02-17": "Imlek",
    "2026-03-18": "Nyepi",
    "2026-03-20": "Idul Fitri",
    "2026-03-21": "Idul Fitri",
    "2026-04-03": "Wafat Isa Almasih",
    "2026-05-01": "Hari Buruh",
    "2026-05-14": "Kenaikan Isa Almasih",
    "2026-05-26": "Idul Adha",
    "2026-06-01": "Hari Lahir Pancasila",
    "2026-06-16": "Tahun Baru Islam",
    "2026-08-17": "Hari Kemerdekaan",
    "2026-08-25": "Maulid Nabi",
    "2026-12-25": "Natal",
}


def parse_date(date_str: str) -> datetime:
    """Parse date string in YYYY-MM-DD format."""
    return datetime.strptime(date_str, "%Y-%m-%d")


def get_weekdays(start: datetime, end: datetime, exclude_weekends: bool = True, exclude_holidays: bool = False) -> List[datetime]:
    """Get all weekdays in a date range, optionally excluding holidays."""
    days = []
    current = start
    while current <= end:
        # Skip weekends if requested
        if exclude_weekends and current.weekday() >= 5:  # Saturday = 5, Sunday = 6
            current += timedelta(days=1)
            continue
        
        # Skip holidays if requested
        date_str = current.strftime("%Y-%m-%d")
        if exclude_holidays and date_str in INDONESIAN_HOLIDAYS:
            current += timedelta(days=1)
            continue
        
        days.append(current)
        current += timedelta(days=1)
    
    return days


async def list_logbook_dates(start: datetime, end: datetime) -> Dict[str, Any]:
    """List logbook entries in date range."""
    session = SessionManager()
    await session.get_api_client()
    
    service = LogbookService(session)
    all_entries = await service.list_logbooks()
    await session.close()
    
    entries = all_entries.get('data', [])
    
    # Filter by date range
    filtered = []
    for entry in entries:
        selected_date_str = entry.get('selected_date', '')
        if selected_date_str:
            # Parse the date (format: 2026-03-12T00:00:00.000Z)
            entry_date = datetime.fromisoformat(selected_date_str.replace('Z', '+00:00'))
            entry_date_naive = entry_date.replace(tzinfo=None)
            if start <= entry_date_naive <= end:
                filtered.append(entry)
    
    return filtered


def format_missing_dates(missing: List[datetime]) -> str:
    """Format missing dates as JSON."""
    return json.dumps([{
        "date": d.strftime("%Y-%m-%d"),
        "day": d.strftime("%A"),
        "holiday": INDONESIAN_HOLIDAYS.get(d.strftime("%Y-%m-%d"), None)
    } for d in missing], indent=2)


async def async_main():
    parser = argparse.ArgumentParser(description="List logbook dates or find missing entries")
    parser.add_argument("--start", type=str, required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--missing", action="store_true", help="Find missing dates (no logbook entry)")
    parser.add_argument("--exclude-weekends", action="store_true", help="Exclude weekends when finding missing dates")
    parser.add_argument("--exclude-holidays", action="store_true", help="Exclude Indonesian holidays")
    
    args = parser.parse_args()
    
    start = parse_date(args.start)
    end = parse_date(args.end)
    
    if args.missing:
        # Get all weekdays in range
        all_days = get_weekdays(start, end, args.exclude_weekends, args.exclude_holidays)
        
        # Get existing logbook dates
        entries = await list_logbook_dates(start, end)
        existing_dates = set()
        for entry in entries:
            date_str = entry.get('selected_date', '')
            if date_str:
                entry_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                existing_dates.add(entry_date.strftime("%Y-%m-%d"))
        
        # Find missing dates
        missing = [d for d in all_days if d.strftime("%Y-%m-%d") not in existing_dates]
        
        if missing:
            print(format_missing_dates(missing))
        else:
            print(json.dumps({"message": "All dates have logbook entries"}))
    else:
        # List entries in range
        entries = await list_logbook_dates(start, end)
        
        # Format output
        result = [{
            "date": e.get('selected_date', '').split('T')[0],
            "project": e.get('project'),
            "activity": e.get('detail', [{}])[0].get('activity', [{}])[0].get('value', 'N/A') if e.get('detail') else 'N/A',
            "work_mode": e.get('work_mode', 'N/A')
        } for e in entries]
        
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(async_main())