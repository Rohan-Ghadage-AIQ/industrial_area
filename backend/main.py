"""
FastAPI server — serves GeoJSON data to the React frontend.

Usage:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_routes import router

app = FastAPI(
    title="Industrial Area Fetcher API",
    description="API for serving industrial area GeoJSON data",
    version="1.0.0"
)

# CORS — allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "name": "Industrial Area Fetcher API",
        "version": "1.0.0",
        "endpoints": {
            "status": "/api/status",
            "states": "/api/data/states",
            "geojson": "/api/data/geojson?state=Maharashtra",
            "geojson_all": "/api/data/geojson",
            "stats": "/api/data/stats",
            "merge": "POST /api/data/merge"
        }
    }
    