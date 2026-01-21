import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Feed from './pages/Feed';
import Favorites from './pages/Favorites';
import Home from './pages/Home';
import Orders from './components/Orders';
import Analytics from './components/Analytics';
import ProfileModal from './components/ProfileModal';
import CreateProductModal from './components/CreateProductModal';
import { auth } from './services/api';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authView, setAuthView] = useState('landing'); // 'landing', 'login', 'signup'
  const [currentTab, setCurrentTab] = useState('feed');
  const [searchQuery, setSearchQuery] = useState('');
  const [appliedSearch, setAppliedSearch] = useState('');
  const [showProfile, setShowProfile] = useState(false);
  const [showCreateProduct, setShowCreateProduct] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    if (auth.isLoggedIn()) {
      auth.getMe()
        .then(setUser)
        .catch(() => {
          auth.logout();
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setAuthView('landing');
  };

  const handleLogout = () => {
    auth.logout();
    setUser(null);
    setAuthView('landing');
  };

  const handleSignupSuccess = () => {
    setAuthView('login');
  };

  const handleTabChange = (tab) => {
    setCurrentTab(tab);
    setSearchQuery('');
    setAppliedSearch('');
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setAppliedSearch(searchQuery);
  };

  const handleUserUpdate = (updatedUser) => {
    setUser(updatedUser);
  };

  const handleProductCreated = () => {
    setRefreshKey(prev => prev + 1);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    if (authView === 'landing') {
      return (
        <Landing 
          onShowLogin={() => setAuthView('login')} 
          onShowSignup={() => setAuthView('signup')} 
        />
      );
    }
    if (authView === 'signup') {
      return (
        <Signup 
          onSignupSuccess={handleSignupSuccess} 
          onBackToLogin={() => setAuthView('login')} 
        />
      );
    }
    return (
      <Login 
        onLogin={handleLogin} 
        onBackToSignup={() => setAuthView('signup')} 
      />
    );
  }

  const renderPage = () => {
    switch (currentTab) {
      case 'feed':
        return <Feed searchQuery={appliedSearch} />;
      case 'favorites':
        return <Favorites />;
      case 'home':
        return <Home key={refreshKey} user={user} onTabChange={handleTabChange} />;
      case 'orders':
        return <Orders />;
      case 'analytics':
        return <Analytics />;
      default:
        return <Feed searchQuery={appliedSearch} />;
    }
  };

  return (
    <div className="app">
      <Navbar 
        user={user} 
        onLogout={handleLogout}
        currentTab={currentTab}
        onTabChange={handleTabChange}
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        onSearch={handleSearch}
        onOpenProfile={() => setShowProfile(true)}
      />
      <main className="main-content">
        {renderPage()}
      </main>

      {/* Floating Add Product Button */}
      <button 
        className="fab-add-product"
        onClick={() => setShowCreateProduct(true)}
        title="Add new product"
      >
        +
      </button>

      {/* Profile Modal */}
      {showProfile && (
        <ProfileModal 
          user={user} 
          onClose={() => setShowProfile(false)}
          onUserUpdate={handleUserUpdate}
        />
      )}

      {/* Create Product Modal */}
      {showCreateProduct && (
        <CreateProductModal 
          onClose={() => setShowCreateProduct(false)}
          onProductCreated={handleProductCreated}
        />
      )}
    </div>
  );
}

export default App;
