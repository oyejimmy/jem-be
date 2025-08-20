# JEM Backend (FastAPI)

## Overview

FastAPI backend for JEM jewelry shop. Provides CRUD APIs for products with SQLAlchemy ORM and Pydantic schemas.

## Enhanced Product Schema

The product model includes comprehensive fields for jewelry management:

### Core Fields
- `id`: Unique product identifier (integer)
- `unique_key`: Unique UUID key for secure identification (auto-generated)
- `name`: Short product name (e.g., "Diamond Ring")
- `full_name`: Full descriptive title (e.g., "18K Gold Diamond Engagement Ring")
- `type`: Jewelry type (optional, since category_id covers this)
- `description`: Detailed product description

### Pricing & Currency
- `retail_price`: Original price (required)
- `offer_price`: Discounted/sale price (optional)
- `currency`: Currency code (default: "PKR")
- `delivery_charges`: Shipping cost (default: 0.0)

### Inventory Management
- `stock`: Current available quantity
- `status`: Product status ("available", "out_of_stock", "sold")
- `available`: Total quantity ever added (for tracking supply)
- `sold`: Total units sold (for analytics)

### Media & Organization
- `images`: JSON string of image URLs (e.g., `["image1.jpg", "image2.jpg"]`)
- `category_id`: Link to category table
- `created_at`: Timestamp of creation

### Example Product JSON
```json
{
  "id": 101,
  "unique_key": "1295cb6d-acf6-4c04-bef2-70d6fc63ce81",
  "name": "Diamond Ring",
  "full_name": "18K White Gold Diamond Engagement Ring",
  "retail_price": 2500,
  "offer_price": 2000,
  "currency": "PKR",
  "description": "Elegant 18K gold ring with a brilliant-cut diamond.",
  "delivery_charges": 200,
  "stock": 5,
  "status": "available",
  "images": ["ring1.jpg", "ring2.jpg", "ring3.jpg"],
  "available": 20,
  "sold": 15,
  "category_id": 1,
  "created_at": "2025-08-19T18:45:00"
}
```

## Project Structure

```
app/
  main.py
  core/
    config.py
  db/
    base_class.py
    base.py
    session.py
  models/
    model.py          # Enhanced Product model
    category.py       # Category model with relationship
    order.py          # Order models
    user.py           # User model
  schemas/
    product.py        # Updated Pydantic schemas
    order.py          # Order schemas
    user.py           # User schemas
  api/
    v1/
      api.py
      endpoints/
        products.py   # Enhanced CRUD endpoints with filtering
        categories.py # Category endpoints with counts
        orders.py     # Order endpoints
        auth.py       # Authentication endpoints
  deps/
    auth.py           # Authentication dependencies
init_db.py
seed_data.py         # Enhanced sample data
test_endpoints.py    # API testing script
requirements.txt
```

## Setup

1) Install dependencies
```
pip install -r requirements.txt
```

2) (Optional) Set DB URL, default is SQLite `./test.db`
```
# PowerShell
$env:DATABASE_URL="sqlite:///./test.db"
```

3) Initialize database
```
python init_db.py
```

4) Seed with sample data
```
python seed_data.py
```

5) Run server
```
uvicorn app.main:app --reload
```

## API Endpoints

### 🎯 Main Products Endpoint (For Frontend Table)
- `GET /api/v1/products/` - **MAIN endpoint for frontend table** - Get all products
- `GET /api/v1/products/{id}` - Get specific product

### 🛒 Product Details for Order Placement
- `GET /api/v1/products/details/{id}` - **Get detailed product info for order/WhatsApp by ID**
- `GET /api/v1/products/details/by-key/{unique_key}` - **Get detailed product info by unique key**
- `GET /api/v1/products/by-key/{unique_key}` - **Get product by unique key**

This endpoint provides everything needed when a user clicks on a product to place an order:

```json
{
  "product": {
    "id": 1,
    "name": "Diamond Ring",
    "full_name": "18K Gold Diamond Engagement Ring",
    "description": "Elegant ring with brilliant-cut diamond",
    "retail_price": 2500,
    "offer_price": 2000,
    "currency": "PKR",
    "delivery_charges": 200,
    "stock": 5,
    "status": "available",
    "images": ["ring1.jpg", "ring2.jpg"],
    "category": "Rings"
  },
          "whatsapp_info": {
            "phone": "+92-300-1234567",
            "message": "Hi! I'm interested in Diamond Ring (Key: 1295cb6d-acf6-4c04-bef2-70d6fc63ce81). Price: PKR 2000. Can you provide more details?",
            "whatsapp_url": "https://wa.me/923001234567?text=Hi! I'm interested in Diamond Ring (Key: 1295cb6d-acf6-4c04-bef2-70d6fc63ce81). Price: PKR 2000. Can you provide more details?"
        },
  "order_info": {
    "total_price": 2200,
    "delivery_time": "2-3 business days",
    "payment_methods": ["Cash on Delivery", "Bank Transfer", "Online Payment"],
    "warranty": "1 year warranty",
    "return_policy": "7 days return policy"
  }
}
```

### 📂 Category-Specific Endpoints
- `GET /api/v1/products/rings` - All rings
- `GET /api/v1/products/pendants` - All pendants
- `GET /api/v1/products/bracelets` - All bracelets
- `GET /api/v1/products/bangles` - All bangles
- `GET /api/v1/products/anklets` - All anklets
- `GET /api/v1/products/ear-studs` - All ear studs
- `GET /api/v1/products/earrings` - All earrings
- `GET /api/v1/products/hoops` - All hoops
- `GET /api/v1/products/hair-accessories` - All hair accessories
- `GET /api/v1/products/wall-frames` - All wall frames
- `GET /api/v1/products/under-299` - All products under 299
- `GET /api/v1/products/combos` - All combos

