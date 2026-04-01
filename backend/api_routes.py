"""
API routes for serving GeoJSON data to the frontend.
"""

import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from config import GEOJSON_DIR, PROGRESS_FILE
from geojson_writer import get_all_stats, load_state_geojson, merge_all_states

router = APIRouter(prefix="/api")


@router.get("/status")
async def get_status():
    """Return current fetching progress."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            progress = json.load(f)
        return progress
    return {
        "completed_districts": [],
        "total_found": 0,
        "total_requests": 0,
        "last_updated": None
    }


@router.get("/data/states")
async def list_states():
    """List all states with their feature counts."""
    stats = get_all_stats()
    states = []
    for state_name, count in sorted(stats["states"].items()):
        states.append({
            "name": state_name,
            "count": count,
            "file": f"{state_name.replace(' ', '_')}.geojson"
        })
    return {
        "total": stats["total"],
        "states": states
    }


@router.get("/data/geojson")
async def get_state_geojson(state: str = None):
    """
    Return GeoJSON for a specific state.
    If no state specified, returns combined GeoJSON.
    """
    if state:
        state_file = GEOJSON_DIR / f"{state.replace(' ', '_')}.geojson"
        if not state_file.exists():
            raise HTTPException(status_code=404, detail=f"No data for state: {state}")
        with open(state_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    else:
        # Return combined
        combined_file = GEOJSON_DIR / "all_india_industrial_areas.geojson"
        if not combined_file.exists():
            # Auto-merge on first request
            merge_all_states()
        if combined_file.exists():
            with open(combined_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return JSONResponse(content=data)
        raise HTTPException(status_code=404, detail="No data available. Run the fetcher first.")


@router.get("/data/stats")
async def get_stats():
    """Return summary statistics."""
    stats = get_all_stats()

    progress = {}
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            progress = json.load(f)

    return {
        "total_places": stats["total"],
        "states_covered": len(stats["states"]),
        "districts_completed": len(progress.get("completed_districts", [])),
        "api_requests_used": progress.get("total_requests", 0),
        "last_updated": progress.get("last_updated"),
        "per_state": stats["states"]
    }


@router.post("/data/merge")
async def trigger_merge():
    """Merge all state GeoJSON files into combined file."""
    output_path = merge_all_states()
    stats = get_all_stats()
    return {
        "message": "Merged successfully",
        "output_file": str(output_path),
        "total_features": stats["total"]
    }
