# E-Commerce Platform

A full-stack e-commerce application with a FastAPI backend and React/TypeScript frontend.

---

## 📁 Project Structure

```
ecommerce/
├── ecommerce-backend/      # FastAPI backend application
├── my-ecommerce/           # React/TypeScript frontend application
├── fastapi/                # Python virtual environment
├── package.json            # Root package configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🏗️ Backend Structure (`ecommerce-backend/`)

### Main Application Files

```
ecommerce-backend/
├── app/
│   ├── __init__.py         # Application initialization
│   ├── main.py             # FastAPI app entry point
│   ├── auth.py             # Authentication logic
│   ├── config.py           # Configuration settings
│   ├── crud.py             # Create, Read, Update, Delete operations
│   ├── database.py         # Database connection setup
│   ├── models.py           # SQLAlchemy database models
│   ├── schemas.py          # Pydantic request/response schemas
│   ├── fix_password.py     # Password utility functions
│   │
│   ├── core/               # Core utilities
│   │   ├── __init__.py
│   │   ├── exceptions.py   # Custom exceptions
│   │   ├── security.py     # Security utilities (JWT, hashing)
│   │   └── redis_client.py # Redis cache client
│   │
│   └── routers/            # API route handlers
│       ├── __init__.py
│       ├── auth.py         # Authentication endpoints
│       ├── cart.py         # Shopping cart endpoints
│       ├── orders.py       # Order management endpoints
│       ├── products.py     # Product catalog endpoints
│       ├── users.py        # User profile endpoints
│       └── deps.py         # Route dependencies
│
├── alembic/                # Database migration tool
│   ├── env.py              # Migration environment config
│   ├── script.py.mako      # Migration template
│   └── versions/           # Migration scripts
│       ├── 67e9c508e996_initial_migration.py
│       └── cb46eb9b75a4_add_role_to_user.py
│
└── alembic.ini             # Alembic configuration file
```

### Backend Features

| File | Purpose |
|------|---------|
| `auth.py` | User authentication & session management |
| `config.py` | Environment variables & app configuration |
| `crud.py` | Database query operations |
| `database.py` | SQLAlchemy setup & connection pooling |
| `models.py` | Database schema definitions |
| `schemas.py` | Request validation & response models |
| `security.py` | JWT tokens, password hashing, encryption |
| `redis_client.py` | Caching layer for performance |

### Backend Routers

- **`auth.py`** - Login, register, logout, token refresh
- **`users.py`** - User profile, preferences, account management
- **`products.py`** - Browse catalog, search, filter products
- **`cart.py`** - Add/remove items, cart management
- **`orders.py`** - Create orders, order history, payment tracking

---

## 🎨 Frontend Structure (`my-ecommerce/`)

### Main Application Files

```
my-ecommerce/
├── src/
│   ├── App.tsx             # Root component
│   ├── main.tsx            # React entry point
│   ├── App.css             # Global styles
│   ├── index.css           # Base styles
│   │
│   ├── api/                # API client & services
│   │   └── ...
│   │
│   ├── components/         # Reusable React components
│   │   └── ...
│   │
│   ├── pages/              # Page components
│   │   └── ...
│   │
│   ├── context/            # Global state management
│   │   └── ...
│   │
│   ├── assets/             # Images, icons, fonts
│   │   └── ...
│   │
│   └── styles/             # Style modules
│       └── ...
│
├── public/                 # Static assets
│   └── images/
│
├── vite.config.ts          # Vite bundler configuration
├── tsconfig.json           # TypeScript configuration
├── tsconfig.app.json       # App-specific TS config
├── tsconfig.node.json      # Node TS config
├── package.json            # Dependencies & scripts
├── index.html              # HTML entry point
├── eslint.config.js        # ESLint configuration
└── README.md              # Frontend documentation
```

### Frontend Architecture

| Directory | Purpose |
|-----------|---------|
| `api/` | HTTP client & API endpoints |
| `components/` | Reusable UI components (buttons, forms, etc.) |
| `pages/` | Full page components (Home, Product, Cart, Checkout) |
| `context/` | React Context for global state (auth, cart, user) |
| `assets/` | Images, icons, and media files |
| `styles/` | CSS modules and styling utilities |

---

## 🔄 Application Flow

### User Registration & Authentication Flow

```
┌─────────────────────────────────────────────────────┐
│  User enters credentials in Frontend                │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Frontend: POST /api/auth/register                  │
│  (email, password, name)                            │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Backend: validate credentials                      │
│  - Check email not registered                       │
│  - Hash password with bcrypt/argon2                 │
│  - Store user in database                           │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Backend: Generate JWT token                        │
│  - Access token (short-lived)                       │
│  - Refresh token (long-lived)                       │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Frontend: Store tokens in localStorage/cookie      │
│  Redirect to home page                              │
└─────────────────────────────────────────────────────┘
```

### Shopping & Order Flow

```
┌─────────────────────────────────────────────────────┐
│  User Browsing Products                             │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Frontend: GET /api/products                        │
│  (with filters: category, price, search)            │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Backend: Query database for products               │
│  Cache results in Redis for performance             │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Frontend: Display product catalog                  │
│  User selects product and adds to cart              │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Frontend: POST /api/cart                           │
│  (product_id, quantity)                             │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Backend: Add item to user's cart                   │
│  Update cart total in database                      │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  User Proceeds to Checkout                          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Frontend: GET /api/cart                            │
│  Display order summary & checkout form              │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  User Completes Payment                             │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Frontend: POST /api/orders                         │
│  (cart_items, shipping_address, payment_method)    │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Backend: Create order record                       │
│  - Clear user's cart                                │
│  - Update product inventory                         │
│  - Save order details                               │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  Backend: Return order confirmation                 │
│  Frontend: Show success message & order details     │
└─────────────────────────────────────────────────────┘
```

### Request/Response Flow

```
┌──────────────────────────────────────────────────────────────┐
│              React Frontend (my-ecommerce)                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Pages → Components → Context State                   │  │
│  └────────────────┬───────────────────────────────────────┘  │
│                   │                                           │
│                   ▼                                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  API Client (Axios/Fetch)                             │  │
│  │  - Sets Authorization header with JWT                 │  │
│  │  - Handles request/response interceptors              │  │
│  └────────────────┬───────────────────────────────────────┘  │
└────────────────────┼──────────────────────────────────────────┘
                     │ HTTP Request
                     │ (GET/POST/PUT/DELETE)
                     ▼
