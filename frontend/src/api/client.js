const API_BASE = 'http://localhost:8000/api';

export async function fetchStates() {
  const res = await fetch(`${API_BASE}/data/states`);
  if (!res.ok) throw new Error('Failed to fetch states');
  return res.json();
}

export async function fetchGeoJSON(state = null) {
  const url = state
    ? `${API_BASE}/data/geojson?state=${encodeURIComponent(state)}`
    : `${API_BASE}/data/geojson`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch GeoJSON');
  return res.json();
}

export async function fetchStats() {
  const res = await fetch(`${API_BASE}/data/stats`);
  if (!res.ok) throw new Error('Failed to fetch stats');
  return res.json();
}

export async function fetchStatus() {
  const res = await fetch(`${API_BASE}/status`);
  if (!res.ok) throw new Error('Failed to fetch status');
  return res.json();
}

export async function triggerMerge() {
  const res = await fetch(`${API_BASE}/data/merge`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to merge');
  return res.json();
}
