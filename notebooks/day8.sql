select distinct c.customer_unique_id,c.customer_state from customers c
where exists (select 1 from orders o join order_items i on
o.order_id=i.order_id join products p
    on i.product_id=p.product_id where
        c.customer_id=o.customer_id and
        p.product_category_name='moveis_decoracao' and
        o.order_status='delivered')
order by c.customer_state
limit 20;

select distinct c.customer_unique_id from customers c
where c.customer_state='SP' and not exists(
    select 1 from orders o join order_items i
             on o.order_id=i.order_id join
        products p on i.product_id=p.product_id
             where c.customer_id=o.customer_id and
                   c.customer_state='electronics' and
                   o.order_status='delivered'
)
limit 20;

select
    date_format(order_purchase_timestamp,'%Y-%m') as month,
    count(*) as order_count,
    round(avg(datediff(order_delivered_customer_date ,order_purchase_timestamp)),1)
as month_avg_delivered_time
from orders
where order_status='delivered' and
      order_purchase_timestamp>='2017-01_01' and
      order_delivered_customer_date<'2018-01-01'
group by month
order by month


