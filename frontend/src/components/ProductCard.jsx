import { useState } from 'react';
import { favorites } from '../services/api';
import './ProductCard.css';

function ProductCard({ product, onClick, showFavorite = false, showSeller = false, showHighestBid = false, onFavoriteToggle }) {
  const [isFavorited, setIsFavorited] = useState(product.is_favorited || false);
  const [loading, setLoading] = useState(false);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'ACTIVE': return 'status-active';
      case 'CLOSED': return 'status-closed';
      case 'SOLD': return 'status-sold';
      case 'EXPIRED': return 'status-expired';
      default: return '';
    }
  };

  const getStatusLabel = () => {
    // For sold products, show order/payment status if available
    if (product.status === 'SOLD' && product.order_status) {
      switch (product.order_status) {
        case 'AWAITING_PAYMENT':
          return 'AWAITING PAYMENT';
        case 'PAID':
          return 'PAYMENT COMPLETE';
        case 'CANCELLED':
          return 'CANCELLED';
        default:
          return 'SOLD';
      }
    }
    return product.status;
  };

  const handleFavoriteClick = async (e) => {
    e.stopPropagation();
    if (loading) return;
    
    setLoading(true);
    try {
      if (isFavorited) {
        await favorites.remove(product.id);
        setIsFavorited(false);
      } else {
        await favorites.add(product.id);
        setIsFavorited(true);
      }
      if (onFavoriteToggle) onFavoriteToggle(product.id, !isFavorited);
    } catch (err) {
      console.error('Failed to toggle favorite:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="product-card" onClick={() => onClick(product)}>
      <div className="product-image">
        {product.images && product.images.length > 0 ? (
          <img src={product.images[0].image_url} alt={product.title} />
        ) : (
          <div className="no-image">No Image</div>
        )}
        <span className={'product-status ' + getStatusClass(product.status)}>
          {getStatusLabel()}
        </span>
        {showFavorite && (
          <button 
            className={'favorite-btn ' + (isFavorited ? 'favorited' : '')}
            onClick={handleFavoriteClick}
            disabled={loading}
          >
            {isFavorited ? '★' : '☆'}
          </button>
        )}
      </div>
      <div className="product-info">
        <h3 className="product-title">{product.title}</h3>
        {showSeller && product.seller && (
          <p className="product-seller">by {product.seller.full_name}</p>
        )}
        <p className="product-description">
          {product.description?.substring(0, 80)}
          {product.description?.length > 80 ? '...' : ''}
        </p>
        <div className="product-price">
          <span className="label">Starting Price:</span>
          <span className="value">{formatPrice(product.starting_price)}</span>
        </div>
        {showHighestBid && (
          <div className="product-highest-bid">
            <span className="label">Highest Bid:</span>
            <span className="value">{product.highest_bid ? formatPrice(product.highest_bid) : '-'}</span>
          </div>
        )}
        <div className="product-meta">
          <span className="auction-end">
            Ends: {formatDate(product.auction_end_at)}
          </span>
          {product.bid_count !== undefined && (
            <span className="bid-count"> | {product.bid_count} bid{product.bid_count !== 1 ? 's' : ''}</span>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProductCard;
