# Arif Brand E-Commerce Application

A modern, full-stack e-commerce platform built with React and Django, featuring secure payments, inventory management, and a beautiful responsive design.

## 🚀 Overview

Arif Brand is a comprehensive e-commerce solution that provides:
- Beautiful, responsive frontend built with React and Tailwind CSS
- Robust Django REST API backend with inventory management
- Firebase Authentication for secure user management
- CBE and Telebirr payment integration (placeholder implementation)
- Cloudinary integration for image management
- Admin panel for product and order management

## 🛠 Technology Stack

**Frontend:**
- React 18 with TypeScript
- Tailwind CSS for styling
- React Router DOM for navigation
- Context API for state management
- Firebase Authentication
- React Hot Toast for notifications

**Backend:**
- Django 4.2 with Django REST Framework
- SQLite (development) / PostgreSQL (production)
- Firebase Admin SDK for authentication
- Cloudinary for image storage
- Email integration for contact forms

**Payments:**
- CBE Banking integration (placeholder)
- Telebirr mobile wallet integration (placeholder)

## 📦 Features

### Core Functionality
- **Product Catalog:** Browse products by categories (T-Shirts, Jackets, Shoes, Bags, Accessories)
- **Product Details:** Modal popup with image carousel, size selection, and quantity controls
- **Shopping Cart:** Persistent cart with localStorage, quantity management, and price calculations
- **User Authentication:** Email/password registration and login with Firebase
- **Order Management:** Complete order history for authenticated users
- **Stock Management:** Real-time inventory tracking with automatic stock decrements
- **Contact Form:** Integrated contact form with email notifications

### Design Features
- **Responsive Design:** Optimized for mobile, tablet, and desktop devices
- **Modern UI:** Clean, professional design with smooth animations
- **Accessibility:** Proper contrast ratios and keyboard navigation
- **Performance:** Optimized images and efficient state management

## 🏗 Installation

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+ and pip
- Firebase project (for authentication)
- Cloudinary account (for image storage)

### Frontend Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Configure environment variables:**
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   VITE_CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
   VITE_CLOUDINARY_UPLOAD_PRESET=your_upload_preset
   
   # Firebase Configuration
   VITE_FIREBASE_API_KEY=your_firebase_api_key
   VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
   VITE_FIREBASE_PROJECT_ID=your_project_id
   VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
   VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
   VITE_FIREBASE_APP_ID=1:123456789:web:abcdefghijk
   
   # Payment Integration
   VITE_CBE_KEY=your_cbe_api_key
   VITE_TELEBIRR_KEY=your_telebirr_api_key
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

5. **Configure environment variables:**
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Cloudinary Settings
   CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
   CLOUDINARY_BASE_URL=https://res.cloudinary.com
   
   # Email Settings
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   CONTACT_RECEIVER_EMAIL=info@arifbrand.com
   
   # Firebase Admin SDK
   GOOGLE_APPLICATION_CREDENTIALS=path/to/firebase-service-account.json
   
   # Payment Integration
   CBE_API_KEY=your_cbe_api_key_here
   TELEBIRR_API_KEY=your_telebirr_api_key_here
   ```

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Seed sample data:**
   ```bash
   python manage.py seed_products
   ```

9. **Start development server:**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Firebase Authentication Setup

1. **Create Firebase Project:**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project
   - Enable Authentication with Email/Password provider

2. **Get Configuration:**
   - Go to Project Settings > General > Your apps
   - Add a web app and copy the configuration
   - Update frontend `.env` file with Firebase config

3. **Generate Service Account:**
   - Go to Project Settings > Service accounts
   - Generate new private key
   - Download JSON file and update backend `.env` file

### Cloudinary Setup

1. **Create Cloudinary Account:**
   - Sign up at [Cloudinary](https://cloudinary.com/)
   - Get your cloud name from the dashboard

2. **Create Upload Preset:**
   - Go to Settings > Upload presets
   - Create unsigned upload preset
   - Update environment variables

### Payment Integration Setup

#### CBE Banking Integration
```bash
# Contact CBE for API credentials and documentation
# Update backend/.env with:
CBE_API_KEY=your_actual_cbe_api_key
```

#### Telebirr Integration
```bash
# Contact Ethio Telecom for Telebirr API access
# Update backend/.env with:
TELEBIRR_API_KEY=your_actual_telebirr_api_key
```

## 📊 Admin Panel

Access the Django admin at `http://localhost:8000/admin/` to:
- Manage product categories and inventory
- Upload product images (store Cloudinary URLs)
- View and manage customer orders
- Track stock movements and inventory levels
- Handle customer inquiries

## 🚀 Deployment

### Frontend Deployment (Netlify/Vercel)

1. **Build for production:**
   ```bash
   npm run build
   ```

2. **Deploy to hosting platform:**
   - Connect your repository
   - Set environment variables
   - Deploy from `dist` folder

### Backend Deployment (Railway/Render/Heroku)

1. **Prepare for production:**
   - Update `ALLOWED_HOSTS` in settings
   - Configure PostgreSQL database
   - Set up environment variables
   - Configure static file serving

2. **Database migration:**
   ```bash
   python manage.py migrate --run-syncdb
   python manage.py collectstatic --noinput
   python manage.py seed_products
   ```

## ⚠️ Limitations

### Payment Integration
- **CBE and Telebirr:** Require live API credentials and proper integration
- Current implementation includes placeholder flows only
- Actual payment processing needs production API keys and testing

### Authentication
- **Firebase Admin:** Requires service account JSON file (`GOOGLE_APPLICATION_CREDENTIALS`)
- Email confirmation is disabled by default
- Social login providers not implemented

### Image Storage
- **Cloudinary:** Requires cloud name and upload preset configuration
- Images must be uploaded via Cloudinary dashboard or API
- Automatic image optimization available with proper setup

### Email Integration
- **SMTP Configuration:** Console backend used in development
- Production requires SMTP credentials (Gmail, SendGrid, etc.)
- Contact form submissions logged to console in development

### Database
- **SQLite:** Suitable for development and small deployments
- **PostgreSQL:** Recommended for production environments
- Database migrations included for both scenarios

### Cross-Domain Deployment
- **CORS Configuration:** Update `CORS_ALLOWED_ORIGINS` for different domains
- **Environment Variables:** Update frontend API base URL for production backend
- **Security:** Configure proper security headers and HTTPS in production

## 🎯 Next Steps

1. **Obtain API credentials** for CBE and Telebirr payment providers
2. **Set up Firebase project** with proper authentication configuration
3. **Configure Cloudinary** for image upload and management
4. **Set up email service** for contact form and order confirmations
5. **Deploy to production** with proper environment configuration
6. **Test payment flows** with actual payment provider credentials

## 📞 Support

For technical support or questions about setup, please contact the development team or refer to the respective service documentation for Firebase, Cloudinary, CBE, and Telebirr integrations.

---

**Arif Brand** - Premium Fashion for the Modern Lifestyle