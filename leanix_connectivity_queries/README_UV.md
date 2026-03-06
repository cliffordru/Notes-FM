# LeanIX Connectivity with uv

## Setup with uv

### Install uv (if not already installed)
```powershell
# On Windows with PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Initialize and run

1. **Sync dependencies** (creates virtual environment automatically):
```powershell
uv sync
```

2. **Run the minimal Atlas script**:
```powershell
uv run get_atlas.py
```

3. **Run the full pipeline script**:
```powershell
uv run telogos_connect_leanix.py --enriched
```

### Add dependencies
```powershell
uv add package-name
```

### Run Python commands in the environment
```powershell
uv run python -c "import requests; print(requests.__version__)"
```

## Quick Start - Get Atlas Factsheet

The minimal script `get_atlas.py` connects to LeanIX and retrieves the Atlas application:

```powershell
# One command to sync dependencies and run
uv run get_atlas.py
```

This will:
- Authenticate with LeanIX
- Search for the "Atlas" application
- Display key information
- Save the full factsheet to `atlas_factsheet.json`

## Environment Variables

Set your LeanIX API token (optional, has default):
```powershell
$env:LEANIX_API_TOKEN = "your-token-here"
```

## Files

- `get_atlas.py` - Minimal script to get Atlas application factsheet
- `telogos_connect_leanix.py` - Full pipeline with data processing
- `pyproject.toml` - Project dependencies managed by uv
- `.python-version` - Python version specification
