-- Sales Data Preparation Queries
-- These queries assume the raw sales data is loaded into a table called 'raw_sales'

-- 1. Create processed sales table with calculated fields
CREATE TABLE processed_sales AS
SELECT
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    price,
    quantity * price AS total_amount,
    EXTRACT(YEAR FROM order_date) AS order_year,
    EXTRACT(MONTH FROM order_date) AS order_month,
    EXTRACT(DAY FROM order_date) AS order_day,
    CASE
        WHEN EXTRACT(DOW FROM order_date) = 0 THEN 'Sunday'
        WHEN EXTRACT(DOW FROM order_date) = 1 THEN 'Monday'
        WHEN EXTRACT(DOW FROM order_date) = 2 THEN 'Tuesday'
        WHEN EXTRACT(DOW FROM order_date) = 3 THEN 'Wednesday'
        WHEN EXTRACT(DOW FROM order_date) = 4 THEN 'Thursday'
        WHEN EXTRACT(DOW FROM order_date) = 5 THEN 'Friday'
        WHEN EXTRACT(DOW FROM order_date) = 6 THEN 'Saturday'
    END AS order_weekday,
    country,
    region
FROM raw_sales
WHERE order_id IS NOT NULL
  AND customer_id IS NOT NULL
  AND product_id IS NOT NULL
  AND quantity > 0
  AND price > 0;

-- 2. Monthly sales aggregation
CREATE TABLE monthly_sales_summary AS
SELECT
    order_year,
    order_month,
    CONCAT(order_year, '-', LPAD(order_month, 2, '0')) AS period,
    SUM(total_amount) AS monthly_revenue,
    COUNT(DISTINCT order_id) AS order_count,
    COUNT(DISTINCT customer_id) AS unique_customers,
    AVG(total_amount) AS avg_order_value
FROM processed_sales
GROUP BY order_year, order_month
ORDER BY order_year, order_month;

-- 3. Customer metrics calculation
CREATE TABLE customer_metrics AS
SELECT
    customer_id,
    SUM(total_amount) AS total_spent,
    COUNT(DISTINCT order_id) AS order_count,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date,
    AVG(total_amount) AS avg_order_value,
    SUM(total_amount) / COUNT(DISTINCT order_id) AS customer_lifetime_value
FROM processed_sales
GROUP BY customer_id;

-- 4. Product performance analysis
CREATE TABLE product_performance AS
SELECT
    product_id,
    SUM(total_amount) AS total_revenue,
    SUM(quantity) AS total_quantity_sold,
    COUNT(DISTINCT order_id) AS order_count,
    AVG(price) AS avg_price,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM processed_sales
GROUP BY product_id
ORDER BY total_revenue DESC;

-- 5. Geographic sales analysis
CREATE TABLE geographic_sales AS
SELECT
    country,
    region,
    SUM(total_amount) AS total_revenue,
    COUNT(DISTINCT order_id) AS order_count,
    COUNT(DISTINCT customer_id) AS unique_customers,
    AVG(total_amount) AS avg_order_value
FROM processed_sales
GROUP BY country, region
ORDER BY total_revenue DESC;

-- 6. KPI Overview Query
SELECT
    'Total Revenue' AS kpi_name,
    SUM(total_amount) AS value
FROM processed_sales
UNION ALL
SELECT
    'Unique Customers',
    COUNT(DISTINCT customer_id)
FROM processed_sales
UNION ALL
SELECT
    'Total Orders',
    COUNT(DISTINCT order_id)
FROM processed_sales
UNION ALL
SELECT
    'Average Order Value',
    AVG(total_amount)
FROM processed_sales;