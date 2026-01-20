import { useState, useEffect } from 'react';
import { products } from '../services/api';
import ProductCard from '../components/ProductCard';
import ProductModal from '../components/ProductModal';
import './Feed.css';

function Feed({ searchQuery }) {
  const [productList, setProductList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedProduct, setSelectedProduct] = useState(null);

  const loadProducts = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await products.getFeed(searchQuery || null);
      setProductList(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, [searchQuery]);

  const handleProductClick = (product) => {
    setSelectedProduct(product);
  };

  const handleCloseModal = () => {
    setSelectedProduct(null);
  };

  const handleBidPlaced = () => {
    loadProducts();
  };

  const handleFavoriteToggle = (productId, isFavorited) => {
    // Update the local state to reflect the favorite change
    setProductList(prev => prev.map(p => 
      p.id === productId ? { ...p, is_favorited: isFavorited } : p
    ));
  };

  return (
    <div className="feed-page">
      <div className="page-header">
        <h1>Feed</h1>
        <p className="page-subtitle">Browse products from other sellers</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading products...</div>
      ) : productList.length === 0 ? (
        <div className="empty-state">
          <h3>No products found</h3>
          <p>Check back later for new listings.</p>
        </div>
      ) : (
        <div className="products-grid">
          {productList.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onClick={handleProductClick}
              showFavorite={true}
              showSeller={true}
              showHighestBid={true}
              onFavoriteToggle={handleFavoriteToggle}
            />
          ))}
        </div>
      )}

      {selectedProduct && (
        <ProductModal
          product={selectedProduct}
          onClose={handleCloseModal}
          onBidPlaced={handleBidPlaced}
        />
      )}
    </div>
  );
}

export default Feed;
