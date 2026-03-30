# User Preferences for SV Logbook

This file contains user-specific defaults for filling logbooks.

## Default Work Mode

```
default_work_mode: WFH
```

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

## Activity Templates

### Presentasi
- "Presentasi: [topic/description]"

### Scripting
- "Scripting: [task description]"
- "Scripting Dataiku: [task description]"

### Explore Data
- "Explore data: [dataset/description]"
- "Explore data Dataiku: [dataset/description]"

### Meeting
- "Meeting: [topic/participants]"

## Quick Reference JSON Examples

### PowerPoint Entry
```json
{
  "tool_fid": "31862f8d-de8e-4c0f-9100-c886ddbb5b53",
  "activity": "Presentasi: [description]"
}
```

### CML Entry
```json
{
  "tool_fid": "6da08da7-3216-4952-a8df-4ff4e8331f10",
  "activity": "Scripting: [description]"
}
```

### HUE Entry
```json
{
  "tool_fid": "62006261-2fc4-4652-9d55-bb5eac45b94b",
  "activity": "Explore data: [description]"
}
```

### Microsoft Teams Entry
```json
{
  "tool_fid": "d22094d7-f0b6-4689-9246-d2acb8af663f",
  "activity": "Meeting: [description]"
}
```

### Dataiku Entry
```json
{
  "tool_fid": "4585fb7b-2150-4254-b83e-8f85ab81f4f8",
  "activity": "Scripting Dataiku / Explore data: [description]"
}
```

## Notes

- Work modes: WFH, WFO, WFA, Workshop, Leave (Cuti), Leave (Sakit)
- Duration is in hours
- Use `get_metadata --search <name>` to find more FIDs