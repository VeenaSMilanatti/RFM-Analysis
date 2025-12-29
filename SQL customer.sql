SELECT
    customer_id,
    MAX(order_date) AS last_purchase_date,
    COUNT(DISTINCT order_id) AS frequency,
    SUM(revenue) AS monetary
FROM fact_sales
GROUP BY customer_id
LIMIT 10;
SELECT
    customer_id,
    last_purchase_date,
    frequency,
    monetary,
    recency_score,
    frequency_score,
    monetary_score,
    (recency_score + frequency_score + monetary_score) AS rfm_score
FROM rfm_scores;
CREATE OR REPLACE VIEW customer_rfm_base AS
SELECT
    customer_id,
    DATEDIFF(CURDATE(), MAX(order_date)) AS recency,
    COUNT(DISTINCT order_id) AS frequency,
    SUM(revenue) AS monetary
FROM fact_sales
GROUP BY customer_id;
SHOW TABLES;
SHOW FULL TABLES WHERE Table_type = 'VIEW';
SELECT * FROM customer_rfm_base LIMIT 5;






