-- 各州销售对比
SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(i.price) AS total_revenue,
    ROUND(AVG(i.price), 2) AS avg_order_value
FROM orders o
JOIN order_items i ON o.order_id = i.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;