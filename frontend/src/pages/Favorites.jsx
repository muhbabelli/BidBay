import { useState, useEffect } from 'react';
import { products } from '../services/api';
import ProductCard from '../components/ProductCard';
import ProductModal from '../components/ProductModal';
import './Favorites.css';

function Favorites() {
  const [productList, setProductList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedProduct, setSelectedProduct] = useState(null);

  const loadFavorites = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await products.getFavorites();
      setProductList(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFavorites();
  }, []);

  const handleProductClick = (product) => {
    setSelectedProduct(product);
  };

  const handleCloseModal = () => {
    setSelectedProduct(null);
  };

  const handleBidPlaced = () => {
    loadFavorites();
  };

  const handleFavoriteToggle = (productId, isFavorited) => {
    if (!isFavorited) {
      // Remove from list when unfavorited
      setProductList(prev => prev.filter(p => p.id !== productId));
    }
  };

  return (
    <div className="favorites-page">
      <div className="page-header">
        <h1>Favorites</h1>
        <p className="page-subtitle">Products you've added to favorites</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading favorites...</div>
      ) : productList.length === 0 ? (
        <div className="empty-state">
          <h3>No favorites yet</h3>
          <p>Browse the feed and click the star to add products to your favorites.</p>
        </div>
      ) : (
        <div className="products-grid">
          {productList.map((product) => (
            <ProductCard
              key={product.id}
              product={{ ...product, is_favorited: true }}
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

export default Favorites;
