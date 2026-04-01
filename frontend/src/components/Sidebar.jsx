import { useState, useMemo } from 'react';

function Sidebar({ statesData, stats, selectedState, onStateSelect, onShowAll, onRefresh, isOpen }) {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredStates = useMemo(() => {
    if (!statesData?.states) return [];
    if (!searchQuery.trim()) return statesData.states;
    return statesData.states.filter(s =>
      s.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [statesData, searchQuery]);

  const totalPlaces = stats?.total_places || statesData?.total || 0;
  const statesCovered = stats?.states_covered || statesData?.states?.length || 0;
  const districtsCompleted = stats?.districts_completed || 0;
  const apiRequests = stats?.api_requests_used || 0;

  return (
    <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
      {/* Header */}
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <div className="logo-icon">🏭</div>
          <div>
            <h1>Industrial Areas</h1>
            <p>India — Ola Maps Explorer</p>
          </div>
        </div>
      </div>

      <div className="sidebar-content">
        {/* Stats Grid */}
        <div className="stats-grid fade-in">
          <div className="stat-card">
            <div className="stat-label">Total Places</div>
            <div className="stat-value accent">{totalPlaces.toLocaleString()}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">States</div>
            <div className="stat-value green">{statesCovered}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Districts</div>
            <div className="stat-value">{districtsCompleted}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">API Calls</div>
            <div className="stat-value">{apiRequests.toLocaleString()}</div>
          </div>
        </div>

        {/* State Filter */}
        <div className="state-filter">
          <div className="section-header">
            <h3>Filter by State</h3>
            <span className="badge">{filteredStates.length}</span>
          </div>

          <div className="state-search-wrap">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              className="state-search"
              placeholder="Search states..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="state-list">
            {/* Show All option */}
            <div
              className={`state-item ${!selectedState ? 'active' : ''}`}
              onClick={onShowAll}
            >
              <span className="state-name state-item-all">🗺️ All India</span>
              <span className="state-count">{totalPlaces.toLocaleString()}</span>
            </div>

            {filteredStates.map((state, idx) => (
              <div
                key={state.name}
                className={`state-item slide-in ${selectedState === state.name ? 'active' : ''}`}
                style={{ animationDelay: `${Math.min(idx * 20, 400)}ms` }}
                onClick={() => onStateSelect(state.name)}
              >
                <span className="state-name">{state.name}</span>
                <span className="state-count">{state.count}</span>
              </div>
            ))}

            {filteredStates.length === 0 && statesData?.states?.length > 0 && (
              <div className="no-data" style={{ padding: '20px' }}>
                <p>No states match "{searchQuery}"</p>
              </div>
            )}

            {(!statesData?.states || statesData.states.length === 0) && (
              <div className="no-data">
                <div className="no-data-icon">📡</div>
                <h3>No Data Yet</h3>
                <p>
                  Run the fetcher script to start collecting industrial area data:
                </p>
                <p style={{ marginTop: '8px' }}>
                  <code>cd backend</code><br />
                  <code>python fetcher.py</code>
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
