import { useState, useEffect } from 'react';
import { bids } from '../services/api';
import './MyProductModal.css';

function MyProductModal({ product, onClose }) {
  const [bidsList, setBidsList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [actionLoading, setActionLoading] = useState(null);

  const loadBids = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await bids.getProductBids(product.id);
      setBidsList(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBids();
  }, [product.id]);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'ACCEPTED': return 'status-accepted';
      case 'REJECTED': return 'status-rejected';
      case 'PENDING': return 'status-pending';
      case 'OUTBID': return 'status-outbid';
      default: return '';
    }
  };

  const handleAccept = async (bidId) => {
    setActionLoading(bidId);
    setError('');
    try {
      await bids.acceptBid(bidId);
      await loadBids();
    } catch (err) {
      setError(err.message);
    } finally {
      setActionLoading(null);
    }
  };

  const handleReject = async (bidId) => {
    setActionLoading(bidId);
    setError('');
    try {
      await bids.rejectBid(bidId);
      await loadBids();
    } catch (err) {
      setError(err.message);
    } finally {
      setActionLoading(null);
    }
  };

  const isProductSold = product.status === 'SOLD';

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content my-product-modal" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>&times;</button>

        <div className="modal-header">
          <h2>{product.title}</h2>
          <span className={'product-status ' + (isProductSold ? 'sold' : 'active')}>
            {product.status}
          </span>
        </div>

        <div className="product-details">
          <div className="detail-row">
            <span className="label">Starting Price:</span>
            <span className="value">{formatPrice(product.starting_price)}</span>
          </div>
          <div className="detail-row">
            <span className="label">Highest Bid:</span>
            <span className="value highlight">{product.highest_bid ? formatPrice(product.highest_bid) : '-'}</span>
          </div>
          <div className="detail-row">
            <span className="label">Total Bids:</span>
            <span className="value">{product.bid_count || 0}</span>
          </div>
        </div>

        <div className="bids-section">
          <h3>Bids</h3>

          {error && <div className="error-message">{error}</div>}

          {loading ? (
            <div className="loading">Loading bids...</div>
          ) : bidsList.length === 0 ? (
            <div className="empty-bids">No bids yet on this product.</div>
          ) : (
            <div className="bids-table">
              {bidsList.map((bid) => (
                <div key={bid.id} className={'bid-row ' + getStatusClass(bid.status)}>
                  <div className="bidder-info">
                    {bid.bidder && (
                      <>
                        <span className="bidder-name">{bid.bidder.full_name}</span>
                        {bid.bidder.phone_number && (
                          <span className="bidder-phone">{bid.bidder.phone_number}</span>
                        )}
                      </>
                    )}
                  </div>
                  <div className="bid-amount-col">
                    <span className="amount">{formatPrice(bid.amount)}</span>
                    <span className="bid-time">{formatDate(bid.created_at)}</span>
                  </div>
                  <div className="bid-status-col">
                    <span className={'bid-status ' + getStatusClass(bid.status)}>{bid.status}</span>
                  </div>
                  <div className="bid-actions">
                    {bid.status === 'PENDING' && !isProductSold && (
                      <>
                        <button
                          className="btn-accept"
                          onClick={() => handleAccept(bid.id)}
                          disabled={actionLoading === bid.id}
                        >
                          {actionLoading === bid.id ? '...' : 'Accept'}
                        </button>
                        <button
                          className="btn-reject"
                          onClick={() => handleReject(bid.id)}
                          disabled={actionLoading === bid.id}
                        >
                          {actionLoading === bid.id ? '...' : 'Reject'}
                        </button>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default MyProductModal;
