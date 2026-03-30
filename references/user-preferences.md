# User Preferences for SV Logbook

This file contains user-specific defaults for filling logbooks.

## Default Values

| Field | Default | Notes |
|-------|---------|-------|
| Work Mode | `WFO` | Unless user specifies otherwise |
| Progress | `1` | Use percentage (e.g., `50%`) if continuation of previous activity |
| Next Activities | `-` | Unless user mentions upcoming activities |

## Activity Description Rules

**Transform user input into formal, clear sentences:**

| User says | Formal activity |
|-----------|-----------------|
| "fix bug di dataiku" | "Bugfixing: memperbaiki bug pada Dataiku" |
| "meeting sama tim" | "Meeting: koordinasi dengan tim" |
| "presentasi ke klien" | "Presentasi: demo ke klien" |
| "explore data hue" | "Eksplorasi data menggunakan HUE" |
| "scripting cml" | "Scripting menggunakan CML" |

**Guidelines:**
- Use formal Bahasa Indonesia
- Be specific and clear
- Capitalize first letter
- No abbreviations unless commonly known

## Tools

| Purpose | Tool Name | FID |
|---------|-----------|-----|
| Presentasi | Microsoft PowerPoint | `31862f8d-de8e-4c0f-9100-c886ddbb5b53` |
| Scripting | CML | `6da08da7-3216-4952-a8df-4ff4e8331f10` |
| Explore data | HUE | `62006261-2fc4-4652-9d55-bb5eac45b94b` |
| Meeting | Microsoft Teams | `d22094d7-f0b6-4689-9246-d2acb8af663f` |
| Scripting + Explore (Dataiku) | Dataiku | `4585fb7b-2150-4254-b83e-8f85ab81f4f8` |

## Projects

| Project Name | FID |
|--------------|-----|
| (add your commonly used projects here) | |

## Quick Reference JSON Example

```json
{
  "date": "2026-03-30",
  "project_fid": "<project-fid>",
  "tool_fid": "<tool-fid>",
  "work_mode": "WFO",
  "progress": 1,
  "activity": "Formal activity description here",
  "next_activities": "-"
}
```

## Work Modes

- `WFH` - Work From Home
- `WFO` - Work From Office
- `WFA` - Work From Anywhere
- `Workshop`
- `Leave (Cuti)`
- `Leave (Sakit)`

## Notes

- Duration is in hours
- Use `get_metadata --search <name>` to find FIDs for projects/tools not listed