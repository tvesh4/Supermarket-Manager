
# ================================================
# SUPERMARKET MANAGEMENT SYSTEM - COMPLETE SOLUTION
# ================================================
# Author: Tvesha Kumar
# Version: 2.0
# Features: Products, Customers, Sales, Reports, Search
# ================================================

import datetime

# ================================================
# GLOBAL VARIABLES AND SAMPLE DATA
# ================================================

# Products database
products = [
    {"id": 101, "name": "Milk", "category": "Dairy", "price": 2.99, "stock": 50, "min_stock": 10},
    {"id": 102, "name": "Bread", "category": "Bakery", "price": 1.49, "stock": 30, "min_stock": 5},
    {"id": 103, "name": "Eggs", "category": "Dairy", "price": 3.99, "stock": 25, "min_stock": 5},
    {"id": 104, "name": "Apples", "category": "Produce", "price": 0.99, "stock": 100, "min_stock": 20},
    {"id": 105, "name": "Chicken", "category": "Meat", "price": 8.99, "stock": 15, "min_stock": 5},
    {"id": 106, "name": "Rice", "category": "Grains", "price": 4.49, "stock": 40, "min_stock": 10},
    {"id": 107, "name": "Coffee", "category": "Beverages", "price": 6.99, "stock": 20, "min_stock": 5},
    {"id": 108, "name": "Cookies", "category": "Snacks", "price": 3.49, "stock": 35, "min_stock": 8}
]

# Customers database
customers = [
    {"id": 1001, "name": "Alice Smith", "phone": "555-0101", "email": "alice@email.com", 
     "loyalty_points": 150, "total_spent": 450.75, "join_date": "2024-01-15"},
    {"id": 1002, "name": "Bob Johnson", "phone": "555-0102", "email": "bob@email.com", 
     "loyalty_points": 75, "total_spent": 225.50, "join_date": "2024-02-20"},
    {"id": 1003, "name": "Charlie Brown", "phone": "555-0103", "email": "charlie@email.com", 
     "loyalty_points": 200, "total_spent": 600.25, "join_date": "2024-01-05"}
]

# Sales history
sales_history = [
    {"sale_id": 5001, "customer_id": 1001, "date": "2024-03-15", 
     "items": [{"product_id": 101, "name": "Milk", "quantity": 2, "price": 2.99},
               {"product_id": 102, "name": "Bread", "quantity": 1, "price": 1.49}],
     "subtotal": 7.47, "tax": 0.60, "total": 8.07, "payment_method": "Credit Card"},
    {"sale_id": 5002, "customer_id": 1002, "date": "2024-03-16",
     "items": [{"product_id": 105, "name": "Chicken", "quantity": 1, "price": 8.99},
               {"product_id": 106, "name": "Rice", "quantity": 2, "price": 4.49},
               {"product_id": 104, "name": "Apples", "quantity": 3, "price": 0.99}],
     "subtotal": 19.44, "tax": 1.55, "total": 20.99, "payment_method": "Cash"}
]

# Global counters
current_sale_id = 5002
tax_rate = 0.085  # 8.5% tax

# ================================================
# UTILITY FUNCTIONS
# ================================================

def clear_screen():
    """Clear the console screen (cross-platform)"""
    print("\n" * 50)

def print_header(title):
    """Print a formatted header"""
    clear_screen()
    print("=" * 60)   
    print(f"{title:^60}")
    print("=" * 60)

