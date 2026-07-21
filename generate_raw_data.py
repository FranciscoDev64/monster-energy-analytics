# ==========================================================
# Monster Energy Distribution Analytics Project
# Raw Data Generator
# Creates Customers and Products datasets
# ==========================================================


# -------------------------
# Imports
# -------------------------

import pandas as pd
import random
from pathlib import Path
from datetime import datetime, timedelta


# Make results reproducible so the same random data is generated every time
random.seed(42)

# Find the project folder
PROJECT_PATH = Path(__file__).parent

# Create data/raw folder
RAW_DATA_PATH = PROJECT_PATH / "data" / "raw"

RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)


print("Creating Monster Energy raw data files...")


# ==========================================================
# CUSTOMERS DATA
# ==========================================================

print("Generating customers...")


# Realistic customer master profiles

customer_profiles = [

    # National Retail
    ("Walmart", "Retail", "Bentonville", "AR", "South"),
    ("Target", "Retail", "Minneapolis", "MN", "Midwest"),
    ("Costco", "Retail", "Issaquah", "WA", "West"),
    ("Kroger", "Grocery", "Cincinnati", "OH", "Midwest"),
    ("Albertsons", "Grocery", "Boise", "ID", "West"),
    ("Safeway", "Grocery", "Pleasanton", "CA", "West"),
    ("CVS Pharmacy", "Retail", "Woonsocket", "RI", "Northeast"),
    ("Walgreens", "Retail", "Deerfield", "IL", "Midwest"),


    # Convenience
    ("7-Eleven", "Convenience", "Irving", "TX", "South"),
    ("Circle K", "Convenience", "Tempe", "AZ", "West"),
    ("Speedway", "Convenience", "Enon", "OH", "Midwest"),
    ("Wawa", "Convenience", "Media", "PA", "Northeast"),
    ("Sheetz", "Convenience", "Altoona", "PA", "Northeast"),
    ("Casey's General Store", "Convenience", "Ankeny", "IA", "Midwest"),


    # Distributors
    ("Reyes Beverage Group", "Distributor", "Los Angeles", "CA", "West"),
    ("Core-Mark", "Distributor", "South San Francisco", "CA", "West"),
    ("UNFI", "Distributor", "Providence", "RI", "Northeast"),
    ("KeHE", "Distributor", "Naperville", "IL", "Midwest"),


    # Regional accounts
    ("Pacific Beverage Distribution", "Distributor", "San Diego", "CA", "West"),
    ("Southern Convenience Network", "Distributor", "Houston", "TX", "South"),
    ("Midwest Beverage Partners", "Distributor", "Chicago", "IL", "Midwest"),
    ("Mountain Retail Alliance", "Retail", "Denver", "CO", "Mountain")
]


customers = []


for customer_id in range(1, 501):

    profile = random.choice(customer_profiles)

    customers.append({
        "customer_id": customer_id,
        "customer_name": profile[0],
        "customer_type": profile[1],
        "channel": profile[1],
        "city": profile[2],
        "state": profile[3],
        "region": profile[4]
    })


# -------------------------
# Insert data quality issues
# -------------------------


# Missing customer names
customers[25]["customer_name"] = None
customers[150]["customer_name"] = None


# Incorrect region spelling
customers[75]["region"] = "Wesst"
customers[220]["region"] = "Northeest"


# Duplicate customer ID
customers[300]["customer_id"] = customers[299]["customer_id"]


# Incorrect state assignment
customers[180]["state"] = "TX"


customers_df = pd.DataFrame(customers)


customers_df.to_csv(
    RAW_DATA_PATH / "customers.csv",
    index=False
)


print("customers.csv created")


# ==========================================================
# PRODUCTS DATA
# ==========================================================


print("Generating products...")


