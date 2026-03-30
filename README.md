# SV Logbook Skill Agent

Automation client for managing Sharing Vision Jakarta logbooks (timesheets).

## Features

- List logbook entries
- Find missing logbook dates (exclude weekends & holidays)
- Quick lookup for last entry
- Add/edit logbook entries
- Session management with encrypted tokens
- Indonesian holiday calendar (2024-2026)

## Prerequisites

- Python 3.10+
- pip

## Installation

```bash
# Clone the repository
git clone https://github.com/wisesa15/sv-logbook-skill-agent.git
cd sv-logbook-skill-agent

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
.venv/bin/playwright install chromium
```

## Configuration

Create a `.env` file in the project root:

```env
# SV Jakarta Timesheet credentials
LOGIN_URL=https://new-timesheet.sharingvisionjakarta.com/api/auth/login
EMAIL=your.email@example.com
PASS=your_password_here
REFERER_URL=https://new-timesheet.sharingvisionjakarta.com
ORIGIN_URL=https://new-timesheet.sharingvisionjakarta.com
DOMAIN=new-timesheet.sharingvisionjakarta.com
```

**Important:** Never commit `.env` to version control. It's already in `.gitignore`.

## Usage

All scripts must be run from the project directory with the virtual environment activated.

```bash
# Activate virtual environment first
source .venv/bin/activate

# Get last logbook entry
python -m scripts.last_entry

# Find missing dates this month
python -m scripts.list_dates --missing --start 2026-03-01 --end 2026-03-31 --exclude-weekends --exclude-holidays

# Search for tools/projects
python -m scripts.get_metadata --type tools --search Dataiku

# List all logbook entries
python -m scripts.list_logbook
```

## Available Scripts

| Script | Description |
|--------|-------------|
| `last_entry` | Get the last logbook entry |
| `list_logbook` | List all logbook entries |
| `list_dates` | List entries in date range / find missing dates |
| `get_metadata` | Search tools, projects, progress types |
| `add_logbook_batch` | Add multiple logbook entries |
| `edit_logbook` | Edit existing logbook entry |

### Examples

```bash
# Get last 5 logbook entries
python -m scripts.last_entry --count 5

# Get just the date of last entry
python -m scripts.last_entry --date-only

# Find missing dates in March (exclude weekends & holidays)
python -m scripts.list_dates --missing --start 2026-03-01 --end 2026-03-31 --exclude-weekends --exclude-holidays

# List entries in date range
python -m scripts.list_dates --start 2026-03-01 --end 2026-03-15

# Search for tools containing "Dataiku"
python -m scripts.get_metadata --type tools --search Dataiku

# Search for projects
python -m scripts.get_metadata --type projects --search "Household"
```

## User Preferences

Edit `references/user-preferences.md` to set your defaults:

- Default work mode (WFO/WFH)
- Frequently used tools/projects FIDs
- Activity description templates

## Session Management

Session tokens are encrypted and stored locally at `~/.sv_logbook/session.enc`. The encryption key is derived from your password, so:

- Password change = session invalid (must re-login)
- Session file is portable between machines with same credentials

## Security

- Credentials stored in `.env` (not committed to git)
- Session tokens encrypted with Fernet (PBKDF2-derived key from password)
- Never share `.env` or `session.enc` files

## Project Structure

```
sv-logbook-skill-agent/
├── core/
│   ├── api/
│   │   └── logbook_service.py    # API client
│   ├── config.py                  # Configuration & Fernet key
│   └── session_manager.py         # Session & auth management
├── scripts/
│   ├── get_metadata.py            # Search tools/projects
│   ├── last_entry.py              # Get last logbook entry
│   ├── list_dates.py              # List/missing dates
│   ├── list_logbook.py            # List all entries
│   ├── add_logbook_batch.py       # Batch add entries
│   └── edit_logbook.py            # Edit entry
├── references/
│   └── user-preferences.md        # User-specific defaults
├── .env.example                   # Environment template
├── requirements.txt               # Python dependencies
├── SKILL.md                       # Skill documentation
└── README.md                      # This file
```

## Integrating with AI Agents

If using with an AI agent framework (like OpenClaw), point your agent to read `SKILL.md` for instructions on how to use this skill.

The agent should:
1. Read `SKILL.md` for available commands and usage patterns
2. Read `references/user-preferences.md` for user-specific defaults
3. Run scripts from this directory with `.venv/bin/python`

## Troubleshooting

### Login failed
- Check `.env` credentials
- Ensure `LOGIN_URL` is correct
- Try deleting `~/.sv_logbook/session.enc` to force re-login

### Module not found
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### Playwright browser error
- Run `.venv/bin/playwright install chromium`

## License

MIT