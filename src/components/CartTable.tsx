import React from 'react';
import { Plus, Minus, Trash2 } from 'lucide-react';
import { useCart } from '../contexts/CartContext';

const CartTable: React.FC = () => {
  const { items, updateQuantity, removeFromCart, getTotalPrice } = useCart();

  if (items.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <div className="w-24 h-24 mx-auto bg-gray-100 rounded-full flex items-center justify-center">
            <span className="text-4xl">🛒</span>
          </div>
        </div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">Your cart is empty</h3>
        <p className="text-gray-600">Add some products to get started!</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Desktop Table */}
      <div className="hidden md:block overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-4 px-2 font-semibold text-gray-900">Product</th>
              <th className="text-left py-4 px-2 font-semibold text-gray-900">Size</th>
              <th className="text-left py-4 px-2 font-semibold text-gray-900">Price</th>
              <th className="text-left py-4 px-2 font-semibold text-gray-900">Quantity</th>
              <th className="text-left py-4 px-2 font-semibold text-gray-900">Total</th>
              <th className="text-left py-4 px-2 font-semibold text-gray-900">Action</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item, index) => (
              <tr key={`${item.product.id}-${item.size}`} className="border-b border-gray-100">
                <td className="py-4 px-2">
                  <div className="flex items-center space-x-4">
                    <img
                      src={item.product.image_url}
                      alt={item.product.name}
                      className="w-16 h-16 object-cover rounded-lg"
                    />
                    <div>
                      <h4 className="font-semibold text-gray-900">{item.product.name}</h4>
                      <p className="text-sm text-gray-600">SKU: {item.product.id}</p>
                    </div>
                  </div>
                </td>
                <td className="py-4 px-2">
                  <span className="bg-gray-100 px-2 py-1 rounded text-sm font-medium">
                    {item.size}
                  </span>
                </td>
                <td className="py-4 px-2 font-semibold text-blue-600">
                  {parseFloat(item.product.price).toFixed(2)} Birr
                </td>
                <td className="py-4 px-2">
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => updateQuantity(item.product.id, item.size, item.quantity - 1)}
                      className="p-1 rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors duration-200"
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                    <span className="min-w-[2rem] text-center font-semibold">
                      {item.quantity}
                    </span>
                    <button
                      onClick={() => updateQuantity(item.product.id, item.size, item.quantity + 1)}
                      disabled={item.quantity >= item.product.stock}
                      className="p-1 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                </td>
                <td className="py-4 px-2 font-bold text-gray-900">
                  {(parseFloat(item.product.price) * item.quantity).toFixed(2)} Birr
                </td>
                <td className="py-4 px-2">
                  <button
                    onClick={() => removeFromCart(item.product.id, item.size)}
                    className="p-2 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors duration-200"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile Cards */}
      <div className="md:hidden space-y-4">
        {items.map((item, index) => (
          <div key={`${item.product.id}-${item.size}`} className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex space-x-4">
              <img
                src={item.product.image_url}
                alt={item.product.name}
                className="w-20 h-20 object-cover rounded-lg"
              />
              <div className="flex-1 space-y-2">
                <h4 className="font-semibold text-gray-900">{item.product.name}</h4>
                <div className="flex items-center space-x-2">
                  <span className="bg-gray-100 px-2 py-1 rounded text-xs font-medium">
                    {item.size}
                  </span>
                  <span className="text-blue-600 font-semibold">
                    {parseFloat(item.product.price).toFixed(2)} Birr
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => updateQuantity(item.product.id, item.size, item.quantity - 1)}
                      className="p-1 rounded-lg border border-gray-300 hover:bg-gray-50"
                    >
                      <Minus className="w-4 h-4" />
                    </button>
                    <span className="min-w-[2rem] text-center font-semibold">
                      {item.quantity}
                    </span>
                    <button
                      onClick={() => updateQuantity(item.product.id, item.size, item.quantity + 1)}
                      disabled={item.quantity >= item.product.stock}
                      className="p-1 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50"
                    >
                      <Plus className="w-4 h-4" />
                    </button>
                  </div>
                  <button
                    onClick={() => removeFromCart(item.product.id, item.size)}
                    className="p-2 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors duration-200"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
                <div className="text-right">
                  <span className="font-bold text-gray-900">
                    Total: {(parseFloat(item.product.price) * item.quantity).toFixed(2)} Birr
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Cart Total */}
      <div className="bg-gray-50 rounded-xl p-6">
        <div className="flex justify-between items-center text-xl font-bold">
          <span>Subtotal:</span>
          <span className="text-blue-600">{getTotalPrice().toFixed(2)} Birr</span>
        </div>
      </div>
    </div>
  );
};

export default CartTable;