### 🔍 Product Filtering & Pagination
- `GET /api/v1/products/?category_name=Rings` - Filter by category name
- `GET /api/v1/products/?category_id=1` - Filter by category ID
- `GET /api/v1/products/?status=available` - Filter by status
- `GET /api/v1/products/?limit=10&offset=0` - Pagination

### 🔧 Admin Endpoints (Require Authentication)
- `POST /api/v1/products/` - Create new product
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

### 📊 Categories
- `GET /api/v1/categories/` - List all category names
- `GET /api/v1/categories/with-counts` - Categories with product counts
- `POST /api/v1/categories/` - Create category (admin only)

### 📦 Orders
- `POST /api/v1/orders/` - Create new order
- `GET /api/v1/orders/` - List orders (admin only)
- `GET /api/v1/orders/{id}` - Get specific order (admin only)

### 🔐 Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration

## 🔑 Unique Key System

Every product has a **unique UUID key** that is automatically generated when the product is created. This provides:

- **Secure identification** - UUIDs are harder to guess than sequential IDs
- **External sharing** - Safe to use in URLs and WhatsApp messages
- **Data integrity** - Unique across all systems
- **Future-proof** - No collisions when merging databases

### **Unique Key Features:**
- ✅ **Auto-generated** on product creation
- ✅ **Immutable** - Cannot be changed once created
- ✅ **Indexed** for fast lookups
- ✅ **Included in WhatsApp messages** for easy reference

## 🎯 How Admin Operations Work

### **Key Point: Single Source of Truth**
When you perform admin operations (create, update, delete), the changes automatically appear in ALL endpoints:

1. **CREATE a product** → Automatically appears in:
   - `GET /products/` (main list)
   - `GET /products/{category_name}` (if it matches the category)
   - `GET /products/?category_name={category_name}` (filtered results)

2. **UPDATE a product** → Changes automatically reflect in all endpoints

3. **DELETE a product** → Automatically removed from all endpoints

### **For Your Frontend Table**
You only need **ONE main endpoint**: `GET /api/v1/products/`
- Use query parameters to filter: `?category_name=Hoops&status=available`
- No need to create separate APIs for different views

## 🛒 Order Flow & WhatsApp Integration

### **User Journey:**
1. User sees products in table: `GET /products/`
2. User clicks on a product
3. Frontend calls: `GET /products/details/{id}`
4. User sees detailed product info with WhatsApp button
5. User clicks WhatsApp button → Opens WhatsApp with pre-filled message

### **WhatsApp Integration:**
- **Pre-filled message** with product details
- **Direct link** to WhatsApp chat
- **Includes** product name, price, and ID
- **Automatic URL generation** for easy sharing

### **Order Information:**
- **Total price** (including delivery)
- **Delivery time**
- **Payment methods**
- **Warranty and return policy**

## Usage Examples

### Frontend Table (Main Use Case)
```bash
# Show all products in table
curl http://localhost:8000/api/v1/products/

# Show only hoops in table
curl "http://localhost:8000/api/v1/products/?category_name=Hoops"

# Show available rings with pagination
curl "http://localhost:8000/api/v1/products/?category_name=Rings&status=available&limit=10&offset=0"
```

### Product Details for Order Placement
```bash
# Get detailed product info for order/WhatsApp by ID
curl http://localhost:8000/api/v1/products/details/1

# Get detailed product info by unique key
curl http://localhost:8000/api/v1/products/details/by-key/1295cb6d-acf6-4c04-bef2-70d6fc63ce81

# Get product by unique key
curl http://localhost:8000/api/v1/products/by-key/1295cb6d-acf6-4c04-bef2-70d6fc63ce81
```

### Category-Specific Pages
```bash
# Rings page
curl http://localhost:8000/api/v1/products/rings

# Hoops page
curl http://localhost:8000/api/v1/products/hoops

# Pendants page
curl http://localhost:8000/api/v1/products/pendants
```

### Admin Operations
```bash
# Create new product (requires admin auth)
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{"name":"New Ring","retail_price":1000,"category_id":1}'

# Update product (requires admin auth)
curl -X PUT http://localhost:8000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{"retail_price":1200}'

# Delete product (requires admin auth)
curl -X DELETE http://localhost:8000/api/v1/products/1
```

### Categories with Analytics
```bash
# Get categories with product counts
curl http://localhost:8000/api/v1/categories/with-counts
```

## Frontend Implementation Guide

### **Product Table Page:**
```javascript
// Get all products for table
const products = await fetch('/api/v1/products/').then(r => r.json());

// Filter by category
const rings = await fetch('/api/v1/products/?category_name=Rings').then(r => r.json());
```

### **Product Detail Page:**
```javascript
// Get detailed product info when user clicks on product
const productDetails = await fetch('/api/v1/products/details/1').then(r => r.json());

// Display product info
const { product, whatsapp_info, order_info } = productDetails;

// WhatsApp button
const whatsappButton = `<a href="${whatsapp_info.whatsapp_url}" target="_blank">
  Contact via WhatsApp
</a>`;
```

## Testing

Run the test script to verify all endpoints:
```bash
python test_endpoints.py
```

## Docs

API Documentation: http://127.0.0.1:8000/docs