products_catalog = [

    # brand, category, flavor, package_size, units_per_case

    ("Monster Energy", "Energy Drink", "Original", "16 oz Can", 24),
    ("Monster Energy", "Energy Drink", "Zero Sugar", "16 oz Can", 24),
    ("Monster Energy", "Energy Drink", "Lo-Carb", "16 oz Can", 24),
    ("Monster Energy", "Energy Drink", "Import", "18.6 oz Can", 12),

    ("Monster Ultra", "Ultra", "Ultra White", "16 oz Can", 24),
    ("Monster Ultra", "Ultra", "Ultra Blue", "16 oz Can", 24),
    ("Monster Ultra", "Ultra", "Ultra Red", "16 oz Can", 24),
    ("Monster Ultra", "Ultra", "Ultra Paradise", "16 oz Can", 24),
    ("Monster Ultra", "Ultra", "Ultra Sunrise", "16 oz Can", 24),
    ("Monster Ultra", "Ultra", "Ultra Violet", "16 oz Can", 24),
    ("Monster Ultra", "Ultra", "Ultra Gold", "16 oz Can", 24),
    ("Monster Ultra", "Ultra", "Ultra Watermelon", "16 oz Can", 24),
    ("Monster Ultra", "Ultra", "Ultra Peachy Keen", "16 oz Can", 24),
    ("Monster Ultra", "Ultra", "Ultra Fiesta Mango", "16 oz Can", 24),
    ("Monster Ultra", "Ultra", "Ultra Strawberry Dreams", "16 oz Can", 24),
    ("Monster Ultra", "Ultra", "Ultra Fantasy Ruby Red", "16 oz Can", 24),

    ("Juice Monster", "Juice", "Mango Loco", "16 oz Can", 24),
    ("Juice Monster", "Juice", "Pipeline Punch", "16 oz Can", 24),
    ("Juice Monster", "Juice", "Pacific Punch", "16 oz Can", 24),
    ("Juice Monster", "Juice", "Aussie Style Lemonade", "16 oz Can", 24),
    ("Juice Monster", "Juice", "Papillon", "16 oz Can", 24),
    ("Juice Monster", "Juice", "Rio Punch", "16 oz Can", 24),
    ("Juice Monster", "Juice", "Khaotic", "16 oz Can", 24),

    ("Java Monster", "Coffee Energy", "Mean Bean", "15 oz Can", 12),
    ("Java Monster", "Coffee Energy", "Loca Moca", "15 oz Can", 12),
    ("Java Monster", "Coffee Energy", "Irish Crème", "15 oz Can", 12),
    ("Java Monster", "Coffee Energy", "French Vanilla", "15 oz Can", 12),
    ("Java Monster", "Coffee Energy", "Salted Caramel", "15 oz Can", 12),

    ("Reign", "Performance Energy", "Orange Dreamsicle", "16 oz Can", 24),
    ("Reign", "Performance Energy", "Rainbow Sherbet", "16 oz Can", 24),
    ("Reign", "Performance Energy", "White Gummy Bear", "16 oz Can", 24),
    ("Reign", "Performance Energy", "Melon Mania", "16 oz Can", 24),
    ("Reign", "Performance Energy", "Cherry Limeade", "16 oz Can", 24),
    ("Reign", "Performance Energy", "Sour Gummy Worm", "16 oz Can", 24),

]


products = []

