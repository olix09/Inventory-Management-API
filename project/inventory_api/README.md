# Inventory Management API

A comprehensive Django REST Framework API for managing inventory items with user authentication, CRUD operations, and advanced filtering capabilities.

## Features

- 🔐 **User Authentication**: Token-based authentication with registration, login, and profile management
- 📦 **Inventory Management**: Full CRUD operations for inventory items
- 📊 **Advanced Filtering**: Filter by category, price range, stock levels, and more
- 📈 **Inventory Tracking**: Track all inventory changes with detailed history
- 🔍 **Search & Sort**: Powerful search across multiple fields with flexible sorting
- 📑 **Pagination**: Built-in pagination for efficient data handling
- ⚡ **Stock Alerts**: Automatic low stock and out of stock detection
- 📱 **RESTful API**: Clean, well-documented REST API endpoints

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone and setup the project:**
```bash
cd inventory_api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Create a superuser:**
```bash
python manage.py createsuperuser
```

4. **Load sample data (optional):**
```bash
python manage.py seed_data --users 3 --items 30
```

5. **Start the development server:**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication
- `POST /api/users/register/` - Register a new user
- `POST /api/users/login/` - Login and get auth token
- `GET /api/users/profile/` - Get current user profile
- `POST /api/users/logout/` - Logout (delete token)

### Inventory Management
- `GET /api/inventory/` - List inventory items (with filtering)
- `POST /api/inventory/` - Create new inventory item
- `GET /api/inventory/{id}/` - Get item details
- `PUT/PATCH /api/inventory/{id}/` - Update item
- `DELETE /api/inventory/{id}/` - Delete item
- `POST /api/inventory/{id}/adjust_quantity/` - Adjust item quantity

### Special Endpoints
- `GET /api/inventory/low_stock/` - Get low stock items
- `GET /api/inventory/out_of_stock/` - Get out of stock items
- `GET /api/inventory/summary/` - Get inventory summary stats

### Inventory Changes
- `GET /api/inventory-changes/` - List inventory changes
- `GET /api/inventory-changes/recent/` - Get recent changes

## Usage Examples

### 1. Register a new user
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com", 
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Login and get token
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

### 3. Create an inventory item
```bash
curl -X POST http://localhost:8000/api/inventory/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Mouse",
    "description": "Ergonomic wireless mouse",
    "quantity": 25,
    "price": "29.99",
    "minimum_stock_level": 10,
    "priority": "medium"
  }'
```

### 4. Filter inventory items
```bash
# Get low stock items
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/inventory/?low_stock=true"

# Filter by price range
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/inventory/?price_min=10&price_max=100"

# Search and sort
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/inventory/?search=mouse&ordering=-price"
```

## Project Structure

```
inventory_api/
├── inventory_management/       # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                     # User management app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── inventory/                 # Inventory management app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── filters.py
│   └── management/commands/
├── requirements.txt
└── README.md
```

## Key Features Explained

### 1. **User Authentication**
- Custom user model with email and username
- Token-based authentication for API access
- User can only manage their own inventory items

### 2. **Inventory Models**
- **InventoryItem**: Core inventory item with quantity, price, category
- **InventoryChange**: Tracks all changes to inventory quantities
- **Category**: Organize items into categories

### 3. **Advanced Filtering**
- Filter by category, price range, stock levels
- Search across name, description, SKU
- Sort by any field (name, price, quantity, date)

### 4. **Stock Management**
- Minimum/maximum stock level settings
- Automatic low stock detection
- Out of stock and overstocked alerts
- Quantity adjustment with change tracking

### 5. **API Features**
- Comprehensive error handling
- Input validation
- Pagination for large datasets
- RESTful design principles

## Environment Variables

Create a `.env` file based on `.env.example`:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Deployment

This API is ready for deployment on platforms like:
- **Heroku**: Includes `Procfile` and `runtime.txt`
- **PythonAnywhere**: Compatible with their Django hosting
- **DigitalOcean App Platform**: Ready for containerized deployment

### For Heroku Deployment:
1. Install Heroku CLI
2. Create Heroku app: `heroku create your-app-name`
3. Set environment variables: `heroku config:set SECRET_KEY=your-secret`
4. Deploy: `git push heroku main`
5. Run migrations: `heroku run python manage.py migrate`

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please create an issue in the repository or contact the maintainers.