import React from 'react';
import { Link } from 'react-router-dom';
import { Category } from '../types';

interface CategoryTileProps {
  category: Category;
}

const CategoryTile: React.FC<CategoryTileProps> = ({ category }) => {
  return (
    <Link 
      to={`/category/${category.slug}`}
      className="group relative block overflow-hidden rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
    >
      <div className="aspect-square">
        <img
          src={category.image_url}
          alt={category.name}
          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 p-6">
          <h3 className="text-white text-xl font-bold mb-2 group-hover:text-blue-200 transition-colors duration-200">
            {category.name}
          </h3>
          <span className="inline-block bg-white text-gray-900 px-4 py-2 rounded-full text-sm font-medium group-hover:bg-blue-100 transition-colors duration-200">
            Shop Now
          </span>
        </div>
      </div>
    </Link>
  );
};

export default CategoryTile;