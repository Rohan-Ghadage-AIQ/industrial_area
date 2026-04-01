import { useState, useEffect, useRef, useMemo } from 'react';
import L from 'leaflet';
import 'leaflet.markercluster';

// Fix default marker icon issue with bundlers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

const industrialIcon = L.divIcon({
  html: `<div style="
    width: 24px; height: 24px;
    display: flex; align-items: center; justify-content: center;
  "><div style="
    width: 12px; height: 12px;
    background: #6366f1;
    border: 2px solid #fff;
    border-radius: 50%;
    box-shadow: 0 0 8px rgba(99,102,241,0.6);
  "></div></div>`,
  className: '',
  iconSize: [24, 24],
  iconAnchor: [12, 12],
  popupAnchor: [0, -12]
});

function MapView({ geojsonData, loading, error, selectedState, onStateSelect }) {
  const [statesGeoJson, setStatesGeoJson] = useState(null);
  const mapRef = useRef(null);
  const mapInstance = useRef(null);
  const clusterGroup = useRef(null);
  const statesLayer = useRef(null);

  // Fetch state boundaries on mount
  useEffect(() => {
    fetch('/india_states.geojson')
      .then(res => res.json())
      .then(data => setStatesGeoJson(data))
      .catch(err => console.error("Error loading state boundaries", err));
  }, []);

  // Initialize map
  useEffect(() => {
    if (mapInstance.current) return;

    const map = L.map(mapRef.current, {
      center: [22.5, 82.0], // Center of India
      zoom: 5,
      zoomControl: false,
      attributionControl: true,
    });

    // Add zoom control to bottom-right
    L.control.zoom({ position: 'topright' }).addTo(map);

    // Dark map tiles (CartoDB Dark Matter)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19,
    }).addTo(map);

    // Initialize marker cluster group
    clusterGroup.current = L.markerClusterGroup({
      maxClusterRadius: 50,
      spiderfyOnMaxZoom: true,
      showCoverageOnHover: false,
      zoomToBoundsOnClick: true,
      chunkedLoading: true,
      iconCreateFunction: (cluster) => {
        const count = cluster.getChildCount();
        let size = 'small';
        let radius = 30;
        if (count > 100) { size = 'large'; radius = 44; }
        else if (count > 10) { size = 'medium'; radius = 36; }

        return L.divIcon({
          html: `<div><span>${count}</span></div>`,
          className: `marker-cluster marker-cluster-${size}`,
          iconSize: L.point(radius, radius),
        });
      }
    });

    map.addLayer(clusterGroup.current);
    mapInstance.current = map;

    return () => {
      if (statesLayer.current) statesLayer.current.remove();
      map.remove();
      mapInstance.current = null;
    };
  }, []);

  // Update state boundaries
  useEffect(() => {
    if (!mapInstance.current || !statesGeoJson) return;

    if (statesLayer.current) {
      mapInstance.current.removeLayer(statesLayer.current);
    }

    statesLayer.current = L.geoJSON(statesGeoJson, {
      style: (feature) => {
        const isSelected = selectedState && feature.properties.st_nm === selectedState;
        return {
          color: isSelected ? '#eab308' : '#f97316', // yellow if selected, else orange
          weight: isSelected ? 2 : 1,
          opacity: isSelected ? 0.9 : 0.6,
          fillOpacity: isSelected ? 0.1 : 0.02,
          fillColor: isSelected ? '#eab308' : 'transparent'
        };
      },
      onEachFeature: (feature, layer) => {
        layer.on({
          click: () => {
            if (onStateSelect) {
              onStateSelect(feature.properties.st_nm);
            }
          }
        });
      }
    });

    statesLayer.current.addTo(mapInstance.current);
    
    // Ensure state borders stay behind markers
    statesLayer.current.bringToBack();
  }, [statesGeoJson, selectedState, onStateSelect]);

  // Update markers when data changes
  useEffect(() => {
    if (!mapInstance.current || !clusterGroup.current) return;

    // Clear existing markers
    clusterGroup.current.clearLayers();

    if (!geojsonData || !geojsonData.features || geojsonData.features.length === 0) return;

    const markers = [];
    const bounds = L.latLngBounds();

    geojsonData.features.forEach((feature) => {
      const coords = feature.geometry?.coordinates;
      if (!coords || coords.length < 2) return;

      const [lng, lat] = coords;
      if (!lat || !lng || lat === 0 || lng === 0) return;

      const props = feature.properties || {};
      const latlng = L.latLng(lat, lng);
      bounds.extend(latlng);

      const marker = L.marker(latlng, { icon: industrialIcon });

      // Build popup content
      const types = (props.types || []).slice(0, 4);
      const tagsHtml = types.map(t =>
        `<span class="popup-tag">${t.replace(/_/g, ' ')}</span>`
      ).join('');

      const popupContent = `
        <div class="place-popup">
          <h4>${props.name || 'Unknown'}</h4>
          <div class="popup-row">
            <span class="popup-label">Address</span>
            <span class="popup-value">${props.address || 'N/A'}</span>
          </div>
          <div class="popup-row">
            <span class="popup-label">District</span>
            <span class="popup-value">${props.district || 'N/A'}</span>
          </div>
          <div class="popup-row">
            <span class="popup-label">State</span>
            <span class="popup-value">${props.state || 'N/A'}</span>
          </div>
          <div class="popup-row">
            <span class="popup-label">Coords</span>
            <span class="popup-value">${lat.toFixed(4)}, ${lng.toFixed(4)}</span>
          </div>
          ${tagsHtml ? `<div class="popup-tags">${tagsHtml}</div>` : ''}
        </div>
      `;

      marker.bindTooltip(popupContent, {
        direction: 'top',
        className: 'dark-popup',
        opacity: 1,
        interactive: true
      });

      marker.on('click', () => {
        if (onStateSelect && props.state) {
          onStateSelect(props.state);
        }
      });

      markers.push(marker);
    });

    if (markers.length > 0) {
      clusterGroup.current.addLayers(markers);

      // Fit bounds with padding
      if (bounds.isValid()) {
        mapInstance.current.fitBounds(bounds, {
          padding: [50, 50],
          maxZoom: 12,
          animate: true,
          duration: 0.8,
        });
      }
    }
  }, [geojsonData]);

  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <div ref={mapRef} style={{ width: '100%', height: '100%' }} />

      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <span className="loading-text">Loading industrial areas...</span>
        </div>
      )}

      {error && !loading && (
        <div className="loading-overlay">
          <div className="no-data">
            <div className="no-data-icon">🏭</div>
            <h3>No Data Available</h3>
            <p>
              Run the fetcher first to collect data:<br />
              <code>python fetcher.py</code>
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default MapView;
