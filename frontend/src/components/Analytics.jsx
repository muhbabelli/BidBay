import { useState, useEffect } from 'react';
import { analytics } from '../services/api';
import './Analytics.css';

function Analytics() {
  const [sellerStats, setSellerStats] = useState([]);
  const [topBidders, setTopBidders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('seller'); // 'seller' or 'bidders'

  const loadAnalytics = async () => {
    setLoading(true);
    setError('');
    try {
      const [statsData, biddersData] = await Promise.all([
        analytics.getSellerBidStats(),
        analytics.getTopBidders(2)
      ]);
      setSellerStats(statsData);
      setTopBidders(biddersData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  const formatPrice = (price) => {
    if (price === null || price === undefined) return '-';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  if (loading) {
    return <div className="loading">Loading analytics...</div>;
  }

  return (
    <div className="analytics-page">
      <div className="page-header">
        <h1>Analytics Dashboard</h1>
        <p className="page-subtitle">View insights from advanced SQL queries</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="analytics-tabs">
        <button
          className={'tab-button ' + (activeTab === 'seller' ? 'active' : '')}
          onClick={() => setActiveTab('seller')}
        >
          My Seller Statistics
        </button>
        <button
          className={'tab-button ' + (activeTab === 'bidders' ? 'active' : '')}
          onClick={() => setActiveTab('bidders')}
        >
          Top Bidders Leaderboard
        </button>
      </div>

      {activeTab === 'seller' && (
        <div className="analytics-section">
          <div className="section-header">
            <h2>Seller Bid Statistics</h2>
            <p className="section-description">
              Advanced SQL query using COUNT, MAX, AVG aggregates and GROUP BY/HAVING clauses
            </p>
          </div>

          {sellerStats.length === 0 ? (
            <div className="empty-analytics">
              <p>No products with bids found.</p>
              <p className="empty-subtitle">Create products and receive bids to see statistics here.</p>
            </div>
          ) : (
            <div className="stats-grid">
              {sellerStats.map((stat) => (
                <div key={stat.product_id} className="stat-card">
                  <div className="stat-header">
                    <h3 className="stat-title">{stat.title}</h3>
                    <span className="stat-badge">ID: {stat.product_id}</span>
                  </div>
                  <div className="stat-metrics">
                    <div className="metric">
                      <span className="metric-label">Total Bids</span>
                      <span className="metric-value bid-count">{stat.bid_count}</span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">Highest Bid</span>
                      <span className="metric-value max-bid">{formatPrice(stat.max_bid)}</span>
                    </div>
                    <div className="metric">
                      <span className="metric-label">Average Bid</span>
                      <span className="metric-value avg-bid">{formatPrice(stat.avg_bid)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'bidders' && (
        <div className="analytics-section">
          <div className="section-header">
            <h2>Top Bidders Leaderboard</h2>
            <p className="section-description">
              Advanced SQL query using JOIN, GROUP BY, HAVING, and ORDER BY to rank most active bidders
            </p>
          </div>

          {topBidders.length === 0 ? (
            <div className="empty-analytics">
              <p>No active bidders found.</p>
              <p className="empty-subtitle">Bidders with at least 2 bids will appear here.</p>
            </div>
          ) : (
            <div className="leaderboard">
              <div className="leaderboard-header">
                <span className="rank-col">Rank</span>
                <span className="user-col">User</span>
                <span className="bids-col">Total Bids</span>
              </div>
              {topBidders.map((bidder, index) => (
                <div key={bidder.user_id} className={'leaderboard-row ' + (index < 3 ? 'top-' + (index + 1) : '')}>
                  <span className="rank-col">
                    {index === 0 && '🥇'}
                    {index === 1 && '🥈'}
                    {index === 2 && '🥉'}
                    {index > 2 && `#${index + 1}`}
                  </span>
                  <span className="user-col">{bidder.email}</span>
                  <span className="bids-col">{bidder.bid_count}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Analytics;
