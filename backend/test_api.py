"""Quick test to find the best Ola Maps endpoint for industrial area search."""

import httpx
import json
import config

config.validate_config()

headers = {
    "Referer": "http://localhost:5173",
    "Origin": "http://localhost:5173",
}

client = httpx.Client()
output = []

# Test 1: Autocomplete API
output.append("TEST 1: Autocomplete — 'industrial area Pune Maharashtra'")
r = client.get(
    "https://api.olamaps.io/places/v1/autocomplete",
    params={
        "input": "industrial area Pune Maharashtra",
        "api_key": config.API_KEY,
    },
    headers=headers,
    timeout=30,
)
data = r.json()
output.append(f"Status: {data.get('status')}")
preds = data.get("predictions", [])
output.append(f"Results: {len(preds)}")
for p in preds:
    sf = p.get("structured_formatting", {})
    name = sf.get("main_text", p.get("description", "?"))
    desc = p.get("description", "")
    geom = p.get("geometry", {}).get("location", {})
    output.append(f"  Name: {name}")
    output.append(f"  Desc: {desc}")
    output.append(f"  Lat: {geom.get('lat','?')}, Lng: {geom.get('lng','?')}")
    output.append(f"  Types: {p.get('types', [])}")
    output.append("")

# Test 2: Nearby Search
output.append("\nTEST 2: Nearby Search — types='industrial' near Pune (18.52,73.85)")
r2 = client.get(
    "https://api.olamaps.io/places/v1/nearbysearch",
    params={
        "location": "18.52,73.85",
        "radius": 50000,
        "types": "industrial",
        "api_key": config.API_KEY,
    },
    headers=headers,
    timeout=30,
)
data2 = r2.json()
output.append(f"Status: {data2.get('status')}")
results2 = data2.get("results", data2.get("predictions", []))
output.append(f"Results: {len(results2)}")
for r in results2[:5]:
    name = r.get("name", "?")
    geom = r.get("geometry", {}).get("location", {})
    output.append(f"  Name: {name}, Lat: {geom.get('lat','?')}, Lng: {geom.get('lng','?')}")

# Test 3: Text Search
output.append("\nTEST 3: Text Search — 'MIDC Pune'")
r3 = client.get(
    "https://api.olamaps.io/places/v1/textsearch",
    params={
        "input": "MIDC Pune",
        "location": "18.52,73.85",
        "radius": 50000,
        "api_key": config.API_KEY,
    },
    headers=headers,
    timeout=30,
)
data3 = r3.json()
output.append(f"Status: {data3.get('status')}")
results3 = data3.get("results", data3.get("predictions", []))
output.append(f"Results: {len(results3)}")

# Test 4: Autocomplete with different queries
for query in ["MIDC", "industrial estate", "factory area Mumbai"]:
    output.append(f"\nTEST 4: Autocomplete — '{query}'")
    r4 = client.get(
        "https://api.olamaps.io/places/v1/autocomplete",
        params={
            "input": query,
            "api_key": config.API_KEY,
        },
        headers=headers,
        timeout=30,
    )
    data4 = r4.json()
    preds4 = data4.get("predictions", [])
    output.append(f"Status: {data4.get('status')}, Results: {len(preds4)}")
    for p in preds4[:3]:
        sf = p.get("structured_formatting", {})
        name = sf.get("main_text", p.get("description", "?"))
        geom = p.get("geometry", {}).get("location", {})
        output.append(f"  {name} | lat={geom.get('lat','?')}, lng={geom.get('lng','?')}")

client.close()

# Write output
result = "\n".join(output)
with open("test_output.txt", "w", encoding="utf-8") as f:
    f.write(result)
print("Done! Check test_output.txt")
