# 连续N天下单
with order_days as (
    select
        c.customer_unique_id,
        date(o.order_purchase_timestamp) as order_date
    from customers c join orders o
    on o.customer_id = c.customer_id
    where year(o.order_purchase_timestamp)=2018
    and o.order_status='delivered'
),
datediff_lag as (
    select customer_unique_id,
           order_date,
           datediff(order_date,lag(order_date)
           over(partition by customer_unique_id order by order_date))
    as datediff_order_date
    from order_days
)
select
    customer_unique_id,
    count(*) as continue_order_customer,
    min(order_date) as first_order_date,
    max(order_date) as last_order_date
from datediff_lag
where datediff_order_date=1
group by customer_unique_id
having count(*)>=2
order by continue_order_customer;

# 用户消费行为分析
select
    c.customer_unique_id ,
    min(date(o.order_purchase_timestamp)) as first_order_date,
    max(date(o.order_purchase_timestamp)) as last_order_date,
    sum(i.price) as total_order,
    count(*) as count_order,
    round(avg(i.price)/count(distinct o.order_id),2) as avg_order
from orders as o join order_items i
on o.order_id=i.order_id
join customers c
on o.customer_id=c.customer_id
where o.order_status='delivered'
group by c.customer_unique_id
order by sum(i.price) desc
limit 20;

# 各品类销量排名
with category_product_sales as(
    select
        p.product_id,
        p.product_category_name,
        round(sum(i.price),2) as total_sales,
        count(p.product_id) as total_orders,
        rank() over(partition by p.product_category_name
            order by sum(i.price) desc) as sales_rank
    from products p join order_items i on i.product_id=p.product_id
    join orders o on o.order_id=i.order_id
    where o.order_status='delivered'
    group by p.product_id,p.product_category_name
)
select
    product_id,
    product_category_name,
    total_sales,
    total_orders,
    sales_rank
from category_product_sales where sales_rank <=3
order by product_category_name,sales_rank;

# 累计销售额
with month_sales as(
    select
        date_format(o.order_purchase_timestamp,'%Y-%m') as month,
        round(sum(i.price),2) as monthly_revenue
    from orders o join order_items i
    on  o.order_id-i.order_id
    where o.order_status='delivered'
    group by month
)
select
    month,
    monthly_revenue,
    round(sum(monthly_revenue) over(order by month),2) as total_revenue,
    round(monthly_revenue/sum(monthly_revenue) over(order by month)*100,2) as pct_of_cumulative
from month_sales
order by month




