select c.customer_unique_id,
           datediff(
               (select max(order_purchase_timestamp) from orders
               where order_status='delivered'),max(o.order_purchase_timestamp)
           ) as recency,
           count(distinct o.order_id) as frequency,
           round(sum(i.price),2) as monetary
    from orders o join customers c on c.customer_id=o.customer_id
        left join order_items i
    on i.order_id=o.order_id
    where o.order_status='delivered'
    group by c.customer_unique_id







