"""
GeoJSON writer for individual industries/companies.
"""

import json
from pathlib import Path
from datetime import datetime
from config import STATE_DIR, COMBINED_GEOJSON


def _make_feature(place: dict, query_used: str, district: str, state: str) -> dict:
    """Convert an Ola Maps place prediction into a GeoJSON Feature for an industry."""
    geometry = place.get("geometry", {})
    location = geometry.get("location", {})

    lat = location.get("lat", 0)
    lng = location.get("lng", 0)

    # Get name
    sf = place.get("structured_formatting", {})
    name = place.get("name", sf.get("main_text", "Unknown"))

    # Get address / description
    address = place.get("formatted_address", place.get("description", ""))

    # place_id or reference
    place_id = place.get("place_id", place.get("reference", ""))
    
    # Types/category
    types = place.get("types", [])

    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lng, lat]
        },
        "properties": {
            "name": name,
            "place_id": place_id,
            "address": address,
            "district": district,
            "state": state,
            "category": types,
            "description": address,  # usually contains context of what it does based on Ola map structured text
            "query_used": query_used,
            "fetched_at": datetime.now().isoformat()
        }
    }


def load_state_geojson(state: str) -> dict:
    """Load existing GeoJSON for a state."""
    filepath = STATE_DIR / f"{state.replace(' ', '_')}.geojson"
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "type": "FeatureCollection",
        "features": []
    }


def get_existing_place_ids(state: str) -> set:
    """Get set of place_ids already saved for a state."""
    data = load_state_geojson(state)
    return {
        f["properties"]["place_id"]
        for f in data.get("features", [])
        if f.get("properties", {}).get("place_id")
    }


def save_places_to_state(
    state: str,
    places: list[dict],
    query_used: str,
    district: str
) -> int:
    """
    Append new industries to a state's GeoJSON file.
    Deduplicates by place_id.
    """
    filepath = STATE_DIR / f"{state.replace(' ', '_')}.geojson"

    # Load existing
    data = load_state_geojson(state)
    existing_ids = {
        f["properties"]["place_id"]
        for f in data["features"]
        if f["properties"].get("place_id")
    }

    new_count = 0
    for place in places:
        place_id = place.get("place_id", place.get("reference", ""))
        if place_id and place_id in existing_ids:
            continue  # Skip duplicate

        feature = _make_feature(place, query_used, district, state)
        data["features"].append(feature)
        if place_id:
            existing_ids.add(place_id)
        new_count += 1

    # Write back
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return new_count


def merge_all_states() -> Path:
    """Merge all per-state GeoJSON files into one combined file."""
    combined = {
        "type": "FeatureCollection",
        "features": [],
        "properties": {
            "name": "Specific Industries of India",
            "generated_at": datetime.now().isoformat(),
            "source": "Ola Maps Autocomplete API"
        }
    }

    for filepath in sorted(STATE_DIR.glob("*.geojson")):
        with open(filepath, "r", encoding="utf-8") as f:
            state_data = json.load(f)
            combined["features"].extend(state_data.get("features", []))

    output_path = COMBINED_GEOJSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Combined GeoJSON saved: {output_path}")
    print(f"  Total companies/industries: {len(combined['features'])}")
    return output_path


def get_all_stats() -> dict:
    """Get statistics across all saved GeoJSON files."""
    stats = {"total": 0, "states": {}}

    for filepath in sorted(STATE_DIR.glob("*.geojson")):
        state_name = filepath.stem.replace("_", " ")
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            count = len(data.get("features", []))
            stats["states"][state_name] = count
            stats["total"] += count

    return stats
