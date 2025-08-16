# Inventory Management API Documentation

## Overview
This is a Django REST Framework-based API for managing inventory items with user authentication, CRUD operations, and advanced filtering capabilities.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
This API uses Token Authentication. Include the token in the Authorization header:
```
Authorization: Token your_token_here
```

## API Endpoints

### Authentication Endpoints

#### Register User
- **POST** `/api/users/register/`
- **Body:**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Login User
- **POST** `/api/users/login/`
- **Body:**
```json
{
    "username": "john_doe",
    "password": "securepassword123"
}
```

#### Get User Profile
- **GET** `/api/users/profile/`
- **Headers:** `Authorization: Token your_token`

#### Logout User
- **POST** `/api/users/logout/`
- **Headers:** `Authorization: Token your_token`

### Inventory Management

#### List Inventory Items
- **GET** `/api/inventory/`
- **Query Parameters:**
  - `page`: Page number
  - `page_size`: Items per page
  - `ordering`: Sort by field (e.g., `-last_updated`, `name`, `price`)
  - `search`: Search in name, description, SKU
  - `category`: Filter by category ID
  - `low_stock`: Filter low stock items (true/false)
  - `out_of_stock`: Filter out of stock items (true/false)
  - `price_min`, `price_max`: Price range filter

#### Create Inventory Item
- **POST** `/api/inventory/`
- **Body:**
```json
{
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse",
    "quantity": 25,
    "price": "29.99",
    "category": 1,
    "minimum_stock_level": 10,
    "maximum_stock_level": 100,
    "priority": "medium",
    "sku": "WM-001",
    "location": "A1-B2"
}
```

#### Get Inventory Item Details
- **GET** `/api/inventory/{id}/`

#### Update Inventory Item
- **PUT** `/api/inventory/{id}/`
- **PATCH** `/api/inventory/{id}/`

#### Delete Inventory Item
- **DELETE** `/api/inventory/{id}/`

#### Adjust Item Quantity
- **POST** `/api/inventory/{id}/adjust_quantity/`
- **Body:**
```json
{
    "quantity_change": 10,
    "reason": "Restocked from supplier",
    "notes": "Received new shipment"
}
```

### Special Inventory Endpoints

#### Low Stock Items
- **GET** `/api/inventory/low_stock/`

#### Out of Stock Items
- **GET** `/api/inventory/out_of_stock/`

#### Overstocked Items
- **GET** `/api/inventory/overstocked/`

#### Inventory Summary
- **GET** `/api/inventory/summary/`

### Inventory Changes

#### List Inventory Changes
- **GET** `/api/inventory-changes/`
- **Query Parameters:**
  - `change_type`: Filter by change type
  - `inventory_item`: Filter by item ID

#### Recent Changes
- **GET** `/api/inventory-changes/recent/`

#### Changes by Type
- **GET** `/api/inventory-changes/by_type/`

### Categories

#### List Categories
- **GET** `/api/categories/`

#### Create Category
- **POST** `/api/categories/`
- **Body:**
```json
{
    "name": "Electronics",
    "description": "Electronic devices and components"
}
```

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

## Filtering Examples

### Filter by Price Range
```
GET /api/inventory/?price_min=10&price_max=100
```

### Filter Low Stock Items in Electronics Category
```
GET /api/inventory/?low_stock=true&category_name=electronics
```

### Search and Sort
```
GET /api/inventory/?search=mouse&ordering=-price
```

## Pagination
All list endpoints support pagination:
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/inventory/?page=3",
    "previous": "http://localhost:8000/api/inventory/?page=1",
    "results": [...]
}
```

## Sample Data
Run this command to populate the database with sample data:
```bash
python manage.py seed_data --users 3 --items 30
```

This creates 3 sample users with 30 inventory items each, across different categories.