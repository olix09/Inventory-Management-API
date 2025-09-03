import React from 'react';
import { Link } from 'react-router-dom';
import { Facebook, Instagram, Twitter, Mail, Phone, MapPin } from 'lucide-react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-blue-800 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">AB</span>
              </div>
              <span className="text-xl font-bold">Arif Brand</span>
            </div>
            <p className="text-gray-300 text-sm leading-relaxed">
              Premium quality clothing and accessories for the modern lifestyle. 
              Discover our curated collection of fashion essentials.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-white transition-colors duration-200">
                <Facebook className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors duration-200">
                <Instagram className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors duration-200">
                <Twitter className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Shop */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Shop</h3>
            <div className="space-y-2">
              <Link to="/category/t-shirts" className="block text-gray-300 hover:text-white transition-colors duration-200">
                T-Shirts
              </Link>
              <Link to="/category/jackets" className="block text-gray-300 hover:text-white transition-colors duration-200">
                Jackets
              </Link>
              <Link to="/category/shoes" className="block text-gray-300 hover:text-white transition-colors duration-200">
                Shoes
              </Link>
              <Link to="/category/bags" className="block text-gray-300 hover:text-white transition-colors duration-200">
                Bags
              </Link>
              <Link to="/category/accessories" className="block text-gray-300 hover:text-white transition-colors duration-200">
                Accessories
              </Link>
            </div>
          </div>

          {/* Help */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Help</h3>
            <div className="space-y-2">
              <Link to="/contact" className="block text-gray-300 hover:text-white transition-colors duration-200">
                Contact Us
              </Link>
              <Link to="/terms" className="block text-gray-300 hover:text-white transition-colors duration-200">
                Terms of Service
              </Link>
              <Link to="/privacy" className="block text-gray-300 hover:text-white transition-colors duration-200">
                Privacy Policy
              </Link>
              <a href="#" className="block text-gray-300 hover:text-white transition-colors duration-200">
                Shipping Info
              </a>
              <a href="#" className="block text-gray-300 hover:text-white transition-colors duration-200">
                Returns
              </a>
            </div>
          </div>

          {/* Contact Info */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Contact</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-2 text-gray-300">
                <Mail className="w-4 h-4" />
                <span className="text-sm">info@arifbrand.com</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-300">
                <Phone className="w-4 h-4" />
                <span className="text-sm">+251 911 123 456</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-300">
                <MapPin className="w-4 h-4" />
                <span className="text-sm">Addis Ababa, Ethiopia</span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400 text-sm">
          <p>&copy; {currentYear} Arif Brand. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;