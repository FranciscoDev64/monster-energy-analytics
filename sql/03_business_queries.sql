/*
===========================================================
Monster Energy Analytics Portfolio Project

Business Analysis Queries

Purpose:
Answer business questions using the PostgreSQL data warehouse.

Sections:
1. Sales Performance
2. Customer Analysis
3. Product Analysis
4. Inventory Analysis
5. Returns Analysis

===========================================================
*/

-- 1. Total Revenue

SELECT
    SUM(revenue) AS total_revenue
FROM fact_sales;

-- 2. Revenue by Region
SELECT
    c.region,
    SUM(s.revenue) AS total_revenue
FROM fact_sales s
JOIN dim_customers c
    ON s.customer_id = c.customer_id
GROUP BY c.region
ORDER BY total_revenue DESC;

-- 3. Revenue by Channel
SELECT
    c.channel,
    SUM(s.revenue) AS total_revenue
FROM fact_sales s
JOIN dim_customers c
    ON s.customer_id = c.customer_id
GROUP BY c.channel
ORDER BY total_revenue DESC;

/*
===========================================================
Executive KPI Dashboard
===========================================================
*/

-- KPI 1
-- Business Question:
-- How much total revenue did the company generate?

SELECT
    ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_sales;

-- KPI 2
-- How many cases were sold?

SELECT
    SUM(quantity_cases) AS total_cases_sold
FROM fact_sales;

-- KPI 3
-- Average revenue per invoice

SELECT
    ROUND(AVG(revenue), 2) AS average_invoice_value
FROM fact_sales;

-- KPI 4
-- Active customers

SELECT
    COUNT(*) AS total_customers
FROM dim_customers
WHERE customer_id <> 0;

SELECT
    COUNT(*) AS total_products
FROM dim_products;

/*
===========================================================
SECTION 3 - PRODUCT PERFORMANCE
===========================================================
*/

-- Product Performance 1
-- Business Question:
-- Which individual products generate the most revenue?

SELECT
    p.product_name,
    p.brand,
    ROUND(SUM(s.revenue), 2) AS total_revenue
FROM fact_sales s
JOIN dim_products p
    ON s.product_id = p.product_id
GROUP BY
    p.product_name,
    p.brand
ORDER BY total_revenue DESC
LIMIT 10;

-- Product Performance 2
-- Business Question:
-- Which brands generate the most revenue?

SELECT
    p.brand,
    ROUND(SUM(s.revenue), 2) AS total_revenue
FROM fact_sales s
JOIN dim_products p
    ON s.product_id = p.product_id
GROUP BY p.brand
ORDER BY total_revenue DESC;

-- Product Performance 3
-- Business Question:
-- Which products sell the highest volume?

SELECT
    p.product_name,
    SUM(s.quantity_cases) AS total_cases_sold
FROM fact_sales s
JOIN dim_products p
    ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_cases_sold DESC;

/*
===========================================================
SECTION 4 - CUSTOMER PERFORMANCE
===========================================================
*/

-- Customer Performance 1
-- Business Question:
-- Which customers generate the most revenue?

SELECT
    c.customer_name,
    c.region,
    c.channel,
    ROUND(SUM(s.revenue), 2) AS total_revenue
FROM fact_sales s
JOIN dim_customers c
    ON s.customer_id = c.customer_id
GROUP BY
    c.customer_name,
    c.region,
    c.channel
ORDER BY total_revenue DESC
LIMIT 10;

-- Customer Performance 2
-- Business Question:
-- Which customers purchase the highest volume?

SELECT
    c.customer_name,
    c.region,
    SUM(s.quantity_cases) AS total_cases
FROM fact_sales s
JOIN dim_customers c
    ON s.customer_id = c.customer_id
GROUP BY
    c.customer_name,
    c.region
ORDER BY total_cases DESC
LIMIT 10;

-- Customer Performance 3
-- Business Question:
-- Which channels generate the most customer revenue?

