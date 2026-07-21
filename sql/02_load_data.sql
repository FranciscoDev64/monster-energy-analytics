/*
===========================================================
Monster Energy Analytics Portfolio Project
Load Cleaned CSV Files into PostgreSQL
===========================================================

Before running this script:

1. Update each COPY file path to match your local project.
2. Run 01_create_tables.sql first.

Load Order:
1. dim_customers
2. dim_products
3. fact_sales
4. fact_inventory
5. fact_returns

===========================================================
*/

/*
===========================================================
Step 1 - Customer Load
===========================================================
*/
COPY dim_customers (
    customer_id,
    customer_name,
    customer_type,
    channel,
    city,
    state,
    region
)

FROM '/Users/frankie/workspace/Monster_Energy_Analytics/data/cleaned/customers_clean.csv'
DELIMITER ','
CSV HEADER;

/*
===========================================================
Step 2 - Products
===========================================================
*/

COPY dim_products (
    product_id,
    sku,
    brand,
    category,
    product_name,
    flavor,
    package_size,
    units_per_case,
    case_cost,
    case_price,
    active
)
FROM '/Users/frankie/workspace/Monster_Energy_Analytics/data/cleaned/products_clean.csv'
DELIMITER ','
CSV HEADER;

/*
===========================================================
Step 3 - Sales
===========================================================
*/
COPY fact_sales (
    invoice_id,
    invoice_date,
    customer_id,
    product_id,
    warehouse,
    sales_rep,
    quantity_cases,
    case_price,
    discount_pct,
    revenue
)
FROM '/Users/frankie/workspace/Monster_Energy_Analytics/data/cleaned/invoices_clean.csv'
DELIMITER ','
CSV HEADER;

/*
===========================================================
Step 4 - Inventory
===========================================================
*/
COPY fact_inventory (
    inventory_id,
    warehouse,
    product_id,
    inventory_cases,
    reorder_level,
    last_updated
)
FROM '/Users/frankie/workspace/Monster_Energy_Analytics/data/cleaned/inventory_clean.csv'
DELIMITER ','
CSV HEADER;

/*
===========================================================
Step 5 - Returns
===========================================================
*/
COPY fact_returns (
    return_id,
    invoice_id,
    return_date,
    product_id,
    customer_id,
    return_quantity,
    return_reason
)
FROM '/Users/frankie/workspace/Monster_Energy_Analytics/data/cleaned/returns_clean.csv'
DELIMITER ','
CSV HEADER;

/*
===========================================================
Step 6 - Verification
===========================================================
*/
SELECT 'dim_customers' AS table_name, COUNT(*) AS rows FROM dim_customers
UNION ALL
SELECT 'dim_products', COUNT(*) FROM dim_products
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM fact_sales
UNION ALL
SELECT 'fact_inventory', COUNT(*) FROM fact_inventory
UNION ALL
SELECT 'fact_returns', COUNT(*) FROM fact_returns;