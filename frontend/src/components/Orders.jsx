import { useState, useEffect } from 'react';
import { orders, payments } from '../services/api';
import PaymentModal from './PaymentModal';
import './Orders.css';

function Orders() {
  const [ordersList, setOrdersList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [showPaymentModal, setShowPaymentModal] = useState(false);

  const loadOrders = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await orders.getBuyerOrders();
      setOrdersList(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOrders();
  }, []);

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
      case 'AWAITING_PAYMENT': return 'status-pending';
      case 'PAID': return 'status-paid';
      case 'CANCELLED': return 'status-cancelled';
      default: return '';
    }
  };

  const handlePayNow = (order) => {
    setSelectedOrder(order);
    setShowPaymentModal(true);
  };

  const handlePaymentSuccess = () => {
    setShowPaymentModal(false);
    setSelectedOrder(null);
    loadOrders();
  };

  if (loading) {
    return <div className="loading">Loading orders...</div>;
  }

  return (
    <div className="orders-page">
      <div className="page-header">
        <h1>My Orders</h1>
        <p className="page-subtitle">View your accepted bids and complete payments</p>
      </div>

      {error && <div className="error-message">{error}</div>}

      {ordersList.length === 0 ? (
        <div className="empty-orders">
          <p>No orders yet.</p>
          <p className="empty-subtitle">When a seller accepts your bid, an order will be created here.</p>
        </div>
      ) : (
        <div className="orders-list">
          {ordersList.map((order) => (
            <div key={order.id} className={`order-card ${getStatusClass(order.status)}`}>
              <div className="order-header">
                <div className="order-info">
                  <h3 className="order-title">{order.product_title}</h3>
                  <span className={`order-status ${getStatusClass(order.status)}`}>
                    {order.status.replace('_', ' ')}
                  </span>
                </div>
                <div className="order-amount">
                  {formatPrice(order.total_amount)}
                </div>
              </div>

              <div className="order-details">
                <div className="detail-item">
                  <span className="detail-label">Order ID:</span>
                  <span className="detail-value">#{order.id}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">Order Date:</span>
                  <span className="detail-value">{formatDate(order.created_at)}</span>
                </div>
                {order.seller && (
                  <>
                    <div className="detail-item">
                      <span className="detail-label">Seller:</span>
                      <span className="detail-value">{order.seller.full_name}</span>
                    </div>
                    {order.status === 'PAID' && order.seller.phone_number && (
                      <div className="detail-item">
                        <span className="detail-label">Seller Phone:</span>
                        <span className="detail-value">{order.seller.phone_number}</span>
                      </div>
                    )}
                  </>
                )}
              </div>

              {order.status === 'AWAITING_PAYMENT' && (
                <div className="order-actions">
                  <button
                    className="btn-pay-now"
                    onClick={() => handlePayNow(order)}
                  >
                    Pay Now
                  </button>
                </div>
              )}

              {order.status === 'PAID' && (
                <div className="order-paid-message">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M10 0C4.477 0 0 4.477 0 10s4.477 10 10 10 10-4.477 10-10S15.523 0 10 0zm4.707 7.707l-5 5a1 1 0 01-1.414 0l-2.5-2.5a1 1 0 111.414-1.414L9 10.586l4.293-4.293a1 1 0 111.414 1.414z" fill="#22c55e"/>
                  </svg>
                  <span>Payment completed successfully</span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {showPaymentModal && selectedOrder && (
        <PaymentModal
          order={selectedOrder}
          onClose={() => {
            setShowPaymentModal(false);
            setSelectedOrder(null);
          }}
          onSuccess={handlePaymentSuccess}
        />
      )}
    </div>
  );
}

export default Orders;