for product_id, product in enumerate(products_catalog, start=1001):

    brand, category, flavor, package_size, units_per_case = product

    # Build readable SKU
    sku = (
        brand.upper().replace(" ", "")[:4]
        + "-"
        + "".join(word[:3].upper() for word in flavor.split())
    )

    # Pricing by category
    if category == "Energy Drink":
        case_cost = round(random.uniform(22, 27), 2)
        case_price = round(random.uniform(31, 36), 2)

    elif category == "Ultra":
        case_cost = round(random.uniform(23, 28), 2)
        case_price = round(random.uniform(33, 38), 2)

    elif category == "Juice":
        case_cost = round(random.uniform(24, 30), 2)
        case_price = round(random.uniform(35, 41), 2)

    elif category == "Coffee Energy":
        case_cost = round(random.uniform(20, 26), 2)
        case_price = round(random.uniform(30, 36), 2)

    else:
        case_cost = round(random.uniform(24, 29), 2)
        case_price = round(random.uniform(35, 40), 2)

    products.append({
        "product_id": product_id,
        "sku": sku,
        "brand": brand,
        "category": category,
        "product_name": f"{brand} {flavor}",
        "flavor": flavor,
        "package_size": package_size,
        "units_per_case": units_per_case,
        "case_cost": case_cost,
        "case_price": case_price,
        "active": True
    })


# -------------------------
# Insert data quality issues
# -------------------------

# Missing flavor
products[5]["flavor"] = None

# Product typo
products[10]["product_name"] = "Monstor Energy Ultra White"

# Duplicate product ID
products[20]["product_id"] = products[19]["product_id"]

# Negative price
products[25]["case_price"] = -products[25]["case_price"]


products_df = pd.DataFrame(products)


products_df.to_csv(
    RAW_DATA_PATH / "products.csv",
    index=False
)


print("products.csv created")

# ==========================================================
# INVOICE DATA
# ==========================================================

print("Generating invoices...")

# Read previously generated datasets
customers_df = pd.read_csv(RAW_DATA_PATH / "customers.csv")
products_df = pd.read_csv(RAW_DATA_PATH / "products.csv")

# Distribution Centers
warehouses = [
    "Los Angeles DC",
    "Dallas DC",
    "Chicago DC",
    "Atlanta DC",
    "Phoenix DC"
]

sales_reps = [
    "Alex Martinez",
    "Jordan Kim",
    "Taylor Johnson",
    "Morgan Lee",
    "Chris Ramirez",
    "Ashley Nguyen",
    "Ryan Thompson",
    "Casey Davis"
]

category_weights = {
    "Energy Drink": 40,
    "Ultra": 30,
    "Juice": 15,
    "Coffee Energy": 10,
    "Performance Energy": 5
}

weighted_products = []

for _, row in products_df.iterrows():
    weight = category_weights.get(row["category"], 1)
    weighted_products.extend([row] * weight)

invoice_rows = []

start_date = datetime(2025, 1, 1)

invoice_rows = []

start_date = datetime(2025, 1, 1)

for invoice_id in range(500001, 550001):

    # Pick customer
    customer = customers_df.sample(1).iloc[0]
    customer_type = customer["customer_type"]


    # Determine order size based on customer type
    if customer_type == "Distributor":
        quantity_cases = random.randint(300, 800)
    elif customer_type in ["Retail", "Grocery"]:
        quantity_cases = random.randint(100, 500)
    elif customer_type == "Convenience":
        quantity_cases = random.randint(20, 80)
    else:
        quantity_cases = random.randint(50, 200)

    # Pick product using weighted pool
    product = random.choice(weighted_products)

    # Invoice date
    invoice_date = start_date + timedelta(
        days=random.randint(0, 364)
    )

    # Discount logic
    discount_chance = random.random()

    if discount_chance < 0.75:
        discount_pct = 0
    elif discount_chance < 0.90:
        discount_pct = 0.05
    elif discount_chance < 0.98:
        discount_pct = 0.10
    else:
        discount_pct = 0.15

    # Revenue calculation
    revenue = round(
        quantity_cases *
        product["case_price"] *
        (1 - discount_pct),
        2
    )


    invoice_rows.append({
        "invoice_id": invoice_id,
        "invoice_date": invoice_date.strftime("%Y-%m-%d"),
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "warehouse": random.choice(warehouses),
        "sales_rep": random.choice(sales_reps),
        "quantity_cases": quantity_cases,
        "case_price": product["case_price"],
        "discount_pct": discount_pct,
        "revenue": revenue
    })

