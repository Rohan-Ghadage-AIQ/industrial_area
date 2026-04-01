# India Industrial Area Explorer

An interactive map-based web application to explore industrial areas, estates, and manufacturing hubs across all districts of India. The project uses the **Ola Krutrim Places API** to intelligently search and fetch industrial zones and displays them on a sleek, dark-themed Leaflet map.

## Key Features

- **Comprehensive Data Fetching:** CLI-based Python script (`fetcher.py`) systematically queries the Ola Maps Autocomplete API for over 700 districts across India.
- **Smart Querying:** Employs multiple industry-specific search queries (like "MIDC", "industrial estate", "factory area") per district to maximize coverage.
- **Interactive Map Visualization:** A responsive React frontend powered by `react-leaflet` and `leaflet.markercluster` renders the locations with custom styling and clustered markers.
- **Hover Interactions:** Automatic tooltips displaying names, addresses, and geographic coordinates when hovering over markers.
- **State Filtering:** An intuitive sidebar interface allows filtering points of interest by specific states.
- **FastAPI Backend:** A lightweight asynchronous Python backend serves the aggregated GeoJSON data dynamically.

## Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- An Ola Krutrim API Key (`KRUTRIM_API_KEY`)

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root containing your API credentials:
   ```env
   KRUTRIM_API_KEY=your_api_key_here
   KRUTRIM_PROJECT_ID=your_project_id_here
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### 3. Frontend Setup
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. The frontend will be available at `http://localhost:5173`.

### 4. Fetching Data
Data is not included natively and requires live fetching. Open another terminal in the backend directory:
```bash
# Fetch data for a specific state
python fetcher.py --state "Maharashtra"

# Or fetch data for all states
python fetcher.py
```
The script resumes automatically if interrupted.

## Architecture & Codebase

Please refer to the [ARCHITECTURE.md](ARCHITECTURE.md) document for an in-depth explanation of the folder structure, data flow, and components.
