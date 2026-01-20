import { useState, useEffect } from 'react';
import { products } from '../services/api';
import ProductCard from '../components/ProductCard';
import ProductModal from '../components/ProductModal';
import './Products.css';

function Products({ user }) {
  const [productList, setProductList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const loadProducts = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await products.list({ q: searchQuery || undefined });
      setProductList(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    loadProducts();
  };

  const handleProductClick = (product) => {
    setSelectedProduct(product);
  };

  const handleCloseModal = () => {
    setSelectedProduct(null);
  };

  const handleBidPlaced = () => {
    loadProducts();
  };

  return (
    <div className="products-page">
      <div className="page-header">
        <h1>All Products</h1>
        <form className="search-form" onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Search products..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button type="submit" className="btn-primary">Search</button>
        </form>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading products...</div>
      ) : productList.length === 0 ? (
        <div className="empty-state">
          <h3>No products found</h3>
          <p>Try a different search term or check back later.</p>
        </div>
      ) : (
        <div className="products-grid">
          {productList.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onClick={handleProductClick}
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

export default Products;
