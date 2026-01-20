import './Navbar.css';

function Navbar({ user, onLogout, currentTab, onTabChange, searchQuery, onSearchChange, onSearch }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <h1>BidBay</h1>
        </div>

        <div className="navbar-tabs">
          <button
            className={'tab-btn' + (currentTab === 'feed' ? ' active' : '')}
            onClick={() => onTabChange('feed')}
          >
            Feed
          </button>
          <button
            className={'tab-btn' + (currentTab === 'favorites' ? ' active' : '')}
            onClick={() => onTabChange('favorites')}
          >
            Favorites
          </button>
          <button
            className={'tab-btn' + (currentTab === 'home' ? ' active' : '')}
            onClick={() => onTabChange('home')}
          >
            Home
          </button>
        </div>

        <form className="navbar-search" onSubmit={onSearch}>
          <input
            type="text"
            placeholder="Search products..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
          />
          <button type="submit" className="btn-search">Search</button>
        </form>

        <div className="navbar-user">
          <span className="user-name">{user.full_name}</span>
          <button onClick={onLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
