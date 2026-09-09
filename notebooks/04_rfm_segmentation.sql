-- RFM 用户分层
SELECT
    customer_unique_id,
    DATEDIFF(MAX(o.order_purchase_timestamp), MIN(o.order_purchase_timestamp)) AS recency_days,
    COUNT(DISTINCT o.order_id) AS frequency,
    ROUND(SUM(i.price), 2) AS monetary,
    CASE
        WHEN COUNT(DISTINCT o.order_id) >= 5 AND SUM(i.price) >= 1000 THEN 'high_value'
        WHEN COUNT(DISTINCT o.order_id) >= 2 THEN 'medium_value'
        ELSE 'low_value'
    END AS segment
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items i ON o.order_id = i.order_id
WHERE o.order_status = 'delivered'
GROUP BY customer_unique_id
ORDER BY monetary DESC;