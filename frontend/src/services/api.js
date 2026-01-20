const API_BASE = '';

function getToken() {
  return localStorage.getItem('bidbay_token');
}

function authHeaders() {
  const token = getToken();
  return token ? { 'Authorization': `Bearer ${token}` } : {};
}

async function handleResponse(response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || 'Request failed');
  }
  return data;
}

export const auth = {
  async login(email, password) {
    const form = new URLSearchParams();
    form.append('username', email);
    form.append('password', password);

    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form.toString(),
    });
    const data = await handleResponse(response);
    localStorage.setItem('bidbay_token', data.access_token);
    return data;
  },

  async register(email, password, fullName, phoneNumber) {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email,
        password,
        full_name: fullName,
        phone_number: phoneNumber || null
      }),
    });
    return handleResponse(response);
  },

  async getMe() {
    const response = await fetch(`${API_BASE}/auth/me`, {
      headers: authHeaders(),
    });
    return handleResponse(response);
  },

  async updateMe(userData) {
    const response = await fetch(`${API_BASE}/auth/me`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders(),
      },
      body: JSON.stringify(userData),
    });
    return handleResponse(response);
  },

  logout() {
    localStorage.removeItem('bidbay_token');
  },

  isLoggedIn() {
    return !!getToken();
  }
};

export const products = {
  async list(params = {}) {
    const query = new URLSearchParams();
    if (params.status) query.append('status', params.status);
    if (params.category_id) query.append('category_id', params.category_id);
    if (params.seller_id) query.append('seller_id', params.seller_id);
    if (params.q) query.append('q', params.q);

    const response = await fetch(API_BASE + '/products/?' + query.toString(), {
      headers: authHeaders(),
    });
    return handleResponse(response);
  },

  async getFeed(q = null) {
    const query = new URLSearchParams();
    if (q) query.append('q', q);
    const response = await fetch(API_BASE + '/products/feed?' + query.toString(), {
      headers: authHeaders(),
    });
    return handleResponse(response);
  },

  async getMyProducts() {
    const response = await fetch(API_BASE + '/products/my-products', {
      headers: authHeaders(),
    });
    return handleResponse(response);
  },

  async getFavorites() {
    const response = await fetch(API_BASE + '/products/favorites', {
      headers: authHeaders(),
    });
    return handleResponse(response);
  },

  async get(id) {
    const response = await fetch(API_BASE + '/products/' + id, {
      headers: authHeaders(),
    });
    return handleResponse(response);
  },

  async create(productData) {
    const response = await fetch(API_BASE + '/products/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders(),
      },
      body: JSON.stringify(productData),
    });
    return handleResponse(response);
  },

  async addImage(productId, imageUrl) {
    const response = await fetch(API_BASE + '/products/' + productId + '/images', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders(),
      },
      body: JSON.stringify({ image_url: imageUrl, position: 0 }),
    });
    return handleResponse(response);
  },

  async update(id, productData) {
    const response = await fetch(API_BASE + '/products/' + id, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders(),
      },
      body: JSON.stringify(productData),
    });
    return handleResponse(response);
  },

  async delete(id) {
    const response = await fetch(API_BASE + '/products/' + id, {
      method: 'DELETE',
      headers: authHeaders(),
    });
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || 'Delete failed');
    }
    return true;
  }
};

export const bids = {
  async place(productId, amount) {
    const response = await fetch(API_BASE + '/bids/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders(),
      },
      body: JSON.stringify({ product_id: productId, amount }),
    });
    return handleResponse(response);
  },

  async getMyBids() {
    const response = await fetch(API_BASE + '/bids/me', {
      headers: authHeaders(),
    });
    return handleResponse(response);
  },

  async getProductBids(productId) {
    const response = await fetch(API_BASE + '/bids/product/' + productId, {
      headers: authHeaders(),
    });
    return handleResponse(response);
  },

  async acceptBid(bidId) {
    const response = await fetch(API_BASE + '/bids/' + bidId + '/accept', {
      method: 'POST',
      headers: authHeaders(),
    });
    return handleResponse(response);
  },

  async rejectBid(bidId) {
    const response = await fetch(API_BASE + '/bids/' + bidId + '/reject', {
      method: 'POST',
      headers: authHeaders(),
    });
    return handleResponse(response);
  }
};

export const favorites = {
  async add(productId) {
    const response = await fetch(API_BASE + '/favorites/' + productId, {
      method: 'POST',
      headers: authHeaders(),
    });
    return handleResponse(response);
  },

  async remove(productId) {
    const response = await fetch(API_BASE + '/favorites/' + productId, {
      method: 'DELETE',
      headers: authHeaders(),
    });
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || 'Remove failed');
    }
    return true;
  },

  async list() {
    const response = await fetch(API_BASE + '/favorites/', {
      headers: authHeaders(),
    });
    return handleResponse(response);
  }
};

export const categories = {
  async list() {
    const response = await fetch(API_BASE + '/categories/', {
      headers: authHeaders(),
    });
    return handleResponse(response);
  }
};
