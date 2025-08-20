#!/usr/bin/env python3
"""
Simple test script for the enhanced product API endpoints.
Run this after starting the server: uvicorn app.main:app --reload
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_endpoints():
    """Test the new API endpoints"""
    
    print("🧪 Testing Enhanced Product API Endpoints...")
    
    # Test 1: Get all products (MAIN endpoint for frontend table)
    print("\n1. Testing GET /products/ (MAIN endpoint for frontend table)")
    try:
        response = requests.get(f"{BASE_URL}/products/")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Found {len(products)} total products")
            print(f"   This is your MAIN API for the frontend table!")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Test product details for order placement
    print("\n2. Testing GET /products/details/1 (Product details for order)")
    try:
        response = requests.get(f"{BASE_URL}/products/details/1")
        if response.status_code == 200:
            details = response.json()
            print(f"✅ Product details retrieved successfully!")
            print(f"   Product: {details['product']['name']}")
            print(f"   Unique Key: {details['product']['unique_key']}")
            print(f"   Price: {details['product']['currency']} {details['product']['offer_price'] or details['product']['retail_price']}")
            print(f"   Total Price: {details['product']['currency']} {details['order_info']['total_price']}")
            print(f"   WhatsApp: {details['whatsapp_info']['phone']}")
            print(f"   WhatsApp Message includes Key: {'Key:' in details['whatsapp_info']['message']}")
            print(f"   Delivery: {details['order_info']['delivery_time']}")
            
            # Store unique key for further testing
            unique_key = details['product']['unique_key']
            
            # Test 2b: Test product details by unique key
            print(f"\n2b. Testing GET /products/details/by-key/{unique_key[:8]}... (by unique key)")
            try:
                response_by_key = requests.get(f"{BASE_URL}/products/details/by-key/{unique_key}")
                if response_by_key.status_code == 200:
                    details_by_key = response_by_key.json()
                    print(f"✅ Product details by unique key retrieved successfully!")
                    print(f"   Same product: {details_by_key['product']['name'] == details['product']['name']}")
                else:
                    print(f"❌ Failed: {response_by_key.status_code}")
            except Exception as e:
                print(f"❌ Error: {e}")
                
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Test all category-specific endpoints
    print("\n3. Testing Category-Specific Endpoints:")
    categories = [
        "rings", "pendants", "bracelets", "bangles", "anklets",
        "ear-studs", "earrings", "hoops", "hair-accessories", 
        "wall-frames", "under-299", "combos"
    ]
    
    for category in categories:
        try:
            response = requests.get(f"{BASE_URL}/products/{category}")
            if response.status_code == 200:
                products = response.json()
                print(f"   ✅ {category}: {len(products)} products")
            else:
                print(f"   ❌ {category}: Failed {response.status_code}")
        except Exception as e:
            print(f"   ❌ {category}: Error {e}")
    
    # Test 4: Filter by category name (alternative method)
    print("\n4. Testing GET /products/?category_name=Hoops")
    try:
        response = requests.get(f"{BASE_URL}/products/?category_name=Hoops")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Found {len(products)} products in Hoops category")
            if products:
                print(f"   First hoop: {products[0]['name']}")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Filter by status
    print("\n5. Testing GET /products/?status=available")
    try:
        response = requests.get(f"{BASE_URL}/products/?status=available")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Found {len(products)} available products")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Categories with counts
    print("\n6. Testing GET /categories/with-counts")
    try:
        response = requests.get(f"{BASE_URL}/categories/with-counts")
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Found {len(categories)} categories with counts:")
            for cat in categories:
                print(f"   - {cat['name']}: {cat['product_count']} products")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 7: Pagination
    print("\n7. Testing GET /products/?limit=2&offset=0")
    try:
        response = requests.get(f"{BASE_URL}/products/?limit=2&offset=0")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Pagination works: {len(products)} products (limit=2)")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def explain_admin_operations():
    """Explain how admin operations work"""
    print("\n" + "="*60)
    print("🔧 ADMIN OPERATIONS EXPLANATION")
    print("="*60)
    
    print("\n📋 HOW ADMIN OPERATIONS WORK:")
    print("1. When you CREATE a product (POST /products/):")
    print("   - It automatically appears in GET /products/ (main list)")
    print("   - It automatically appears in category-specific endpoints")
    print("   - It automatically appears in filtered results")
    
    print("\n2. When you UPDATE a product (PUT /products/{id}):")
    print("   - Changes automatically reflect in all endpoints")
    print("   - No need to update multiple places")
    
    print("\n3. When you DELETE a product (DELETE /products/{id}):")
    print("   - It's automatically removed from all endpoints")
    print("   - No need to delete from multiple places")
    
    print("\n🎯 KEY POINT: You only need ONE main endpoint for your frontend table:")
    print("   GET /products/ - This shows ALL products")
    print("   Use query parameters to filter: ?category_name=Hoops&status=available")
    
    print("\n📖 EXAMPLES FOR FRONTEND:")
    print("   - Show all products: GET /products/")
    print("   - Show only hoops: GET /products/?category_name=Hoops")
    print("   - Show available hoops: GET /products/?category_name=Hoops&status=available")
    print("   - Show rings with pagination: GET /products/?category_name=Rings&limit=10&offset=0")

def explain_order_flow():
    """Explain the order flow and WhatsApp integration"""
    print("\n" + "="*60)
    print("🛒 ORDER FLOW & WHATSAPP INTEGRATION")
    print("="*60)
    
    print("\n📱 USER JOURNEY:")
    print("1. User sees products in table: GET /products/")
    print("2. User clicks on a product")
    print("3. Frontend calls: GET /products/details/{id}")
    print("4. User sees detailed product info with WhatsApp button")
    print("5. User clicks WhatsApp button → Opens WhatsApp with pre-filled message")
    
    print("\n🔗 WHATSAPP INTEGRATION:")
    print("   - Pre-filled message with product details")
    print("   - Direct link to WhatsApp chat")
    print("   - Includes product name, price, and ID")
    
    print("\n💳 ORDER INFORMATION:")
    print("   - Total price (including delivery)")
    print("   - Delivery time")
    print("   - Payment methods")
    print("   - Warranty and return policy")
    
    print("\n📖 FRONTEND IMPLEMENTATION:")
    print("   - Use GET /products/details/{id} for product detail page")
    print("   - Display all product images, prices, descriptions")
    print("   - Show WhatsApp button with whatsapp_url")
    print("   - Show order information for purchase decisions")

if __name__ == "__main__":
    print("🚀 Starting API Endpoint Tests...")
    test_endpoints()
    explain_admin_operations()
    explain_order_flow()
    print("\n✨ Testing completed!")
    print("\n📖 Available endpoints:")
    print("   GET /api/v1/products/ - ALL PRODUCTS (main endpoint for frontend)")
    print("   GET /api/v1/products/details/{id} - Product details for order/WhatsApp")
    print("   GET /api/v1/products/rings - All rings")
    print("   GET /api/v1/products/hoops - All hoops")
    print("   GET /api/v1/products/pendants - All pendants")
    print("   GET /api/v1/products/bracelets - All bracelets")
    print("   GET /api/v1/products/bangles - All bangles")
    print("   GET /api/v1/products/anklets - All anklets")
    print("   GET /api/v1/products/ear-studs - All ear studs")
    print("   GET /api/v1/products/earrings - All earrings")
    print("   GET /api/v1/products/hair-accessories - All hair accessories")
    print("   GET /api/v1/products/wall-frames - All wall frames")
    print("   GET /api/v1/products/under-299 - All products under 299")
    print("   GET /api/v1/products/combos - All combos")
    print("\n🔧 Admin endpoints (require authentication):")
    print("   POST /api/v1/products/ - Create product")
    print("   PUT /api/v1/products/{id} - Update product")
    print("   DELETE /api/v1/products/{id} - Delete product")