def get_valid_input(prompt, input_type="str"):
    """Get validated user input"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("❌ Input cannot be empty!")
                continue
                
            if input_type == "int":
                return int(user_input)
            elif input_type == "float":
                return float(user_input)
            elif input_type == "positive_int":
                value = int(user_input)
                if value <= 0:
                    print("❌ Value must be positive!")
                    continue
                return value
            elif input_type == "positive_float":
                value = float(user_input)
                if value <= 0:
                    print("❌ Value must be positive!")
                    continue
                return round(value, 2)
            else:
                return user_input
        except ValueError:
            print(f"❌ Please enter a valid {input_type}!")
        except Exception as e:
            print(f"❌ Error: {e}")

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:.2f}"

# ================================================
# PRODUCT MANAGEMENT FUNCTIONS
# ================================================

def add_product():
    """Add a new product to inventory"""
    print_header("ADD NEW PRODUCT")
    
    # Generate new product ID
    if products:
        new_id = max(p["id"] for p in products) + 1
    else:
        new_id = 101
    
    print(f"New Product ID: {new_id}")
    print("-" * 40)
    
    name = get_valid_input("Product Name: ", "str")
    category = get_valid_input("Category: ", "str")
    price = get_valid_input("Price ($): ", "positive_float")
    stock = get_valid_input("Initial Stock: ", "positive_int")
    min_stock = get_valid_input("Minimum Stock Level: ", "positive_int")
    
    # Create new product dictionary
    new_product = {
        "id": new_id,
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
        "min_stock": min_stock
    }
    
    products.append(new_product)
    products.sort(key=lambda x: x["id"])
    
    print(f"\n✅ Product '{name}' added successfully!")
    print(f"   ID: {new_id}, Price: {format_currency(price)}, Stock: {stock}")

def view_products(sort_by="id"):
    """Display all products with sorting options"""
    print_header("PRODUCT INVENTORY")
    
    if not products:
        print("No products in inventory!")
        return
    
    # Sorting options
    if sort_by == "name":
        sorted_products = sorted(products, key=lambda x: x["name"])
    elif sort_by == "category":
        sorted_products = sorted(products, key=lambda x: x["category"])
    elif sort_by == "price_low":
        sorted_products = sorted(products, key=lambda x: x["price"])
    elif sort_by == "price_high":
        sorted_products = sorted(products, key=lambda x: x["price"], reverse=True)
    elif sort_by == "stock_low":
        sorted_products = sorted(products, key=lambda x: x["stock"])
    else:
        sorted_products = sorted(products, key=lambda x: x["id"])
    
    # Display table header
    print(f"{'ID':<5} {'Name':<15} {'Category':<10} {'Price':<10} {'Stock':<10} {'Status':<10}")
    print("-" * 65)
    
    # Display each product
    for product in sorted_products:
        status = "✅ OK" if product["stock"] >= product["min_stock"] else "⚠️ LOW"
        print(f"{product['id']:<5} {product['name']:<15} {product['category']:<10} "
              f"{format_currency(product['price']):<10} {product['stock']:<10} {status:<10}")
    
    print("-" * 65)
    
    # Display statistics
    total_value = sum(p["price"] * p["stock"] for p in products)
    low_stock_count = len([p for p in products if p["stock"] < p["min_stock"]])
    
    print(f"\n📊 Inventory Statistics:")
    print(f"   • Total Products: {len(products)}")
    print(f"   • Total Value: {format_currency(total_value)}")
    print(f"   • Low Stock Items: {low_stock_count}")
    
    return sorted_products

def update_product():
    """Update existing product details"""
    view_products()
    
    if not products:
        return
    
    try:
        product_id = get_valid_input("\nEnter Product ID to update: ", "int")
        
        # Find product
        product = next((p for p in products if p["id"] == product_id), None)
        
        if not product:
            print(f"❌ Product ID {product_id} not found!")
            return
        
        print(f"\nCurrent details for '{product['name']}':")
        print(f"   Name: {product['name']}")
        print(f"   Category: {product['category']}")
        print(f"   Price: {format_currency(product['price'])}")
        print(f"   Stock: {product['stock']}")
        print(f"   Min Stock: {product['min_stock']}")
        print("-" * 40)
        
        print("Enter new values (press Enter to keep current):")
        
        new_name = input(f"New Name [{product['name']}]: ").strip()
        new_category = input(f"New Category [{product['category']}]: ").strip()
        
        price_input = input(f"New Price [${product['price']:.2f}]: ").strip()
        stock_input = input(f"New Stock [{product['stock']}]: ").strip()
        min_stock_input = input(f"New Min Stock [{product['min_stock']}]: ").strip()
        
        # Update fields if new values provided
        if new_name:
            product['name'] = new_name
        if new_category:
            product['category'] = new_category
        if price_input:
            product['price'] = float(price_input)
        if stock_input:
            product['stock'] = int(stock_input)
        if min_stock_input:
            product['min_stock'] = int(min_stock_input)
        
        print(f"\n✅ Product '{product['name']}' updated successfully!")
        
    except Exception as e:
        print(f"❌ Error updating product: {e}")

def delete_product():
    """Remove a product from inventory"""
    view_products()
    
    if not products:
        return
    
    try:
        product_id = get_valid_input("\nEnter Product ID to delete: ", "int")
        
        # Find product
        product = next((p for p in products if p["id"] == product_id), None)
        
        if not product:
            print(f"❌ Product ID {product_id} not found!")
            return
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete '{product['name']}'? (yes/no): ").lower()
        
        if confirm == "yes":
            products.remove(product)
            print(f"✅ Product '{product['name']}' deleted successfully!")
        else:
            print("❌ Deletion cancelled.")
            
    except Exception as e:
        print(f"❌ Error deleting product: {e}")

def check_low_stock():
    """Display products with low stock"""
    print_header("LOW STOCK ALERT")
    
    low_stock_items = [p for p in products if p["stock"] < p["min_stock"]]
    
    if not low_stock_items:
        print("✅ All products have sufficient stock!")
        return
    
    # Sort by how low the stock is
    low_stock_items.sort(key=lambda x: x["stock"] - x["min_stock"])
    
    print("⚠️  URGENT - RESTOCK NEEDED ⚠️")
    print("=" * 60)
    print(f"{'ID':<5} {'Product':<15} {'Current':<10} {'Minimum':<10} {'Needed':<10}")
    print("-" * 60)
    
    for product in low_stock_items:
        needed = product["min_stock"] - product["stock"]
        print(f"{product['id']:<5} {product['name']:<15} {product['stock']:<10} "
              f"{product['min_stock']:<10} {needed:<10}")
    
    print("=" * 60)

# ================================================
# CUSTOMER MANAGEMENT FUNCTIONS
# ================================================

def add_customer():
    """Register a new customer"""
    print_header("REGISTER NEW CUSTOMER")
    
    # Generate new customer ID
    if customers:
        new_id = max(c["id"] for c in customers) + 1
    else:
        new_id = 1001
    
    print(f"New Customer ID: {new_id}")
    print("-" * 40)
    
    name = get_valid_input("Full Name: ", "str")
    phone = get_valid_input("Phone Number: ", "str")
    email = get_valid_input("Email Address: ", "str")
    
    # Get current date
    join_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Create new customer
    new_customer = {
        "id": new_id,
        "name": name,
        "phone": phone,
        "email": email,
        "loyalty_points": 0,
        "total_spent": 0.0,
        "join_date": join_date
    }
    
    customers.append(new_customer)
    customers.sort(key=lambda x: x["id"])
    
    print(f"\n✅ Customer '{name}' registered successfully!")
    print(f"   Welcome to our loyalty program!")

def view_customers():
    """Display all customers"""
    print_header("CUSTOMER DATABASE")
    
    if not customers:
        print("No customers registered yet!")
        return
    
    # Sort by ID
    sorted_customers = sorted(customers, key=lambda x: x["id"])
    
    # Display table
    print(f"{'ID':<6} {'Name':<20} {'Phone':<12} {'Loyalty':<10} {'Spent':<12}")
    print("-" * 65)
    
    for customer in sorted_customers:
        print(f"{customer['id']:<6} {customer['name']:<20} {customer['phone']:<12} "
              f"{customer['loyalty_points']:<10} {format_currency(customer['total_spent']):<12}")
    
    print("-" * 65)
    
    # Display statistics
    total_customers = len(customers)
    total_loyalty = sum(c["loyalty_points"] for c in customers)
    total_spent = sum(c["total_spent"] for c in customers)
    avg_spent = total_spent / total_customers if total_customers > 0 else 0
    
    print(f"\n📊 Customer Statistics:")
    print(f"   • Total Customers: {total_customers}")
    print(f"   • Total Loyalty Points: {total_loyalty}")
    print(f"   • Total Revenue: {format_currency(total_spent)}")
    print(f"   • Average per Customer: {format_currency(avg_spent)}")

def calculate_loyalty_points(customer_id, purchase_amount):
    """Calculate and update loyalty points for a customer"""
    customer = next((c for c in customers if c["id"] == customer_id), None)
    
    if customer:
        # 1 point per $10 spent
        points_earned = int(purchase_amount / 10)
        customer["loyalty_points"] += points_earned
        customer["total_spent"] += purchase_amount
        
        return points_earned
    return 0

def find_customer_by_id(customer_id):
    """Find a customer by ID"""
    return next((c for c in customers if c["id"] == customer_id), None)

def find_customer_by_name(name):
    """Find customers by name (partial match)"""
    name_lower = name.lower()
    return [c for c in customers if name_lower in c["name"].lower()]

# ================================================
# SALES PROCESSING FUNCTIONS
# ================================================

def process_sale():
    """Process a new sale transaction"""
    global current_sale_id
    
    print_header("PROCESS NEW SALE")
    
    # Step 1: Customer selection
    print("Step 1: Select Customer")
    print("-" * 40)
    print("1. Existing Customer")
    print("2. New Customer")
    print("3. Guest (No Customer)")
    
    customer_choice = get_valid_input("\nSelect option (1-3): ", "int")
    customer = None
    
    if customer_choice == 1:
        # Existing customer
        view_customers()
        if customers:
            cust_id = get_valid_input("\nEnter Customer ID: ", "int")
            customer = find_customer_by_id(cust_id)
            if customer:
                print(f"Customer: {customer['name']}")
            else:
                print("❌ Customer not found!")
                return
    elif customer_choice == 2:
        # New customer
        add_customer()
        customer = customers[-1]  # Get the last added customer
    else:
        # Guest
        print("Processing as Guest Sale")
    
    # Step 2: Shopping cart
    print("\nStep 2: Add Items to Cart")
    print("-" * 40)
    
    cart = []
    while True:
        view_products("name")
        
        print("\nCart Options:")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. View Cart")
        print("4. Checkout")
        
        choice = get_valid_input("\nSelect option (1-4): ", "int")
        
        if choice == 1:
            # Add item
            product_id = get_valid_input("Enter Product ID to add: ", "int")
            product = next((p for p in products if p["id"] == product_id), None)
            
            if not product:
                print("❌ Product not found!")
                continue
            
            if product["stock"] <= 0:
                print(f"❌ {product['name']} is out of stock!")
                continue
            
            quantity = get_valid_input(f"Enter quantity (max {product['stock']}): ", "positive_int")
            
            if quantity > product["stock"]:
                print(f"❌ Only {product['stock']} available!")
                continue
            
            # Check if item already in cart
            existing_item = next((item for item in cart if item["product_id"] == product_id), None)
            
            if existing_item:
                existing_item["quantity"] += quantity
            else:
                cart.append({
                    "product_id": product_id,
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": quantity
                })
            
            print(f"✅ Added {quantity} x {product['name']} to cart")
            
        elif choice == 2:
            # Remove item
            if not cart:
                print("❌ Cart is empty!")
                continue
            
            print("\nCurrent Cart:")
            for i, item in enumerate(cart, 1):
                print(f"{i}. {item['name']} x{item['quantity']} = "
                      f"{format_currency(item['price'] * item['quantity'])}")
            
            try:
                item_num = int(input("\nEnter item number to remove: "))
                if 1 <= item_num <= len(cart):
                    removed = cart.pop(item_num - 1)
                    print(f"✅ Removed {removed['name']} from cart")
                else:
                    print("❌ Invalid item number!")
            except:
                print("❌ Invalid input!")
                
        elif choice == 3:
            # View cart
            print("\n🛒 Current Shopping Cart:")
            print("-" * 40)
            
            if not cart:
                print("Cart is empty!")
                continue
            
            for item in cart:
                item_total = item["price"] * item["quantity"]
                print(f"• {item['name']} x{item['quantity']} @ {format_currency(item['price'])} "
                      f"= {format_currency(item_total)}")
            
            subtotal = sum(item["price"] * item["quantity"] for item in cart)
            print("-" * 40)
            print(f"Subtotal: {format_currency(subtotal)}")
            
        elif choice == 4:
            # Checkout
            if not cart:
                print("❌ Cannot checkout with empty cart!")
                continue
            break
    
    # Step 3: Calculate totals
    print("\nStep 3: Checkout")
    print("-" * 40)
    
    # Calculate subtotal
    subtotal = sum(item["price"] * item["quantity"] for item in cart)
    
    # Apply discount
    discount = 0
    if subtotal > 100:
        discount = subtotal * 0.10  # 10% discount
        discount_type = "10% (Over $100)"
    elif subtotal > 50:
        discount = subtotal * 0.05  # 5% discount
        discount_type = "5% (Over $50)"
    else:
        discount_type = "None"
    
    discounted_total = subtotal - discount
    
    # Calculate tax
    tax = discounted_total * tax_rate
    
    # Final total
    total = discounted_total + tax
    
    # Display invoice
    print("\n" + "=" * 60)
    print("INVOICE".center(60))
    print("=" * 60)
    print(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Sale ID: {current_sale_id + 1}")
    
    if customer:
        print(f"Customer: {customer['name']} (ID: {customer['id']})")
    else:
        print("Customer: Guest")
    
    print("-" * 60)
    
    for item in cart:
        item_total = item["price"] * item["quantity"]
        print(f"{item['name']:20} x{item['quantity']:<3} @ {format_currency(item['price']):<8} "
              f"= {format_currency(item_total)}")
    
    print("-" * 60)
    print(f"{'Subtotal:':30} {format_currency(subtotal):>20}")
    print(f"{'Discount (' + discount_type + '):':30} {format_currency(-discount):>20}")
    print(f"{'Tax (8.5%):':30} {format_currency(tax):>20}")
    print("=" * 60)
    print(f"{'TOTAL:':30} {format_currency(total):>20}")
    print("=" * 60)
    
    # Step 4: Payment
    print("\nStep 4: Payment")
    print("-" * 40)
    
    payment_methods = ["Cash", "Credit Card", "Debit Card", "Digital Wallet"]
    print("Payment Methods:")
    for i, method in enumerate(payment_methods, 1):
        print(f"{i}. {method}")
    
    pm_choice = get_valid_input("\nSelect payment method (1-4): ", "int")
    
    if 1 <= pm_choice <= 4:
        payment_method = payment_methods[pm_choice - 1]
    else:
        payment_method = "Cash"
    
    # Step 5: Confirm sale
    confirm = input("\nConfirm sale? (yes/no): ").lower()
    
    if confirm != "yes":
        print("❌ Sale cancelled!")
        return
    
    # Process the sale
    current_sale_id += 1
    sale_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Update inventory
    for cart_item in cart:
        product = next(p for p in products if p["id"] == cart_item["product_id"])
        product["stock"] -= cart_item["quantity"]
    
    # Update loyalty points if customer exists
    points_earned = 0
    if customer:
        points_earned = calculate_loyalty_points(customer["id"], total)
    
    # Create sale record
    sale_record = {
        "sale_id": current_sale_id,
        "customer_id": customer["id"] if customer else 0,
        "date": sale_date,
        "items": cart.copy(),
        "subtotal": round(subtotal, 2),
        "discount": round(discount, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
        "payment_method": payment_method
    }
    
    sales_history.append(sale_record)
    
    # Generate receipt
    print("\n" + "=" * 60)
    print("RECEIPT".center(60))
    print("=" * 60)
    print(f"Thank you for your purchase!")
    print(f"Sale ID: {current_sale_id}")
    print(f"Date: {sale_date}")
    
    if customer:
        print(f"Customer: {customer['name']}")
        print(f"Loyalty Points Earned: {points_earned}")
        print(f"Total Points: {customer['loyalty_points']}")
    
    print(f"Payment Method: {payment_method}")
    print(f"Amount Paid: {format_currency(total)}")
    print("=" * 60)
    print("Please come again!")
    print("=" * 60)

# ================================================
# REPORT FUNCTIONS
# ================================================

def sales_report():
    """Generate sales report"""
    print_header("SALES REPORT")
    
    if not sales_history:
        print("No sales recorded yet!")
        return
    
    # Sort sales by date (newest first)
    sorted_sales = sorted(sales_history, key=lambda x: x["date"], reverse=True)
    
    # Overall statistics
    total_sales = len(sales_history)
    total_revenue = sum(s["total"] for s in sales_history)
    total_items = sum(len(s["items"]) for s in sales_history)
    
    # Calculate today's sales
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_sales = [s for s in sales_history if s["date"] == today]
    today_revenue = sum(s["total"] for s in today_sales)
    
    print(f"📅 Report Date: {today}")
    print("-" * 60)
    
    print(f"Overall Statistics:")
    print(f"   • Total Sales: {total_sales}")
    print(f"   • Total Revenue: {format_currency(total_revenue)}")
    print(f"   • Total Items Sold: {total_items}")
    print(f"   • Average Sale: {format_currency(total_revenue/total_sales if total_sales > 0 else 0)}")
    
    print(f"\nToday's Statistics ({today}):")
    print(f"   • Sales Today: {len(today_sales)}")
    print(f"   • Revenue Today: {format_currency(today_revenue)}")
    
    # Top selling products
    print("\n🏆 Top Selling Products:")
    print("-" * 40)
    
    # Count product sales
    product_sales = {}
    for sale in sales_history:
        for item in sale["items"]:
            product_id = item["product_id"]
            quantity = item["quantity"]
            product_sales[product_id] = product_sales.get(product_id, 0) + quantity
    
    # Sort by quantity sold
    top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for product_id, quantity in top_products:
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            revenue = quantity * product["price"]
            print(f"   • {product['name']}: {quantity} sold, Revenue: {format_currency(revenue)}")
    
    # Recent sales
    print(f"\n🔄 Recent Sales (Last 5):")
    print("-" * 60)
    print(f"{'Date':<12} {'Sale ID':<8} {'Customer':<15} {'Total':<12} {'Items':<8}")
    print("-" * 60)
    
    for sale in sorted_sales[:5]:
        customer = find_customer_by_id(sale["customer_id"])
        customer_name = customer["name"] if customer else "Guest"
        
        print(f"{sale['date']:<12} {sale['sale_id']:<8} {customer_name[:15]:<15} "
              f"{format_currency(sale['total']):<12} {len(sale['items']):<8}")

def inventory_report():
    """Generate inventory status report"""
    print_header("INVENTORY STATUS REPORT")
    
    if not products:
        print("No products in inventory!")
        return
    
    # Sort by stock level (lowest first)
    sorted_products = sorted(products, key=lambda x: x["stock"])
    
    # Statistics
    total_items = sum(p["stock"] for p in products)
    total_value = sum(p["price"] * p["stock"] for p in products)
    low_stock_count = len([p for p in products if p["stock"] < p["min_stock"]])
    
    print(f"📊 Inventory Summary:")
    print(f"   • Total Products: {len(products)}")
    print(f"   • Total Items in Stock: {total_items}")
    print(f"   • Total Inventory Value: {format_currency(total_value)}")
    print(f"   • Low Stock Items: {low_stock_count}")
    print("-" * 60)
    
    # Low stock warning
    if low_stock_count > 0:
        print("⚠️  LOW STOCK ITEMS NEEDING RESTOCK:")
        print(f"{'ID':<5} {'Product':<15} {'Current':<10} {'Minimum':<10} {'Status':<15}")
        print("-" * 60)
        
        for product in sorted_products:
            if product["stock"] < product["min_stock"]:
                needed = product["min_stock"] - product["stock"]
                status = f"Need {needed}"
                print(f"{product['id']:<5} {product['name']:<15} {product['stock']:<10} "
                      f"{product['min_stock']:<10} {status:<15}")
        
        print("-" * 60)
    
    # All products
    print(f"\n📋 COMPLETE INVENTORY LIST:")
    print(f"{'ID':<5} {'Product':<15} {'Category':<10} {'Price':<10} {'Stock':<10} {'Value':<12}")
    print("-" * 65)
    
    for product in sorted_products:
        value = product["price"] * product["stock"]
        status = "⚠️ " if product["stock"] < product["min_stock"] else "✅ "
        
        print(f"{product['id']:<5} {status + product['name']:<15} {product['category']:<10} "
              f"{format_currency(product['price']):<10} {product['stock']:<10} "
              f"{format_currency(value):<12}")
    
    print("-" * 65)

def customer_report():
    """Generate customer spending report"""
    print_header("CUSTOMER SPENDING REPORT")
    
    if not customers:
        print("No customers registered!")
        return
    
    # Sort customers by total spent (highest first)
    sorted_customers = sorted(customers, key=lambda x: x["total_spent"], reverse=True)
    
    print(f"{'ID':<6} {'Name':<20} {'Join Date':<12} {'Spent':<12} {'Visits':<8} {'Points':<10}")
    print("-" * 75)
    
    for customer in sorted_customers:
        # Count customer's purchases
        visits = len([s for s in sales_history if s["customer_id"] == customer["id"]])
        
        print(f"{customer['id']:<6} {customer['name']:<20} {customer['join_date']:<12} "
              f"{format_currency(customer['total_spent']):<12} {visits:<8} "
              f"{customer['loyalty_points']:<10}")
    
    print("-" * 75)
    
    # Statistics
    total_customers = len(customers)
    total_spent = sum(c["total_spent"] for c in customers)
    avg_spent = total_spent / total_customers if total_customers > 0 else 0
    
    print(f"\n📊 Customer Statistics:")
    print(f"   • Total Customers: {total_customers}")
    print(f"   • Total Revenue from Customers: {format_currency(total_spent)}")
    print(f"   • Average per Customer: {format_currency(avg_spent)}")
    
    # Top customers
    print(f"\n🏆 Top 3 Customers:")
    for i, customer in enumerate(sorted_customers[:3], 1):
        print(f"   {i}. {customer['name']} - {format_currency(customer['total_spent'])}")

# ================================================
# SEARCH FUNCTIONS
# ================================================

def search_products():
    """Search products by name or category"""
    print_header("SEARCH PRODUCTS")
    
    print("Search Options:")
    print("1. By Name")
    print("2. By Category")
    print("3. By Price Range")
    
    choice = get_valid_input("\nSelect search type (1-3): ", "int")
    
    if choice == 1:
        # Search by name
        search_term = input("Enter product name (or part of name): ").lower()
        results = [p for p in products if search_term in p["name"].lower()]
        
        if not results:
            print(f"No products found matching '{search_term}'")
            return
        
        print(f"\nFound {len(results)} product(s):")
        print("-" * 60)
        for product in results:
            print(f"ID: {product['id']}, Name: {product['name']}, "
                  f"Category: {product['category']}, Price: {format_currency(product['price'])}, "
                  f"Stock: {product['stock']}")
    
    elif choice == 2:
        # Search by category
        print("\nAvailable Categories:")
        categories = sorted(set(p["category"] for p in products))
        for cat in categories:
            print(f"  • {cat}")
        
        search_cat = input("\nEnter category: ").lower()
        results = [p for p in products if p["category"].lower() == search_cat]
        
        if not results:
            print(f"No products found in category '{search_cat}'")
            return
        
        print(f"\nFound {len(results)} product(s) in '{search_cat}':")
        print("-" * 60)
        for product in results:
            print(f"ID: {product['id']}, Name: {product['name']}, "
                  f"Price: {format_currency(product['price'])}, Stock: {product['stock']}")
    
    elif choice == 3:
        # Search by price range
        min_price = get_valid_input("Enter minimum price: $", "float")
        max_price = get_valid_input("Enter maximum price: $", "float")
        
        results = [p for p in products if min_price <= p["price"] <= max_price]
        
        if not results:
            print(f"No products found between ${min_price:.2f} and ${max_price:.2f}")
            return
        
        print(f"\nFound {len(results)} product(s) in price range:")
        print("-" * 60)
        for product in sorted(results, key=lambda x: x["price"]):
            print(f"ID: {product['id']}, Name: {product['name']}, "
                  f"Price: {format_currency(product['price'])}, Stock: {product['stock']}")

def search_customers():
    """Search customers by name or phone"""
    print_header("SEARCH CUSTOMERS")
    
    print("Search Options:")
    print("1. By Name")
    print("2. By Phone")
    print("3. By Loyalty Points")
    
    choice = get_valid_input("\nSelect search type (1-3): ", "int")
    
    if choice == 1:
        # Search by name
        search_term = input("Enter customer name (or part of name): ").lower()
        results = [c for c in customers if search_term in c["name"].lower()]
        
        if not results:
            print(f"No customers found matching '{search_term}'")
            return
        
        print(f"\nFound {len(results)} customer(s):")
        print("-" * 60)
        for customer in results:
            print(f"ID: {customer['id']}, Name: {customer['name']}, "
                  f"Phone: {customer['phone']}, Email: {customer['email']}, "
                  f"Points: {customer['loyalty_points']}")
    
    elif choice == 2:
        # Search by phone
        search_phone = input("Enter phone number (or part): ").lower()
        results = [c for c in customers if search_phone in c["phone"]]
        
        if not results:
            print(f"No customers found with phone containing '{search_phone}'")
            return
        
        print(f"\nFound {len(results)} customer(s):")
        print("-" * 60)
        for customer in results:
            print(f"ID: {customer['id']}, Name: {customer['name']}, "
                  f"Phone: {customer['phone']}, Email: {customer['email']}")
    
    elif choice == 3:
        # Search by loyalty points
        min_points = get_valid_input("Enter minimum loyalty points: ", "int")
        
        results = [c for c in customers if c["loyalty_points"] >= min_points]
        
        if not results:
            print(f"No customers found with {min_points}+ loyalty points")
            return
        
        # Sort by points (highest first)
        results.sort(key=lambda x: x["loyalty_points"], reverse=True)
        
        print(f"\nFound {len(results)} customer(s) with {min_points}+ points:")
        print("-" * 60)
        for customer in results:
            print(f"ID: {customer['id']}, Name: {customer['name']}, "
                  f"Points: {customer['loyalty_points']}, "
                  f"Total Spent: {format_currency(customer['total_spent'])}")

def search_sales():
    """Search sales by date or amount"""
    print_header("SEARCH SALES")
    
    if not sales_history:
        print("No sales recorded yet!")
        return
    
    print("Search Options:")
    print("1. By Date")
    print("2. By Amount Range")
    print("3. By Customer")
    
    choice = get_valid_input("\nSelect search type (1-3): ", "int")
    
    if choice == 1:
        # Search by date
        search_date = input("Enter date (YYYY-MM-DD): ")
        results = [s for s in sales_history if s["date"] == search_date]
        
        if not results:
            print(f"No sales found on {search_date}")
            return
        
        print(f"\nFound {len(results)} sale(s) on {search_date}:")
        print("-" * 60)
        for sale in results:
            customer = find_customer_by_id(sale["customer_id"])
            customer_name = customer["name"] if customer else "Guest"
            
            print(f"Sale ID: {sale['sale_id']}, Customer: {customer_name}, "
                  f"Total: {format_currency(sale['total'])}, Items: {len(sale['items'])}")
    
    elif choice == 2:
        # Search by amount range
        min_amount = get_valid_input("Enter minimum amount: $", "float")
        max_amount = get_valid_input("Enter maximum amount: $", "float")
        
        results = [s for s in sales_history if min_amount <= s["total"] <= max_amount]
        
        if not results:
            print(f"No sales found between ${min_amount:.2f} and ${max_amount:.2f}")
            return
        
        # Sort by amount (highest first)
        results.sort(key=lambda x: x["total"], reverse=True)
        
        print(f"\nFound {len(results)} sale(s) in amount range:")
        print("-" * 60)
        for sale in results:
            customer = find_customer_by_id(sale["customer_id"])
            customer_name = customer["name"] if customer else "Guest"
            
            print(f"Date: {sale['date']}, Sale ID: {sale['sale_id']}, "
                  f"Customer: {customer_name}, Total: {format_currency(sale['total'])}")
    
    elif choice == 3:
        # Search by customer
        cust_name = input("Enter customer name (or part): ").lower()
        
        # Find matching customers
        matching_customers = [c for c in customers if cust_name in c["name"].lower()]
        
        if not matching_customers:
            print(f"No customers found matching '{cust_name}'")
            return
        
        # Get all sales for these customers
        results = []
        for customer in matching_customers:
            customer_sales = [s for s in sales_history if s["customer_id"] == customer["id"]]
            results.extend(customer_sales)
        
        if not results:
            print(f"No sales found for customers matching '{cust_name}'")
            return
        
        print(f"\nFound {len(results)} sale(s) for matching customers:")
        print("-" * 60)
        for sale in results:
            customer = find_customer_by_id(sale["customer_id"])
            print(f"Date: {sale['date']}, Sale ID: {sale['sale_id']}, "
                  f"Customer: {customer['name']}, Total: {format_currency(sale['total'])}")

# ================================================
# MAIN MENU FUNCTIONS
# ================================================

def product_management_menu():
    """Product management menu"""
    while True:
        print_header("PRODUCT MANAGEMENT")
        
        print("1. 📦 Add New Product")
        print("2. 👁️  View All Products")
        print("3. 🔄 Update Product")
        print("4. ❌ Delete Product")
        print("5. ⚠️  Check Low Stock")
        print("6. 📊 View Inventory Report")
        print("7. ↩️  Back to Main Menu")
        
        choice = get_valid_input("\nEnter your choice (1-7): ", "int")
        
        if choice == 1:
            add_product()
            input("\nPress Enter to continue...")
        elif choice == 2:
            view_products()
            input("\nPress Enter to continue...")
        elif choice == 3:
            update_product()
            input("\nPress Enter to continue...")
        elif choice == 4:
            delete_product()
            input("\nPress Enter to continue...")
        elif choice == 5:
            check_low_stock()
            input("\nPress Enter to continue...")
        elif choice == 6:
            inventory_report()
            input("\nPress Enter to continue...")
        elif choice == 7:
            break
        else:
            print("❌ Invalid choice!")

def customer_management_menu():
    """Customer management menu"""
    while True:
        print_header("CUSTOMER MANAGEMENT")
        
        print("1. 👤 Add New Customer")
        print("2. 👥 View All Customers")
        print("3. 📊 View Customer Report")
        print("4. 🔍 Search Customers")
        print("5. ↩️  Back to Main Menu")
        
        choice = get_valid_input("\nEnter your choice (1-5): ", "int")
        
        if choice == 1:
            add_customer()
            input("\nPress Enter to continue...")
        elif choice == 2:
            view_customers()
            input("\nPress Enter to continue...")
        elif choice == 3:
            customer_report()
            input("\nPress Enter to continue...")
        elif choice == 4:
            search_customers()
            input("\nPress Enter to continue...")
        elif choice == 5:
            break
        else:
            print("❌ Invalid choice!")

def reports_menu():
    """Reports menu"""
    while True:
        print_header("REPORTS SYSTEM")
        
        print("1. 💰 Sales Report")
        print("2. 📦 Inventory Report")
        print("3. 👥 Customer Report")
        print("4. ↩️  Back to Main Menu")
        
        choice = get_valid_input("\nEnter your choice (1-4): ", "int")
        
        if choice == 1:
            sales_report()
            input("\nPress Enter to continue...")
        elif choice == 2:
            inventory_report()
            input("\nPress Enter to continue...")
        elif choice == 3:
            customer_report()
            input("\nPress Enter to continue...")
        elif choice == 4:
            break
        else:
            print("❌ Invalid choice!")

def search_menu():
    """Search system menu"""
    while True:
        print_header("SEARCH SYSTEM")
        
        print("1. 🔍 Search Products")
        print("2. 🔍 Search Customers")
        print("3. 🔍 Search Sales")
        print("4. ↩️  Back to Main Menu")
        
        choice = get_valid_input("\nEnter your choice (1-4): ", "int")
        
        if choice == 1:
            search_products()
            input("\nPress Enter to continue...")
        elif choice == 2:
            search_customers()
            input("\nPress Enter to continue...")
        elif choice == 3:
            search_sales()
            input("\nPress Enter to continue...")
        elif choice == 4:
            break
        else:
            print("❌ Invalid choice!")

def save_data():
    """Save all data to files (simulated)"""
    print("\n💾 Saving data...")
    print("✅ Data saved successfully!")
    print("   Note: In a real system, this would save to files/database")

# ================================================
# MAIN PROGRAM
# ================================================

def main():
    """Main program function"""
    print("\n" + "=" * 60)
    print("SUPERMARKET MANAGEMENT SYSTEM".center(60))
    print("Version 2.0".center(60))
    print("=" * 60)
    print("Initializing system...")
    
    # Display startup statistics
    print(f"\n System Status:")
    print(f"   • Products in inventory: {len(products)}")
    print(f"   • Registered customers: {len(customers)}")
    print(f"   • Sales recorded: {len(sales_history)}")
    print(f"   • Current sale ID: {current_sale_id}")
    
    input("\nPress Enter to start the system...")
    
    while True:
        print_header("MAIN MENU")
        
        print("1. 📦 Product Management")
        print("2. 👥 Customer Management")
        print("3. 💰 Process Sale")
        print("4. 📊 View Reports")
        print("5. 🔍 Search System")
        print("6. ❌ Exit System")
        
        choice = get_valid_input("\nEnter your choice (1-6): ", "int")
        
        if choice == 1:
            product_management_menu()
        elif choice == 2:
            customer_management_menu()
        elif choice == 3:
            process_sale()
            input("\nPress Enter to continue...")
        elif choice == 4:
            reports_menu()
        elif choice == 5:
            search_menu()
        elif choice == 6:
            # Exit system
            confirm = input("\nAre you sure you want to exit? (yes/no): ").lower()
            if confirm == "yes":
                save_data()
                print_header("GOODBYE")
                print("Thank you for using Supermarket Management System!")
                print("\nDeveloped by: Python Learner")
                print("Version: 2.0")
                print("=" * 60)
                break
        else:
            print("❌ Invalid choice!")

# ================================================
# RUN THE PROGRAM
# ================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user!")
        save_data()
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please restart the program.")
    finally:
        print("\nProgram ended.")

