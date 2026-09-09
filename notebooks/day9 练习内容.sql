with first_order as (
    select c.customer_unique_id,
           min(date(o.order_purchase_timestamp)) as first_order_date
    from customers c join orders o
    on c.customer_id=o.customer_id
    where o.order_status='delivered'
    group  by c.customer_unique_id
),
day1_users as(
    select customer_unique_id,
           first_order_date from first_order
            where first_order_date between '2017-01-01'and '2017-01-31'

)
select
    d.first_order_date,
    count(distinct d.customer_unique_id) as new_uers,
    count(distinct case when o2.order_id is not null then d.customer_unique_id end) as retained,
    round(count(distinct case when o2.order_id is not null then d.customer_unique_id end)*100.0/
          count(distinct d.customer_unique_id),2)
as retention_rate
from day1_users d
    left join customers c
         on c.customer_unique_id=d.customer_unique_id
    left join orders o2
         on c.customer_id=o2.customer_id
         and date(o2.order_purchase_timestamp)=
             date_add(d.first_order_date,interval 1 day)
         and o2.order_status='delivered'
group by d.first_order_date
order by d.first_order_date;

with funnel as (
    select
        count(distinct case when order_purchase_timestamp is not null then order_id end) as step_1,
        count(distinct case when order_approved_at is not null then order_id end) as step_2,
        count(distinct case when order_delivered_carrier_date is not null then order_id end) as step_3,
        count(distinct case when order_delivered_customer_date is not null then order_id end) as step_4
    from orders
)
select '下单' as step_order,step_1 as users,100.0 as conv_rate from funnel
union all
select '支付确认' as step_confirm,step_2,round(step_2*100/step_1,2) from funnel
union all
select '交给物流' as step_transform,step_3,round(step_3*100/step_2,2) from funnel
union all
select '送达客户' as step_arrive,step_4,round(step_4*100/step_3,2) from funnel
