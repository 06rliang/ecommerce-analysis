# 计算各个州平均配送时长
select
    c.customer_state as state,
    count(*) as order_count,
    round(avg(datediff(o.order_delivered_customer_date,o.order_purchase_timestamp)),2) as avg_delivered
from customers c join orders o
on c.customer_id=o.customer_id
where o.order_status='delivered'
and o.order_purchase_timestamp is not null
group by c.customer_state
order by avg_delivered desc




