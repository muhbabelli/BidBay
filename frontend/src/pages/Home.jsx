import { useState, useEffect } from 'react';
import { products, bids } from '../services/api';
import ProductCard from '../components/ProductCard';
import MyProductModal from '../components/MyProductModal';
import './Home.css';

function Home({ user }) {
  const [myProducts, setMyProducts] = useState([]);
  const [myBids, setMyBids] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedProduct, setSelectedProduct] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError('');
    try {
      const [productsData, bidsData] = await Promise.all([
        products.getMyProducts(),
        bids.getMyBids()
      ]);
      setMyProducts(productsData);
      setMyBids(bidsData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleProductClick = (product) => {
    setSelectedProduct(product);
  };

  const handleCloseModal = () => {
    setSelectedProduct(null);
    loadData();
  };

  const handleDeleteProduct = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) {
      return;
    }
    try {
      await products.delete(productId);
      loadData();
    } catch (err) {
      alert('Failed to delete: ' + err.message);
    }
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
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

  return (
    <div className="home-page">
      <div className="section">
        <div className="section-header">
          <h2>My Products</h2>
          <p className="section-subtitle">Manage your listings and view bids</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        {loading ? (
          <div className="loading">Loading...</div>
        ) : myProducts.length === 0 ? (
          <div className="empty-state">
            <h3>No products listed</h3>
            <p>Click the + button at the bottom right to create your first listing.</p>
          </div>
        ) : (
          <div className="products-grid">
            {myProducts.map((product) => (
              <div key={product.id} className="my-product-card-wrapper">
                <ProductCard
                  product={product}
                  onClick={handleProductClick}
                  showHighestBid={true}
                />
                <button 
                  className="delete-product-btn"
                  onClick={(e) => { e.stopPropagation(); handleDeleteProduct(product.id); }}
                  title="Delete product"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="section">
        <div className="section-header">
          <h2>My Bids</h2>
          <p className="section-subtitle">Track your bids on other products</p>
        </div>

        {loading ? (
          <div className="loading">Loading...</div>
        ) : myBids.length === 0 ? (
          <div className="empty-state">
            <h3>No bids placed</h3>
            <p>Browse the feed to find products and place bids.</p>
          </div>
        ) : (
          <div className="bids-list">
            {myBids.map((bid) => (
              <div key={bid.id} className={'bid-card ' + getStatusClass(bid.status)}>
                <div className="bid-info">
                  <h4 className="bid-product-title">{bid.product_title || 'Unknown Product'}</h4>
                  <div className="bid-details">
                    <span className="bid-amount">Your bid: {formatPrice(bid.amount)}</span>
                    <span className={'bid-status ' + getStatusClass(bid.status)}>{bid.status}</span>
                  </div>
                  {bid.seller && (
                    <div className="seller-info">
                      <span>Seller: {bid.seller.full_name}</span>
                      {bid.status === 'ACCEPTED' && bid.seller.phone_number && (
                        <span className="seller-phone">Phone: {bid.seller.phone_number}</span>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedProduct && (
        <MyProductModal
          product={selectedProduct}
          onClose={handleCloseModal}
        />
      )}
    </div>
  );
}

export default Home;
