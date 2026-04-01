import os
from pathlib import Path
from dotenv import load_dotenv

# Paths
BASE_DIR = Path(__file__).parent.resolve()
ROOT_DIR = BASE_DIR.parent
DATA_DIR = BASE_DIR / "data"
GEOJSON_DIR = DATA_DIR / "geojson"
STATE_DIR = GEOJSON_DIR / "state"

DISTRICTS_FILE = BASE_DIR.parent / "backend" / "data" / "districts.json"
PROGRESS_FILE = DATA_DIR / "fetch_progress.json"
COMBINED_GEOJSON = GEOJSON_DIR / "all_india_specific_industries.geojson"

# Ensure directories exist
STATE_DIR.mkdir(parents=True, exist_ok=True)

# Load Environment Variables from root directory
load_dotenv(ROOT_DIR / ".env")

API_KEY = os.getenv("KRUTRIM_API_KEY")
PROJECT_ID = os.getenv("KRUTRIM_PROJECT_ID")

# Ola Maps endpoints
AUTOCOMPLETE_ENDPOINT = "https://api.olamaps.io/places/v1/autocomplete"

# Fetcher settings
REQUEST_DELAY_SECONDS = 0.5
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 2

def validate_config():
    """Verify that required API keys and constants exist."""
    print("✓ Loaded config")
    if not API_KEY:
        print("✗ Error: KRUTRIM_API_KEY not found in .env")
        exit(1)
    
    masked_key = f"...{API_KEY[-4:]}" if len(API_KEY) > 4 else "***"
    print(f"✓ API Key loaded (ends with {masked_key})")
    print(f"✓ Output directory: {GEOJSON_DIR}")
