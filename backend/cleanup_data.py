import json
import math
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DISTRICTS_FILE = DATA_DIR / "districts.json"
GEOJSON_DIR = DATA_DIR / "geojson"

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two lat/lng points."""
    R = 6371.0  # Earth radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def perform_cleanup():
    # Load districts lookup
    with open(DISTRICTS_FILE, 'r', encoding='utf-8') as f:
        districts = json.load(f)
    
    # Create lookup dictionary {(state, district): (lat, lng)}
    district_coords = {}
    for d in districts:
        district_coords[(d['state'], d['district'])] = (d['lat'], d['lng'])

    total_removed = 0
    total_kept = 0
    
    for geojson_file in GEOJSON_DIR.glob("*.geojson"):
        if geojson_file.name == "all_india_industrial_areas.geojson":
            continue
            
        with open(geojson_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        original_count = len(data.get('features', []))
        if original_count == 0:
            continue
            
        valid_features = []
        for feature in data.get('features', []):
            props = feature['properties']
            state = props.get('state')
            district = props.get('district')
            coords = feature['geometry']['coordinates']
            lng, lat = coords[0], coords[1]
            
            ref_coords = district_coords.get((state, district))
            
            if ref_coords:
                ref_lat, ref_lng = ref_coords
                distance = haversine_distance(lat, lng, ref_lat, ref_lng)
                
                # If distance is more than ~150km (generous radius for large districts), discard it
                if distance <= 150.0:
                    valid_features.append(feature)
            else:
                # If district not found (rare), keep it by default
                valid_features.append(feature)
                
        # Save back
        data['features'] = valid_features
        with open(geojson_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        removed = original_count - len(valid_features)
        total_removed += removed
        total_kept += len(valid_features)
        
        if removed > 0:
            print(f"[{geojson_file.stem}] Kept: {len(valid_features)} | Removed: {removed}")

    print(f"\nCleanup Complete.")
    print(f"Total Places Kept: {total_kept}")
    print(f"Total Out-of-Bounds Removed: {total_removed}")

if __name__ == "__main__":
    print("Starting cleanup of out-of-bounds locations...")
    perform_cleanup()