┌──────────────────────────────────────────────────────────────┐
│              FastAPI Backend (ecommerce-backend)             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  API Routers (FastAPI)                                │  │
│  │  - Validate JWT token in header                       │  │
│  │  - Check user permissions                             │  │
│  │  - Route to appropriate handler                       │  │
│  └────────────────┬───────────────────────────────────────┘  │
│                   │                                           │
│                   ▼                                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Business Logic (CRUD)                                │  │
│  │  - Validate request data                              │  │
│  │  - Process business rules                             │  │
│  └────────────────┬───────────────────────────────────────┘  │
│                   │                                           │
│                   ▼                                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Cache Layer (Redis)                                  │  │
│  │  - Check if data exists in cache                      │  │
│  │  - Return cached data if available                    │  │
│  └────────────────┬───────────────────────────────────────┘  │
│                   │                                           │
│                   ▼                                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Database (SQLAlchemy Models)                         │  │
│  │  - Query/Update/Delete database records              │  │
│  │  - Execute migrations                                 │  │
│  └────────────────┬───────────────────────────────────────┘  │
└────────────────────┼──────────────────────────────────────────┘
                     │ HTTP Response (JSON)
                     │ + JWT (if auth endpoint)
                     ▼
┌──────────────────────────────────────────────────────────────┐
│              React Frontend (my-ecommerce)                    │
│  - Update component state                                    │
│  - Re-render UI with new data                                │
│  - Store tokens in localStorage/cookies                      │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Caching**: Redis
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: bcrypt/argon2
- **Migrations**: Alembic

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **Package Manager**: npm
- **Styling**: CSS
- **Linting**: ESLint

---

## 🚀 Getting Started

### Backend Setup

```bash
# Activate Python virtual environment
cd ecommerce
.\fastapi\Scripts\Activate.ps1  # On Windows
# source fastapi/bin/activate   # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the FastAPI server
python ecommerce-backend/app/main.py
# Server runs on http://localhost:8000
```

### Frontend Setup

```bash
# Install dependencies
cd my-ecommerce
npm install

# Start development server
npm run dev
# Frontend runs on http://localhost:5173
```

---

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Create new user account
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Refresh access token

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile
- `GET /api/users/{id}` - Get user public profile

### Products
- `GET /api/products` - List products (with filters)
- `GET /api/products/{id}` - Get product details
- `GET /api/products/search` - Search products

### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart` - Add item to cart
- `PUT /api/cart/{item_id}` - Update cart item quantity
- `DELETE /api/cart/{item_id}` - Remove item from cart

### Orders
- `POST /api/orders` - Create new order
- `GET /api/orders` - Get user's orders
- `GET /api/orders/{id}` - Get order details

---

## 🗄️ Database Schema

### Core Models
- **User** - User accounts with authentication
- **Product** - Product catalog information
- **Cart** - Shopping cart items per user
- **Order** - Customer orders
- **OrderItem** - Individual items in an order

### Key Migrations
1. `initial_migration.py` - Create base tables
2. `add_role_to_user.py` - Add role-based access control

---

## 📝 Notes

- JWT tokens are validated on every protected endpoint
- Redis caches frequently accessed data (products, categories)
- Database migrations are managed through Alembic
- User roles support different permission levels

---

## 📞 Support

For questions or issues, refer to individual component documentation or contact the development team.
