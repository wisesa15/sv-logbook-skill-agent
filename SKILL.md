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

## Tools

### 1. `get_metadata` (via script)
- **Description**: Fetches lookup data for tools, projects, and progress types.
- **Usage**: `python -m scripts.get_metadata [--type tools|projects|progress] [--search <pattern>]`
- **Example**: `python -m scripts.get_metadata --type tools --search Dataiku`

### 2. `list_tools` / `list_projects` (via MCP)
- **Description**: Quickly find tools or projects by name.
- **Usage**: Call MCP tool `list_tools(search="dataiku")` or `list_projects(search="GKG")`.

### 3. `list_logbooks` (via MCP/script)
- **Description**: Retrieves logbook entries for the current user.
- **Usage**: `python -m scripts.list_logbook [--id <fid>]`

### 4. `submit_logbook_batch` (via MCP/script)
- **Description**: Adds multiple logbook entries in one call.
- **Usage**: `echo '[<LogbookEntry>]' | python -m scripts.add_logbook_batch`

## Domain Knowledge

### Search-First Protocol
**CRITICAL:** The metadata list can be extremely large (over 300KB).
1.  **NEVER** assume a tool or project is missing just because you don't see it in a truncated list.
2.  **ALWAYS** use the `search` parameter or `--search` flag to verify the existence of a tool (e.g., "Dataiku", "Notion", "Slack").
3.  Match the `fid` exactly from the search results.

### Work Modes
- `WFH`, `WFO`, `WFA`, `Workshop`, `Leave (Cuti)`, `Leave (Sakit)`.

## Safety & Constraints
- Always use the `fid` (Friendly ID) for updates and tool/project references.
- Dates must be `YYYY-MM-DD`.
- `current_team` and `user_id` are automatically handled by the scripts via the session.
