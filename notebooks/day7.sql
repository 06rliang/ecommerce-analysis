with monthly_total_amount as(
    select
        date_format(o.order_purchase_timestamp,'%Y-%m') as month,
        sum(i.price) as sum_monthly_amount
    from orders as o join order_items as i on o.order_id=i.order_id group by month order by month
)
select * from monthly_total_amount where sum_monthly_amount>1000000;

# 第二题
with high_value_customers as(
    select c.customer_unique_id,
           sum(i.price) as total_amount
    from customers c join orders o on
        c.customer_id=o.customer_id
    join order_items i on o.order_id=i.order_id
    where o.order_status='delivered' group by c.customer_unique_id having sum(i.price)>=1000
)
select
    count(distinct o.order_id) as total_orders,
    count(i.order_item_id) as total_items,
    round(avg(i.price),2) as avg_price
from
    high_value_customers h join customers c on h.customer_unique_id=c.customer_unique_id
join orders o on c.customer_id=o.customer_id
join order_items i on o.order_id=i.order_id where o.order_status='delivered';

# 第三题
with monthly_amount_category as (
    select date_format(o.order_purchase_timestamp,'%Y-%m') as month,
           p.product_category_name as category,
           sum(i.price) as revenue
    from orders o
        join order_items i on o.order_id=i.order_id
        join products p on i.product_id=p.product_id
    where o.order_status='delivered'
    group by p.product_category_name,month
    ),
    last_month_amount as (
        select category,
               month,
               revenue,
               lag(revenue,1) over(partition by category order by month) as last_month_revenue
        from monthly_amount_category
)
select month,
       category,
       revenue,
       last_month_revenue,
       round((revenue-last_month_revenue)*100/last_month_revenue,2) as growth_pct
from last_month_amount where last_month_revenue is not null
                         and last_month_revenue>0
                         and (revenue-last_month_revenue)/last_month_revenue>0.5 order by growth_pct desc;

# 第四题
select concat(order_id,'_',orders.order_status,'_',
              date_format(order_purchase_timestamp,'%Y-%m')) from orders limit 20;

# 第五题
with highest_revenue_state as (select
    c.customer_state,
    p.product_category_name,
    sum(i.price) as revenue,
    rank() over(partition by c.customer_state order by sum(i.price) desc) as rk
        from customers c join orders o on c.customer_id=o.customer_id join order_items i on
        i.order_id=o.order_id join products p on
        p.product_id=i.product_id where o.order_status='delivered'
            group by c.customer_state,p.product_category_name
)
select
    customer_state as state,
    revenue,
    product_category_name as category
    from highest_revenue_state
where rk=1

union all

select
    'all' as state,
    revenue,
    category
      from(
    select p.product_category_name as category,
           sum(i.price) as revenue from
    orders o join order_items i on o.order_id=i.order_id
    join products p on p.product_id=i.product_id
    where o.order_status='delivered'
    group by p.product_category_name
    order by revenue desc
    limit 1
    ) national_top
order by state






















