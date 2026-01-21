import { useState } from 'react';
import { payments } from '../services/api';
import './PaymentModal.css';

function PaymentModal({ order, onClose, onSuccess }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [paymentComplete, setPaymentComplete] = useState(false);

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(price);
  };

  const handlePayment = async () => {
    setLoading(true);
    setError('');
    try {
      await payments.create(order.id);
      setPaymentComplete(true);
      setTimeout(() => {
        onSuccess();
      }, 2000);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content payment-modal" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>&times;</button>

        {!paymentComplete ? (
          <>
            <div className="modal-header">
              <h2>Complete Payment</h2>
            </div>

            <div className="payment-body">
              <div className="payment-summary">
                <h3>Order Summary</h3>
                <div className="summary-row">
                  <span className="summary-label">Product:</span>
                  <span className="summary-value">{order.product_title}</span>
                </div>
                <div className="summary-row">
                  <span className="summary-label">Order ID:</span>
                  <span className="summary-value">#{order.id}</span>
                </div>
                {order.seller && (
                  <div className="summary-row">
                    <span className="summary-label">Seller:</span>
                    <span className="summary-value">{order.seller.full_name}</span>
                  </div>
                )}
                <div className="summary-divider"></div>
                <div className="summary-row total">
                  <span className="summary-label">Total Amount:</span>
                  <span className="summary-value">{formatPrice(order.total_amount)}</span>
                </div>
              </div>

              <div className="payment-info">
                <div className="info-box">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" fill="#3b82f6"/>
                  </svg>
                  <div className="info-text">
                    <strong>Mock Payment System</strong>
                    <p>This is a demonstration payment system. In a real application, you would enter your payment details here. The payment will be automatically marked as successful.</p>
                  </div>
                </div>
              </div>

              {error && <div className="error-message">{error}</div>}

              <div className="payment-actions">
                <button
                  className="btn-cancel"
                  onClick={onClose}
                  disabled={loading}
                >
                  Cancel
                </button>
                <button
                  className="btn-pay"
                  onClick={handlePayment}
                  disabled={loading}
                >
                  {loading ? 'Processing...' : `Pay ${formatPrice(order.total_amount)}`}
                </button>
              </div>
            </div>
          </>
        ) : (
          <>
            <div className="modal-header">
              <h2>Payment Successful!</h2>
            </div>

            <div className="payment-success">
              <div className="success-icon">
                <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                  <circle cx="32" cy="32" r="32" fill="#dcfce7"/>
                  <path d="M20 32l8 8 16-16" stroke="#22c55e" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
              <h3>Payment Completed</h3>
              <p>Your payment of {formatPrice(order.total_amount)} has been processed successfully.</p>
              <p className="success-subtitle">You can now contact the seller to arrange pickup or delivery.</p>
              {order.seller && order.seller.phone_number && (
                <div className="seller-contact">
                  <strong>Seller Contact:</strong>
                  <p>{order.seller.full_name}</p>
                  <p>{order.seller.phone_number}</p>
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default PaymentModal;
