export interface Category {
  id: number;
  name: string;
  slug: string;
  image_url: string;
}

export interface Product {
  id: number;
  category: number;
  name: string;
  slug: string;
  description: string;
  price: string;
  image_url: string;
  sizes: string[];
  active: boolean;
  created_at: string;
  stock: number;
}

export interface CartItem {
  product: Product;
  quantity: number;
  size: string;
}

export interface User {
  uid: string;
  email: string;
  displayName?: string;
}

export interface Order {
  id: number;
  user_uid: string;
  email: string;
  total: string;
  status: 'pending' | 'paid' | 'canceled';
  payment_ref?: string;
  created_at: string;
  items: OrderItem[];
}

export interface OrderItem {
  id: number;
  product: Product;
  quantity: number;
  price: string;
  size: string;
}

export interface ContactForm {
  name: string;
  email: string;
  message: string;
}