CREATE TABLE dim_customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_type VARCHAR(50),
    channel VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(2),
    region VARCHAR(50)
);

CREATE TABLE dim_products (
    product_id INT PRIMARY KEY,
    sku VARCHAR(30),
    brand VARCHAR(50),
    category VARCHAR(50),
    product_name VARCHAR(100),
    flavor VARCHAR(50),
    package_size VARCHAR(30),
    units_per_case INT,
    case_cost DECIMAL(10,2),
    case_price DECIMAL(10,2),
    active BOOLEAN
);

CREATE TABLE fact_sales (
    invoice_id INT PRIMARY KEY,
    invoice_date DATE,
    customer_id INT,
    product_id INT,
    warehouse VARCHAR(50),
    sales_rep VARCHAR(100),
    quantity_cases INT,
    case_price DECIMAL(10,2),
    discount_pct DECIMAL(5,2),
    revenue DECIMAL(12,2),

    FOREIGN KEY (customer_id)
        REFERENCES dim_customers(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES dim_products(product_id)
);

CREATE TABLE fact_returns (
    return_id INT PRIMARY KEY,
    invoice_id INT,
    return_date DATE,
    product_id INT,
    customer_id INT,
    return_quantity INT,
    return_reason VARCHAR(100),

    FOREIGN KEY (product_id)
        REFERENCES dim_products(product_id),

    FOREIGN KEY (customer_id)
        REFERENCES dim_customers(customer_id)
);

CREATE TABLE fact_inventory (
    inventory_id INT PRIMARY KEY,
    warehouse VARCHAR(50),
    product_id INT,
    inventory_cases INT,
    reorder_level INT,
    last_updated DATE,

    FOREIGN KEY (product_id)
        REFERENCES dim_products(product_id)
);