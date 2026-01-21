import { useState, useEffect } from 'react';
import { bids } from '../services/api';
import './ProductModal.css';

function ProductModal({ product, onClose, onBidPlaced }) {
  // Calculate minimum required bid
  const minBidAmount = product.highest_bid
    ? parseFloat(product.highest_bid) + parseFloat(product.min_increment)
    : parseFloat(product.starting_price);

  const [bidAmount, setBidAmount] = useState(minBidAmount.toString());
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  // Update bidAmount when product changes
  useEffect(() => {
    const newMinBid = product.highest_bid
      ? parseFloat(product.highest_bid) + parseFloat(product.min_increment)
      : parseFloat(product.starting_price);
    setBidAmount(newMinBid.toString());
  }, [product.highest_bid, product.min_increment, product.starting_price]);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handlePlaceBid = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    const amount = parseFloat(bidAmount);
    if (isNaN(amount) || amount <= 0) {
      setError('Please enter a valid bid amount');
      return;
    }

    // Validate minimum bid amount
    if (amount < minBidAmount) {
      setError(`Bid must be at least ${formatPrice(minBidAmount)}`);
      return;
    }

    setLoading(true);
    try {
      await bids.place(product.id, amount);
      setSuccess('Bid placed successfully!');
      // Update to new minimum bid after successful placement
      const newMinBid = amount + parseFloat(product.min_increment);
      setBidAmount(newMinBid.toString());
      if (onBidPlaced) onBidPlaced();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const isActive = product.status === 'ACTIVE' &&
    new Date(product.auction_end_at) > new Date();

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>&times;</button>

        <div className="modal-body">
          <div className="modal-image">
            {product.images && product.images.length > 0 ? (
              <img src={product.images[0].image_url} alt={product.title} />
            ) : (
              <div className="no-image">No Image Available</div>
            )}
          </div>

          <div className="modal-details">
            <h2>{product.title}</h2>
            <p className="description">{product.description}</p>

            <div className="detail-row">
              <span className="label">Starting Price:</span>
              <span className="value">{formatPrice(product.starting_price)}</span>
            </div>

            <div className="detail-row">
              <span className="label">Minimum Increment:</span>
              <span className="value">{formatPrice(product.min_increment)}</span>
            </div>

            <div className="detail-row">
              <span className="label">Auction Ends:</span>
              <span className="value">{formatDate(product.auction_end_at)}</span>
            </div>

            <div className="detail-row">
              <span className="label">Status:</span>
              <span className={`status status-${product.status.toLowerCase()}`}>
                {product.status}
              </span>
            </div>

            {isActive && (
              <form className="bid-form" onSubmit={handlePlaceBid}>
                <h3>Place a Bid</h3>
                {error && <div className="error-message">{error}</div>}
                {success && <div className="success-message">{success}</div>}
                <div className="bid-input-group">
                  <span className="currency">$</span>
                  <input
                    type="number"
                    step={product.min_increment}
                    min={minBidAmount}
                    value={bidAmount}
                    onChange={(e) => setBidAmount(e.target.value)}
                    placeholder={`Minimum bid: ${formatPrice(minBidAmount)}`}
                    disabled={loading}
                  />
                </div>
                <button type="submit" className="btn-primary" disabled={loading}>
                  {loading ? 'Placing Bid...' : 'Place Bid'}
                </button>
              </form>
            )}

            {!isActive && (
              <div className="auction-ended">
                This auction has ended or is no longer active.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductModal;
