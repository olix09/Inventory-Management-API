# 🏬 Inventory Management API

A production-ready backend system for managing inventory items, built with **Django** and **Django REST Framework**.

---

## 🚀 Features
- 🔑 **User Authentication** with JWT tokens  
- 📦 **Inventory CRUD** (Create, Read, Update, Delete)  
- 📊 **Inventory Level Tracking** with change history  
- 🔎 **Filtering & Search** by category, price range, and stock level  
- 📑 **Pagination & Sorting** for large datasets  
- 🔐 **Permissions** (users can only manage their own inventory)  
- 🌍 **Deployment Ready** for Heroku/PythonAnywhere  

---

## 🛠 Tech Stack
- Python 3.11+  
- Django 5+  
- Django REST Framework  
- PostgreSQL (or SQLite for local dev)  
- JWT Authentication (`djangorestframework-simplejwt`)  

---

## 📂 Project Structure

---

## ⚙️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com/your-username/inventory_api.git
cd inventory_api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
🔑 Authentication

The API uses JWT Authentication.

Obtain Token

POST /api/token/


Refresh Token

POST /api/token/refresh/


Use token in requests:

Authorization: Bearer <your-token>

📊 API Endpoints
Users

POST /api/users/register/ → Register a new user

POST /api/token/ → Login & get JWT token

Inventory

GET /api/inventory/ → List items (with filters, pagination, sorting)

POST /api/inventory/ → Create new item

GET /api/inventory/<id>/ → Retrieve item details

PUT /api/inventory/<id>/ → Update item

DELETE /api/inventory/<id>/ → Delete item

Inventory Changes

GET /api/inventory/<id>/changes/ → View change history for an item

Use Procfile and runtime.txt for Heroku.

Run migrations after deployment:

python manage.py migrate

🧪 Testing

Run tests with:

python manage.py test
