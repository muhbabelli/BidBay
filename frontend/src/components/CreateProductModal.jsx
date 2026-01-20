import { useState, useEffect } from 'react';
import { products, categories } from '../services/api';
import './CreateProductModal.css';

function CreateProductModal({ onClose, onProductCreated }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [startingPrice, setStartingPrice] = useState('');
  const [minIncrement, setMinIncrement] = useState('5');
  const [categoryId, setCategoryId] = useState('');
  const [auctionEndDate, setAuctionEndDate] = useState('');
  const [auctionEndTime, setAuctionEndTime] = useState('');
  const [imagePreview, setImagePreview] = useState(null);
  const [categoryList, setCategoryList] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    categories.list()
      .then(setCategoryList)
      .catch(console.error);
  }, []);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!title || !description || !startingPrice || !categoryId || !auctionEndDate || !auctionEndTime) {
      setError('Please fill in all required fields.');
      return;
    }

    const endDateTime = new Date(auctionEndDate + 'T' + auctionEndTime);
    if (endDateTime <= new Date()) {
      setError('Auction end date must be in the future.');
      return;
    }

    setLoading(true);
    try {
      const productData = {
        title,
        description,
        starting_price: parseFloat(startingPrice),
        min_increment: parseFloat(minIncrement) || 5,
        category_id: parseInt(categoryId),
        auction_end_at: endDateTime.toISOString(),
      };

      const newProduct = await products.create(productData);

      if (imagePreview) {
        try {
          await products.addImage(newProduct.id, imagePreview);
        } catch (imgErr) {
          console.error('Failed to add image:', imgErr);
        }
      }

      onProductCreated();
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content create-product-modal" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>&times;</button>
        
        <h2>Create New Product</h2>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Product Title *</label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter product title"
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description *</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe your product..."
              rows={3}
              disabled={loading}
            />
          </div>

          <div className="form-row two-cols">
            <div className="form-group">
              <label htmlFor="startingPrice">Starting Price ($) *</label>
              <input
                id="startingPrice"
                type="number"
                step="0.01"
                min="0"
                value={startingPrice}
                onChange={(e) => setStartingPrice(e.target.value)}
                placeholder="0.00"
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label htmlFor="minIncrement">Min Bid Increment ($)</label>
              <input
                id="minIncrement"
                type="number"
                step="0.01"
                min="0"
                value={minIncrement}
                onChange={(e) => setMinIncrement(e.target.value)}
                placeholder="5.00"
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="category">Category *</label>
            <select
              id="category"
              value={categoryId}
              onChange={(e) => setCategoryId(e.target.value)}
              disabled={loading}
            >
              <option value="">Select a category</option>
              {categoryList.map((cat) => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>

          <div className="form-row two-cols">
            <div className="form-group">
              <label htmlFor="auctionEndDate">Auction End Date *</label>
              <input
                id="auctionEndDate"
                type="date"
                value={auctionEndDate}
                onChange={(e) => setAuctionEndDate(e.target.value)}
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label htmlFor="auctionEndTime">Auction End Time *</label>
              <input
                id="auctionEndTime"
                type="time"
                value={auctionEndTime}
                onChange={(e) => setAuctionEndTime(e.target.value)}
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Product Image</label>
            <div className="image-upload-area">
              {imagePreview ? (
                <div className="image-preview">
                  <img src={imagePreview} alt="Preview" />
                  <button 
                    type="button" 
                    className="remove-image" 
                    onClick={() => setImagePreview(null)}
                  >
                    &times;
                  </button>
                </div>
              ) : (
                <label className="upload-label">
                  <input
                    type="file"
                    accept="image/png,image/jpeg,image/jpg,image/gif,image/webp"
                    onChange={handleImageChange}
                    disabled={loading}
                  />
                  <span>Click to upload image</span>
                  <span className="upload-hint">PNG, JPG, GIF up to 5MB</span>
                </label>
              )}
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="form-actions">
            <button type="button" className="btn-cancel" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Creating...' : 'Create Product'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateProductModal;
