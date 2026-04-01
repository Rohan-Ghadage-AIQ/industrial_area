"""
Configuration for the Industrial Area Fetcher.
Loads API credentials and defines constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# ── Ola Maps API ──────────────────────────────────────────────
API_KEY = os.getenv("KRUTRIM_API_KEY", "")
PROJECT_ID = os.getenv("KRUTRIM_PROJECT_ID", "")
API_BASE_URL = "https://api.olamaps.io"
AUTOCOMPLETE_ENDPOINT = f"{API_BASE_URL}/places/v1/autocomplete"

# ── Data Paths ────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / "data"
DISTRICTS_FILE = DATA_DIR / "districts.json"
PROGRESS_FILE = DATA_DIR / "progress.json"
GEOJSON_DIR = DATA_DIR / "geojson"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
GEOJSON_DIR.mkdir(parents=True, exist_ok=True)

# ── Fetcher Settings ─────────────────────────────────────────
REQUEST_DELAY_SECONDS = 0.25          # Delay between API calls (250ms)
SEARCH_RADIUS_METERS = 50000          # 50km radius per district search
MAX_RETRIES = 3                        # Retries on failure
RETRY_BACKOFF_FACTOR = 2               # Exponential backoff multiplier

# ── Validation ────────────────────────────────────────────────
def validate_config():
    """Validate that required config values are set."""
    if not API_KEY:
        raise ValueError(
            "KRUTRIM_API_KEY is not set. "
            "Please add it to the .env file in the project root."
        )
    print(f"✓ API Key loaded (ends with ...{API_KEY[-4:]})")
    print(f"✓ Data directory: {DATA_DIR}")
    print(f"✓ GeoJSON output: {GEOJSON_DIR}")
