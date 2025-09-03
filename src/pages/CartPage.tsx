import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingBag, CreditCard } from 'lucide-react';
import CartTable from '../components/CartTable';
import { useCart } from '../contexts/CartContext';
import { useAuth } from '../contexts/AuthContext';

const CartPage: React.FC = () => {
  const { items, getTotalPrice, getTotalItems } = useCart();
  const { currentUser } = useAuth();
  const navigate = useNavigate();

  const handleCheckout = () => {
    if (!currentUser) {
      navigate('/signin?redirect=/cart');
      return;
    }
    
    // Navigate to checkout page (to be implemented)
    navigate('/checkout');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center space-y-4 mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 flex items-center justify-center space-x-3">
            <ShoppingBag className="w-8 h-8 text-blue-600" />
            <span>Shopping Cart</span>
          </h1>
          {items.length > 0 && (
            <p className="text-lg text-gray-600">
              {getTotalItems()} {getTotalItems() === 1 ? 'item' : 'items'} in your cart
            </p>
          )}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Cart Items */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <CartTable />
            </div>
          </div>

          {/* Order Summary */}
          {items.length > 0 && (
            <div className="lg:col-span-1">
              <div className="bg-white rounded-xl shadow-lg p-6 sticky top-24">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Order Summary</h2>
                
                <div className="space-y-4 mb-6">
                  <div className="flex justify-between text-gray-600">
                    <span>Subtotal ({getTotalItems()} items)</span>
                    <span>{getTotalPrice().toFixed(2)} Birr</span>
                  </div>
                  <div className="flex justify-between text-gray-600">
                    <span>Shipping</span>
                    <span>Free</span>
                  </div>
                  <div className="border-t border-gray-200 pt-4">
                    <div className="flex justify-between text-xl font-bold text-gray-900">
                      <span>Total</span>
                      <span className="text-blue-600">{getTotalPrice().toFixed(2)} Birr</span>
                    </div>
                  </div>
                </div>

                <button
                  onClick={handleCheckout}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 px-6 rounded-xl font-semibold transition-colors duration-200 flex items-center justify-center space-x-2"
                >
                  <CreditCard className="w-5 h-5" />
                  <span>Proceed to Checkout</span>
                </button>

                {!currentUser && (
                  <p className="text-sm text-gray-600 text-center mt-4">
                    <Link to="/signin" className="text-blue-600 hover:text-blue-700">
                      Sign in
                    </Link>
                    {' '}to continue with checkout
                  </p>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Continue Shopping */}
        {items.length === 0 && (
          <div className="text-center mt-8">
            <Link 
              to="/"
              className="inline-flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold transition-colors duration-200"
            >
              <ShoppingBag className="w-5 h-5" />
              <span>Continue Shopping</span>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default CartPage;