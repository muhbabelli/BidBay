import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Feed from './pages/Feed';
import Favorites from './pages/Favorites';
import Home from './pages/Home';
import { auth } from './services/api';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentTab, setCurrentTab] = useState('feed');
  const [searchQuery, setSearchQuery] = useState('');
  const [appliedSearch, setAppliedSearch] = useState('');

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
  };

  const handleLogout = () => {
    auth.logout();
    setUser(null);
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

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  const renderPage = () => {
    switch (currentTab) {
      case 'feed':
        return <Feed searchQuery={appliedSearch} />;
      case 'favorites':
        return <Favorites />;
      case 'home':
        return <Home user={user} />;
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
      />
      <main className="main-content">
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