invoices_df = pd.DataFrame(invoice_rows)

# ==========================================================
# Insert invoice data quality issues
# ==========================================================

print("Adding invoice data issues...")

# Duplicate invoice IDs
invoices_df.loc[100, "invoice_id"] = invoices_df.loc[99, "invoice_id"]

# Missing customer IDs
invoices_df.loc[500, "customer_id"] = None
invoices_df.loc[750, "customer_id"] = None

# Negative quantities
invoices_df.loc[1000, "quantity_cases"] = -250
invoices_df.loc[2000, "quantity_cases"] = -50

# Incorrect revenue
invoices_df.loc[3000, "revenue"] = 999999

# Invalid date
invoices_df.loc[4000, "invoice_date"] = "2025-15-99"

invoices_df.to_csv(
    RAW_DATA_PATH / "invoices.csv",
    index=False
)

print("invoices.csv created")

# ==========================================================
# INVENTORY DATA
# ==========================================================

print("Generating inventory...")

warehouses = [
    "Los Angeles DC",
    "Dallas DC",
    "Chicago DC",
    "Atlanta DC",
    "Phoenix DC"
]

inventory_rows = []
inventory_id = 1

for warehouse in warehouses:
    for _, product in products_df.iterrows():
        inventory_cases = random.randint(100, 5000)
        reorder_level = random.randint(100, 1000)

        inventory_rows.append({
            "inventory_id": inventory_id,
            "warehouse": warehouse,
            "product_id": product["product_id"],
            "inventory_cases": inventory_cases,
            "reorder_level": reorder_level,
            "last_updated": "2025-07-01"
        })

        inventory_id += 1

inventory_df = pd.DataFrame(inventory_rows)

# -------------------------
# Insert inventory issues
# -------------------------

print("Adding inventory issues...")

# Negative inventory
inventory_df.loc[10, "inventory_cases"] = -250

# Missing reorder level
inventory_df.loc[50, "reorder_level"] = None

# Stock inconsistency
inventory_df.loc[100, "inventory_cases"] = 500
inventory_df.loc[100, "reorder_level"] = 1000

inventory_df.to_csv(
    RAW_DATA_PATH / "inventory.csv",
    index=False
)

print("inventory.csv created")

# ==========================================================
# RETURNS DATA
# ==========================================================

print("Generating returns...")

return_reasons = [
    "Damaged Product",
    "Customer Complaint",
    "Wrong Shipment",
    "Expired Product",
    "Quality Issue"
]

returns = []

return_id = 1

# Approximately 2% of invoices become returns

sample_invoices = invoices_df.sample(
    n=int(len(invoices_df) * 0.02),
    random_state=42
)

for _, invoice in sample_invoices.iterrows():
    return_quantity = random.randint(
        1,
        max(1, int(invoice["quantity_cases"] * 0.10))
    )

    return_date = datetime.strptime(
        invoice["invoice_date"],
        "%Y-%m-%d"
    ) + timedelta(
        days=random.randint(5, 45)
    )

    returns.append({
        "return_id": return_id,
        "invoice_id": invoice["invoice_id"],
        "return_date": return_date.strftime("%Y-%m-%d"),
        "product_id": invoice["product_id"],
        "customer_id": invoice["customer_id"],
        "return_quantity": return_quantity,
        "return_reason": random.choice(return_reasons)
    })

    return_id += 1

returns_df = pd.DataFrame(returns)

# -------------------------
# Insert return issues
# -------------------------

print("Adding return issues...")

# Nonexistent invoice
returns_df.loc[10, "invoice_id"] = 999999

# Negative return quantity
returns_df.loc[20, "return_quantity"] = -25

# Missing reason
returns_df.loc[30, "return_reason"] = None

returns_df.to_csv(
    RAW_DATA_PATH / "returns.csv",
    index=False
)

print("returns.csv created")

print("\nCustomer and product datasets generated successfully!")