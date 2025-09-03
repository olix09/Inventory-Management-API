import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { CheckCircle, Package, Home } from 'lucide-react';

const SuccessPage: React.FC = () => {
  const location = useLocation();
  const orderId = location.state?.orderId;

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full text-center space-y-8">
        <div className="text-green-500 mb-6">
          <CheckCircle className="w-20 h-20 mx-auto" />
        </div>
        
        <div className="space-y-4">
          <h1 className="text-3xl font-bold text-gray-900">Payment Successful!</h1>
          <p className="text-lg text-gray-600">
            Thank you for your order. Your payment has been processed successfully.
          </p>
          
          {orderId && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <p className="text-sm text-green-800">
                Order ID: <span className="font-mono font-semibold">#{orderId}</span>
              </p>
            </div>
          )}
        </div>

        <div className="space-y-4">
          <p className="text-gray-600">
            We've sent a confirmation email with your order details. 
            Your items will be shipped within 2-3 business days.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/orders"
              className="inline-flex items-center justify-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold transition-colors duration-200"
            >
              <Package className="w-5 h-5" />
              <span>View Orders</span>
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

export default SuccessPage;