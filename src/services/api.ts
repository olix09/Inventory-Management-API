const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

class ApiError extends Error {
  constructor(message: string, public status: number) {
    super(message);
    this.name = 'ApiError';
  }
}

const handleResponse = async (response: Response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ message: 'An error occurred' }));
    throw new ApiError(errorData.message || 'An error occurred', response.status);
  }
  return response.json();
};

export const api = {
  // Categories
  getCategories: async () => {
    const response = await fetch(`${API_BASE_URL}/categories/`);
    return handleResponse(response);
  },

  // Products
  getProducts: async (categorySlug?: string) => {
    const url = categorySlug 
      ? `${API_BASE_URL}/products/?category=${categorySlug}`
      : `${API_BASE_URL}/products/`;
    const response = await fetch(url);
    return handleResponse(response);
  },

  getProduct: async (id: number) => {
    const response = await fetch(`${API_BASE_URL}/products/${id}/`);
    return handleResponse(response);
  },

  // Orders
  createOrder: async (orderData: any, token: string) => {
    const response = await fetch(`${API_BASE_URL}/orders/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(orderData),
    });
    return handleResponse(response);
  },

  getOrders: async (token: string) => {
    const response = await fetch(`${API_BASE_URL}/orders/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },

  // Checkout
  checkoutCBE: async (orderData: any, token: string) => {
    const response = await fetch(`${API_BASE_URL}/checkout/cbe/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(orderData),
    });
    return handleResponse(response);
  },

  checkoutTelebirr: async (orderData: any, token: string) => {
    const response = await fetch(`${API_BASE_URL}/checkout/telebirr/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(orderData),
    });
    return handleResponse(response);
  },

  // Contact
  submitContact: async (contactData: any) => {
    const response = await fetch(`${API_BASE_URL}/contact/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(contactData),
    });
    return handleResponse(response);
  }
};