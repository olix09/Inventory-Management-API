import React from 'react';
import { Link } from 'react-router-dom';
import { XCircle, ArrowLeft, Home } from 'lucide-react';

const CancelPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full text-center space-y-8">
        <div className="text-red-500 mb-6">
          <XCircle className="w-20 h-20 mx-auto" />
        </div>
        
        <div className="space-y-4">
          <h1 className="text-3xl font-bold text-gray-900">Payment Canceled</h1>
          <p className="text-lg text-gray-600">
            Your payment was canceled. No charges have been made to your account.
          </p>
        </div>

        <div className="space-y-4">
          <p className="text-gray-600">
            Your cart items are still saved. You can continue shopping or try checkout again.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/cart"
              className="inline-flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold transition-colors duration-200"
            >
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Cart</span>
            </Link>
            
            <Link
              to="/"
              className="inline-flex items-center justify-center space-x-2 border border-gray-300 hover:border-gray-400 text-gray-700 hover:text-gray-900 px-6 py-3 rounded-xl font-semibold transition-colors duration-200"
            >
              <Home className="w-5 h-5" />
              <span>Continue Shopping</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CancelPage;