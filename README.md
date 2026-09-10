# 巴西电商用户行为数据分析

## 1. 项目背景

巴西电商平台 Olist 的真实订单数据（2016-2018），包含 8 张业务表、9.6万+ 订单。目标是通过 SQL + Pandas 分析销售趋势、用户价值和配送效率，发现业务问题并提出可落地的建议。

## 2. 数据集

- **来源**：Kaggle - Brazilian E-Commerce Public Dataset by Olist
- **规模**：93,358 位独立客户、99,000+ 订单、8 张业务表（orders、order_items、customers、products、payments、reviews、sellers、category_translation）
- **时间范围**：2016-09 至 2018-08
- **存储**：MySQL 数据库（通过 SQLAlchemy 导入）

## 3. 分析思路

围绕三个核心问题展开：

1. **销售趋势分析**：月度销售额和订单量趋势如何？高峰在什么时候？
2. **用户价值分析**：用户价值如何分布？RFM 分层结果如何？
3. **订单履约分析**：各州配送时效差异如何？配送是否存在瓶颈？

## 4. 技术栈

| 工具 | 用途 |
|------|------|
| MySQL + SQLAlchemy | 数据存储、多表关联查询 |
| SQL | 窗口函数、聚合、多表 JOIN、CASE WHEN 分层 |
| Python / Pandas | 数据清洗、聚合、RFM 分层、时间序列 |
| Matplotlib | 双轴图、饼图、柱状图可视化 |
| Jupyter Notebook | 分析过程记录 |

## 5. 核心结论

### 结论 1：销售额 2017 年快速增长，11 月达峰值

| 时间 | 订单数 | 销售额（R$） | 客单价（R$） |
|------|--------|-------------|-------------|
| 2017-01 | 750 | 111,798 | 122.45 |
| 2017-06 | 3,135 | 421,923 | 120.93 |
| 2017-11（峰值） | 7,289 | 987,765 | 116.55 |
| 2018-08（最新） | 6,351 | 838,577 | 117.41 |

- 2017 年 1 月到 11 月销售额增长约 **783%**（111,798 → 987,765）
- 2017-11 订单量突增至 7,289 单，推测与 Black Friday 促销有关
- 客单价全年稳定在 R$110-130 区间，波动不大

### 结论 2：RFM 分层显示用户价值分布均匀

对 93,358 位客户进行 RFM 分层（R/F/M 各分 4 档）：

| 用户群体 | 客户数 | 占比 |
|---------|--------|------|
| 重要价值客户 | 12,097 | 12.9% |
| 重要保持客户 | 11,311 | 12.1% |
| 重要发展客户 | 11,503 | 12.3% |
| 重要挽留客户 | 11,678 | 12.5% |
| 重要挽回客户 | 11,401 | 12.2% |
| 新客户 | 11,769 | 12.6% |
| 一般保持客户 | 11,593 | 12.4% |
| 流失客户 | 12,006 | 12.8% |

- 由于数据集 97% 的客户只下过一次单，Frequency 分布高度集中，通过 rank(method='first') 排名后强制分档
- 12.9% 的重要价值客户是运营重点对象
- 12.8% 的流失客户需要召回策略

### 结论 3：各州配送时效差异显著

通过 SQL 关联 customers 和 orders 表，计算各州平均配送天数（下单到送达），并绘制双轴图对比订单量与配送时效。

- 订单量最大的州（SP）配送效率相对较好
- 部分订单量小的州配送时间明显更长，存在物流瓶颈

## 6. 业务建议

1. **VIP 运营**：针对 12.9% 的重要价值客户做专属服务和优先推荐，预计可提升复购率
2. **流失召回**：对 12.8% 的流失客户推送召回优惠券，预期转化率 8-12%
3. **配送优化**：重点改善配送时间较长的州，优化仓库布局和物流路线

## 7. 项目结构

```
ecommerce-analysis/
├── data/
│   └── raw/                         # 原始数据（8 张 CSV）
├── notebooks/
│   ├── 01_data_cleaning.ipynb        # 数据清洗与月度销售趋势
│   ├── 02_data_draw.ipynb            # 月度销售额与订单量可视化
│   ├── 03_avg_delivery_days_draw_fixed.ipynb  # 各州配送时效双轴图
│   └── 04_RFM.ipynb                  # RFM 用户分层分析
├── sql/
│   ├── init_database.py              # MySQL 数据导入脚本
│   └── queries/
│       ├── 03_state_sales.sql         # 各州销售对比
│       └── 04_rfm_segmentation.sql    # RFM 用户分层
├── output/
│   ├── monthly_revenue.png            # 月度销售额与订单量趋势图
│   ├── state_delivery.png            # 各州订单量与配送时效双轴图
│   └── rfm_segments.png              # RFM 用户分层饼图
├── .gitignore
└── README.md
```

## 8. 关键技术实现

### SQL：月度销售趋势
```sql
SELECT
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') AS month,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(i.price) AS total_revenue,
    ROUND(AVG(i.price), 2) AS avg_price
FROM orders o
JOIN order_items i ON o.order_id = i.order_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month;
```

### SQL + Pandas：RFM 分层
```sql
-- 用动态最大日期作为基准，避免 2019 年订单产生负 Recency
SELECT c.customer_unique_id,
    DATEDIFF(
        (SELECT MAX(order_purchase_timestamp) FROM orders WHERE order_status='delivered'),
        MAX(o.order_purchase_timestamp)
    ) AS recency,
    COUNT(DISTINCT o.order_id) AS frequency,
    ROUND(SUM(i.price), 2) AS monetary
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
LEFT JOIN order_items i ON i.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_unique_id;
```

```python
# Frequency 高度集中（97% 为 1），用 rank(method='first') 解决 qcut 同值问题
df['R'] = pd.qcut(df['recency'], 4, labels=[4, 3, 2, 1])
df['F'] = pd.qcut(df['frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
df['M'] = pd.qcut(df['monetary'], 4, labels=[1, 2, 3, 4])
```

### SQL：各州配送时效
```sql
SELECT
    c.customer_state AS state,
    COUNT(*) AS order_count,
    ROUND(AVG(DATEDIFF(o.order_delivered_customer_date,
                       o.order_purchase_timestamp)), 2) AS avg_delivered
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp IS NOT NULL
GROUP BY c.customer_state
ORDER BY avg_delivered DESC;
```
