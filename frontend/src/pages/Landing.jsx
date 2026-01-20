import './Landing.css';

function Landing({ onShowLogin, onShowSignup }) {
  return (
    <div className="landing-container">
      <div className="landing-content">
        <h1 className="landing-logo">BidBay</h1>
        <p className="landing-tagline">Your Premier Auction Marketplace</p>
        <p className="landing-description">
          Buy and sell unique items through exciting auctions. 
          Join thousands of users in the ultimate bidding experience.
        </p>
        <div className="landing-buttons">
          <button className="btn-primary btn-large" onClick={onShowLogin}>
            Login
          </button>
          <button className="btn-secondary btn-large" onClick={onShowSignup}>
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
}

export default Landing;
