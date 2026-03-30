---
name: sv-logbook
description: Automation skill for managing Sharing Vision Jakarta logbooks (timesheets). Use when the user needs to fill logbooks, check timesheet entries, log work activities, manage projects, or search for tools/projects in SV Jakarta system. Triggers on phrases like "isi logbook", "fill timesheet", "log my work", "cek logbook", "SV Jakarta timesheet".
---

# SV Logbook Skill

## When to use this skill
Use this skill when the user needs to:
- Fill out daily or batch logbooks (timesheets).
- Check previous logbook entries or presence history.
- View or manage projects and use cases.
- Search for valid tools or projects.

## Prerequisites
This skill authenticates to SV Jakarta timesheet service. Ensure `.env` is configured (see `.env.example`).

## User Preferences

**Important:** First read `/root/.openclaw/workspace/sv-logbook-skill-agent/references/user-preferences.md` if it exists. This file contains user-specific defaults for:
- Default project/tool selection
- Default work mode (WFH/WFO)
- Typical activity descriptions

## Tools (via script)

All scripts must be run from the project directory with the virtual environment:
```bash
cd /root/.openclaw/workspace/sv-logbook-skill-agent && .venv/bin/python -m scripts.<script_name>
```

### Metadata

| Script | Description |
|--------|-------------|
| `python -m scripts.get_metadata [--type all\|projects\|tools\|progress] [--search <pattern>]` | Fetch lookup data for tools, projects, progress types |

### Logbook

| Script | Description |
|--------|-------------|
| `python -m scripts.list_logbook` | List all logbook entries (returns full JSON array) |
| `python -m scripts.list_dates --start YYYY-MM-DD --end YYYY-MM-DD` | List entries in date range |
| `python -m scripts.list_dates --missing --start YYYY-MM-DD --end YYYY-MM-DD [--exclude-weekends] [--exclude-holidays]` | Find dates without logbook entries |
| `python -m scripts.add_logbook_batch` | Add multiple logbook entries (stdin JSON) |
| `python -m scripts.edit_logbook` | Edit existing logbook entry (stdin JSON with `fid`) |

**Quick commands (run from project directory with `.venv`):**

```bash
# Get last logbook entry
.venv/bin/python -c "
import asyncio, json
from scripts.list_logbook import async_business_logic
r = asyncio.run(async_business_logic({}))
e = r.get('data', [{}])[0] if r else {}
print(f\"Last entry: {e.get('selected_date', 'N/A').split('T')[0]} | {e.get('project', 'N/A')} | {e.get('work_mode', 'N/A')}\")
"

# Find missing dates this month (exclude weekends + holidays)
.venv/bin/python -m scripts.list_dates --missing --start 2026-03-01 --end 2026-03-31 --exclude-weekends --exclude-holidays
```

### Project

| Script | Description |
|--------|-------------|
| `python -m scripts.list_project` | List projects |
| `python -m scripts.add_project` | Add new project (stdin JSON) |
| `python -m scripts.edit_project` | Edit existing project (stdin JSON with `fid`) |

## Domain Knowledge

### Search-First Protocol
**CRITICAL:** The metadata list can be extremely large (over 300KB).
1. **NEVER** assume a tool or project is missing just because you don't see it in a truncated list.
2. **ALWAYS** use the `--search` flag to verify existence (e.g., `--search Dataiku`).
3. Match the `fid` exactly from the search results.

### Work Modes
- `WFH`, `WFO`, `WFA`, `Workshop`, `Leave (Cuti)`, `Leave (Sakit)`.

## Safety & Constraints
- Always use the `fid` (Friendly ID) for updates and tool/project references.
- Dates must be `YYYY-MM-DD`.
- `current_team` and `user_id` are automatically handled by the session.
- Session is encrypted and stored locally at `~/.sv_logbook/session.enc`.
- All scripts require the `.venv` virtual environment in the project directory.