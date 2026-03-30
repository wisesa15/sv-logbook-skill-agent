---
name: sv-logbook
description: Automation skill for managing Sharing Vision Jakarta logbooks, presences, and projects.
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

## Tools (via script)

### Metadata

| Script | Description |
|--------|-------------|
| `python -m scripts.get_metadata [--type all\|projects\|tools\|progress] [--search <pattern>]` | Fetch lookup data for tools, projects, progress types |

### Logbook

| Script | Description |
|--------|-------------|
| `python -m scripts.list_logbook` | List logbook entries for current user |
| `python -m scripts.add_logbook_batch` | Add multiple logbook entries (stdin JSON) |
| `python -m scripts.edit_logbook` | Edit existing logbook entry (stdin JSON with `fid`) |

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