SELECT
    c.channel,
    ROUND(SUM(s.revenue),2) AS total_revenue
FROM fact_sales s
JOIN dim_customers c
    ON s.customer_id = c.customer_id
GROUP BY c.channel
ORDER BY total_revenue DESC;

/*
===========================================================
SECTION 5 - INVENTORY HEALTH
===========================================================
*/

-- Inventory Health 1
-- Business Question:
-- How much inventory exists by warehouse?

SELECT
    warehouse,
    SUM(inventory_cases) AS total_inventory_cases
FROM fact_inventory
GROUP BY warehouse
ORDER BY total_inventory_cases DESC;

-- Inventory Health 2
-- Business Question:
-- Which products are below their reorder threshold?

SELECT
    p.product_name,
    i.warehouse,
    i.inventory_cases,
    i.reorder_level
FROM fact_inventory i
JOIN dim_products p
    ON i.product_id = p.product_id
WHERE i.inventory_cases < i.reorder_level
ORDER BY 
    i.inventory_cases ASC;

-- Inventory Health 3
-- Business Question:
-- Which products have the most inventory?

SELECT
    p.product_name,
    SUM(i.inventory_cases) AS total_inventory_cases
FROM fact_inventory i
JOIN dim_products p
    ON i.product_id = p.product_id
GROUP BY
    p.product_name
ORDER BY total_inventory_cases DESC;

-- Inventory Health 4
-- Business Question:
-- Compare inventory levels against sales demand.

SELECT
    p.product_name,
    SUM(i.inventory_cases) AS inventory_cases,
    SUM(s.quantity_cases) AS annual_cases_sold
FROM fact_inventory i
JOIN fact_sales s
    ON i.product_id = s.product_id
JOIN dim_products p
    ON i.product_id = p.product_id
GROUP BY
    p.product_name
ORDER BY annual_cases_sold DESC;

/*
===========================================================
SECTION 6 - RETURNS & QUALITY ANALYSIS
===========================================================
*/

-- Returns Analysis 1
-- Business Question:
-- Which products have the highest return quantities?

SELECT
    p.product_name,
    SUM(r.return_quantity) AS total_returned_cases
FROM fact_returns r
JOIN dim_products p
    ON r.product_id = p.product_id
GROUP BY
    p.product_name
ORDER BY total_returned_cases DESC;

-- Returns Analysis 2
-- Business Question:
-- What are the most common return reasons?

SELECT
    return_reason,
    COUNT(*) AS return_count,
    SUM(return_quantity) AS total_returned_cases
FROM fact_returns
GROUP BY return_reason
ORDER BY total_returned_cases DESC;

-- Returns Analysis 3
-- Business Question:
-- Which customers return the most products?

SELECT
    c.customer_name,
    c.region,
    SUM(r.return_quantity) AS returned_cases
FROM fact_returns r
JOIN dim_customers c
    ON r.customer_id = c.customer_id
GROUP BY
    c.customer_name,
    c.region
ORDER BY returned_cases DESC
LIMIT 10;

-- Returns Analysis 4
-- Business Question:
-- What is the overall return rate?

SELECT
    ROUND(
        SUM(r.return_quantity)::numeric /
        SUM(s.quantity_cases)::numeric * 100,
        2
    ) AS return_rate_percentage
FROM fact_returns r
JOIN fact_sales s
    ON r.product_id = s.product_id;

-- Returns Analysis 5
-- Business Question:
-- Which products have the highest return rates?

SELECT
    p.product_name,
    SUM(r.return_quantity) AS returned_cases,
    SUM(s.quantity_cases) AS sold_cases,
    ROUND(
        SUM(r.return_quantity)::numeric /
        SUM(s.quantity_cases)::numeric * 100,
        2
    ) AS return_rate_percentage
FROM fact_returns r
JOIN fact_sales s
    ON r.product_id = s.product_id
JOIN dim_products p
    ON r.product_id = p.product_id
GROUP BY
    p.product_name
ORDER BY return_rate_percentage DESC;