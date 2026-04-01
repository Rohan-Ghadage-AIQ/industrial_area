import { useState, useEffect, useCallback, useRef } from 'react';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import './index.css';

import MapView from './components/MapView';
import Sidebar from './components/Sidebar';
import { fetchStates, fetchGeoJSON, fetchStats } from './api/client';

function App() {
  const [statesData, setStatesData] = useState({ total: 0, states: [] });
  const [stats, setStats] = useState(null);
  const [geojsonData, setGeojsonData] = useState(null);
  const [selectedState, setSelectedState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Load initial data
  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const [statesRes, statsRes] = await Promise.all([
        fetchStates(),
        fetchStats()
      ]);

      setStatesData(statesRes);
      setStats(statsRes);

      // Load GeoJSON (all or selected state)
      if (statesRes.total > 0) {
        const geojson = await fetchGeoJSON(selectedState);
        setGeojsonData(geojson);
      }
    } catch (err) {
      console.error('Error loading data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [selectedState]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleStateSelect = async (stateName) => {
    setSelectedState(stateName);
    try {
      setLoading(true);
      const geojson = await fetchGeoJSON(stateName);
      setGeojsonData(geojson);
    } catch (err) {
      console.error('Error loading state data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleShowAll = async () => {
    setSelectedState(null);
    try {
      setLoading(true);
      const geojson = await fetchGeoJSON(null);
      setGeojsonData(geojson);
    } catch (err) {
      console.error('Error loading all data:', err);
    } finally {
      setLoading(false);
    }
  };

  const featureCount = geojsonData?.features?.length || 0;

  return (
    <div className="app">
      <Sidebar
        statesData={statesData}
        stats={stats}
        selectedState={selectedState}
        onStateSelect={handleStateSelect}
        onShowAll={handleShowAll}
        onRefresh={loadData}
        isOpen={sidebarOpen}
      />

      <div className="map-container">
        <MapView
          geojsonData={geojsonData}
          loading={loading}
          error={error}
          selectedState={selectedState}
          onStateSelect={handleStateSelect}
        />

        {featureCount > 0 && (
          <div className="map-info-bar fade-in">
            <div className="info-item">
              <span className="info-dot"></span>
              <span>
                Showing <strong>{featureCount.toLocaleString()}</strong> industrial areas
              </span>
            </div>
            {selectedState && (
              <div className="info-item">
                <span>📍</span>
                <strong>{selectedState}</strong>
              </div>
            )}
            {!selectedState && stats && (
              <div className="info-item">
                <span>🗺️</span>
                <strong>{stats.states_covered} states</strong>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
