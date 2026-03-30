# User Preferences for SV Logbook

This file contains user-specific defaults for filling logbooks.
Edit this file to customize your defaults.

## Default Work Mode

Default work mode when not specified:
- `WFH` - Work From Home
- `WFO` - Work From Office
- `WFA` - Work From Anywhere

```
default_work_mode: WFH
```

## Default Project/Tool

Project and tool IDs for quick reference. Use `get_metadata --search <name>` to find IDs.

### Projects

| Project Name | FID |
|--------------|-----|
| (add your commonly used projects here) | |

### Tools

| Tool Name | FID |
|-----------|-----|
| (add your commonly used tools here) | |

## Activity Templates

Pre-defined activity descriptions for common tasks:

### Development
- "Development: [task description]"
- "Code review: [PR/component]"
- "Bug fixing: [issue description]"

### Meetings
- "Team meeting: [topic]"
- "Client call: [client name]"

### Research
- "Research: [topic]"
- "Learning: [course/material]"

## Example Logbook Entry

```json
{
  "date": "2026-03-30",
  "project_fid": "your-project-fid",
  "tool_fid": "your-tool-fid",
  "work_mode": "WFH",
  "activity": "Development: feature implementation",
  "duration": 8
}
```

## Notes

- FIDs (Friendly IDs) can be found using: `python -m scripts.get_metadata --type tools --search <name>`- Work modes: WFH, WFO, WFA, Workshop, Leave (Cuti), Leave (Sakit)
- Duration is in hours