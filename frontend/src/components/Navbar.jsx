import './Navbar.css';

const DEFAULT_AVATAR = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iI2NjYyI+PHBhdGggZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6bTAgM2MxLjY2IDAgMyAxLjM0IDMgM3MtMS4zNCAzLTMgMy0zLTEuMzQtMy0zIDEuMzQtMyAzLTN6bTAgMTQuMmMtMi41IDAtNC43MS0xLjI4LTYtMy4yMi4wMy0xLjk5IDQtMy4wOCA2LTMuMDggMS45OSAwIDUuOTcgMS4wOSA2IDMuMDgtMS4yOSAxLjk0LTMuNSAzLjIyLTYgMy4yMnoiLz48L3N2Zz4=';

function Navbar({ user, onLogout, currentTab, onTabChange, searchQuery, onSearchChange, onSearch, onOpenProfile }) {
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
          <button
            className={'tab-btn' + (currentTab === 'orders' ? ' active' : '')}
            onClick={() => onTabChange('orders')}
          >
            Orders
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
          <button className="profile-btn" onClick={onOpenProfile}>
            <img 
              src={user.profile_image || DEFAULT_AVATAR} 
              alt="Profile" 
              className="nav-profile-image"
            />
            <span className="user-name">{user.full_name}</span>
          </button>
          <button onClick={onLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
