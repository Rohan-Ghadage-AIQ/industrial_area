"""
Industrial Area Fetcher — CLI Script
Fetches industrial areas across India using Ola Maps Places API.

Usage:
    python fetcher.py                  # Fetch all states (resumes from last checkpoint)
    python fetcher.py --state "Maharashtra"  # Fetch a specific state only
    python fetcher.py --stats          # Show current progress stats
    python fetcher.py --merge          # Merge all state GeoJSON into combined file
    python fetcher.py --reset          # Reset progress (start fresh)
"""

import json
import time
import argparse
import sys
from datetime import datetime
from pathlib import Path

import httpx

import config
from geojson_writer import save_places_to_state, merge_all_states, get_all_stats


# ── Progress Tracking ─────────────────────────────────────────

def load_progress() -> dict:
    """Load fetching progress from disk."""
    if config.PROGRESS_FILE.exists():
        with open(config.PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "completed_districts": [],
        "total_found": 0,
        "total_requests": 0,
        "last_updated": None,
        "errors": []
    }


def save_progress(progress: dict):
    """Save fetching progress to disk."""
    progress["last_updated"] = datetime.now().isoformat()
    with open(config.PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def reset_progress():
    """Reset progress file."""
    if config.PROGRESS_FILE.exists():
        config.PROGRESS_FILE.unlink()
    print("✓ Progress reset. Will start fresh on next run.")


# ── Districts Data ────────────────────────────────────────────

def load_districts() -> list[dict]:
    """Load the districts dataset."""
    if not config.DISTRICTS_FILE.exists():
        print(f"✗ Districts file not found: {config.DISTRICTS_FILE}")
        print("  Run: python generate_districts.py")
        sys.exit(1)

    with open(config.DISTRICTS_FILE, "r", encoding="utf-8") as f:
        districts = json.load(f)

    print(f"✓ Loaded {len(districts)} districts")
    return districts


# ── API Calls ─────────────────────────────────────────────────

# Query templates — multiple per district for better coverage
QUERY_TEMPLATES = [
    "industrial area {district}",
    "industrial estate {district} {state}",
    "MIDC {district}",               # Maharashtra-specific but works elsewhere too
    "factory area {district}",
    "manufacturing hub {district}",
]

HEADERS = {
    "Referer": "http://localhost:5173",
    "Origin": "http://localhost:5173",
}


def search_autocomplete(
    client: httpx.Client,
    query: str,
) -> list[dict]:
    """
    Call Ola Maps Autocomplete API.
    Returns list of prediction results.
    """
    params = {
        "input": query,
        "api_key": config.API_KEY,
    }

    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            response = client.get(
                config.AUTOCOMPLETE_ENDPOINT,
                params=params,
                headers=HEADERS,
                timeout=30
            )

            if response.status_code == 429:
                wait = config.RETRY_BACKOFF_FACTOR ** attempt * 2
                print(f"  ⚠ Rate limited. Waiting {wait}s...")
                time.sleep(wait)
                continue

            if response.status_code != 200:
                print(f"  ✗ HTTP {response.status_code}: {response.text[:200]}")
                if attempt < config.MAX_RETRIES:
                    time.sleep(config.RETRY_BACKOFF_FACTOR ** attempt)
                    continue
                return []

            data = response.json()
            status = data.get("status", "")

            if status in ("ok", "OK"):
                return data.get("predictions", [])
            elif status in ("zero_results", "ZERO_RESULTS"):
                return []
            else:
                return data.get("predictions", [])

        except httpx.TimeoutException:
            print(f"  ⚠ Timeout (attempt {attempt}/{config.MAX_RETRIES})")
            if attempt < config.MAX_RETRIES:
                time.sleep(config.RETRY_BACKOFF_FACTOR ** attempt)
        except Exception as e:
            print(f"  ✗ Error: {e}")
            if attempt < config.MAX_RETRIES:
                time.sleep(config.RETRY_BACKOFF_FACTOR ** attempt)

    return []


def _is_industrial_result(prediction: dict) -> bool:
    """Filter to keep only results that look like industrial areas."""
    name = prediction.get("structured_formatting", {}).get("main_text", "").lower()
    desc = prediction.get("description", "").lower()
    types = [t.lower() for t in prediction.get("types", [])]
    combined = f"{name} {desc}"

    # Positive keywords — matches industrial areas
    industrial_keywords = [
        "industrial", "midc", "gidc", "riico", "sidco", "sipcot",
        "iie", "factory", "manufacturing", "warehouse", "estate",
        "sez", "epz", "special economic", "industrial park",
        "industrial cluster", "industrial hub", "industrial zone",
    ]

    if any(kw in combined for kw in industrial_keywords):
        return True

    # Also check types
    industrial_types = ["industrial", "warehouse", "storage", "factory"]
    if any(t in types for t in industrial_types):
        return True

    return False


# ── Main Fetcher Logic ────────────────────────────────────────

def fetch_district(
    client: httpx.Client,
    district: dict,
    progress: dict
) -> int:
    """
    Fetch industrial areas for a single district using multiple queries.
    Returns count of new places found.
    """
    state = district["state"]
    dist_name = district["district"]
    district_key = f"{state}|{dist_name}"

    if district_key in progress["completed_districts"]:
        return 0

    all_results = []

    for template in QUERY_TEMPLATES:
        query = template.format(district=dist_name, state=state)
        results = search_autocomplete(client, query)
        progress["total_requests"] += 1
        time.sleep(config.REQUEST_DELAY_SECONDS)

        # Filter to keep industrial-looking results
        for pred in results:
            if _is_industrial_result(pred):
                all_results.append((pred, query))

    # Deduplicate by place_id / reference
    seen = set()
    unique_results = []
    for pred, query in all_results:
        pid = pred.get("place_id", pred.get("reference", ""))
        if pid and pid not in seen:
            seen.add(pid)
            unique_results.append((pred, query))

    new_count = 0
    for pred, query in unique_results:
        new_count += save_places_to_state(state, [pred], query, dist_name)

    progress["completed_districts"].append(district_key)
    progress["total_found"] += new_count

    return new_count


def fetch_all(target_state: str = None):
    """
    Main fetching loop. Iterates through all districts state-by-state.
    Resumes from last checkpoint automatically.
    """
    config.validate_config()

    districts = load_districts()
    progress = load_progress()

    # Filter by target state if specified
    if target_state:
        districts = [d for d in districts if d["state"].lower() == target_state.lower()]
        if not districts:
            print(f"✗ No districts found for state: {target_state}")
            return
        print(f"\n→ Fetching for state: {target_state} ({len(districts)} districts)")
    else:
        print(f"\n→ Fetching all India ({len(districts)} districts)")

    # Count remaining
    completed = set(progress["completed_districts"])
    remaining = [d for d in districts if f"{d['state']}|{d['district']}" not in completed]

    if not remaining:
        print("✓ All districts already fetched! Use --reset to start fresh.")
        return

    print(f"  Already completed: {len(districts) - len(remaining)}")
    print(f"  Remaining: {len(remaining)}")
    print(f"  Total found so far: {progress['total_found']}")
    print(f"  Total API requests so far: {progress['total_requests']}")
    print(f"\n{'─' * 60}")

    # Group remaining by state for display
    current_state = None

    with httpx.Client() as client:
        try:
            for i, district in enumerate(remaining, 1):
                state = district["state"]
                dist_name = district["district"]

                # Print state header
                if state != current_state:
                    current_state = state
                    state_districts = [d for d in remaining if d["state"] == state]
                    print(f"\n{'═' * 60}")
                    print(f"  STATE: {state} ({len(state_districts)} districts)")
                    print(f"{'═' * 60}")

                # Fetch
                new_count = fetch_district(client, district, progress)

                # Progress display
                status = f"  [{i}/{len(remaining)}] {dist_name}"
                if new_count > 0:
                    status += f" → +{new_count} new places"
                else:
                    status += f" → no results"
                print(status)

                # Save progress every 5 districts
                if i % 5 == 0:
                    save_progress(progress)

        except KeyboardInterrupt:
            print(f"\n\n⚠ Interrupted! Saving progress...")
        finally:
            save_progress(progress)
            print(f"\n{'─' * 60}")
            print(f"  Progress saved. Total found: {progress['total_found']}")
            print(f"  Total API requests used: {progress['total_requests']}")
            print(f"  Run again to resume from where you left off.")


def show_stats():
    """Display current fetching statistics."""
    progress = load_progress()
    stats = get_all_stats()

    print(f"\n{'═' * 60}")
    print(f"  INDUSTRIAL AREA FETCHER — STATISTICS")
    print(f"{'═' * 60}")
    print(f"  Total places found: {stats['total']}")
    print(f"  Districts completed: {len(progress.get('completed_districts', []))}")
    print(f"  API requests used: {progress.get('total_requests', 0)}")
    print(f"  Last updated: {progress.get('last_updated', 'N/A')}")
    print(f"\n  Per-state breakdown:")
    print(f"  {'─' * 40}")

    for state, count in sorted(stats["states"].items(), key=lambda x: -x[1]):
        bar = "█" * min(count, 50)
        print(f"  {state:30s} {count:5d}  {bar}")

    if not stats["states"]:
        print("  No data fetched yet.")

    print(f"{'═' * 60}")


# ── CLI ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Fetch industrial area locations across India using Ola Maps API"
    )
    parser.add_argument(
        "--state", type=str, default=None,
        help="Fetch for a specific state only (e.g., 'Maharashtra')"
    )
    parser.add_argument(
        "--stats", action="store_true",
        help="Show current fetching statistics"
    )
    parser.add_argument(
        "--merge", action="store_true",
        help="Merge all state GeoJSON files into combined file"
    )
    parser.add_argument(
        "--reset", action="store_true",
        help="Reset progress and start fresh"
    )

    args = parser.parse_args()

    if args.stats:
        show_stats()
    elif args.merge:
        merge_all_states()
    elif args.reset:
        reset_progress()
    else:
        fetch_all(target_state=args.state)


if __name__ == "__main__":
    main()
