# -*- coding: utf-8 -*-
"""
电商数据导入 MySQL 脚本
运行后打开 DataGrip 连接 ecommerce 库即可写 SQL 分析
"""
import os
from sqlalchemy import create_engine, text
import pandas as pd

# ========== 改这里 ==========
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'      # 改成你的 MySQL 密码
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
DB_NAME = 'ecommerce'
# ============================

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, 'data', 'raw')

FILES = [
    ('orders', 'olist_orders_dataset.csv'),
    ('order_items', 'olist_order_items_dataset.csv'),
    ('customers', 'olist_customers_dataset.csv'),
    ('products', 'olist_products_dataset.csv'),
    ('order_payments', 'olist_order_payments_dataset.csv'),
    ('order_reviews', 'olist_order_reviews_dataset.csv'),
    ('sellers', 'olist_sellers_dataset.csv'),
    ('category_translation', 'product_category_name_translation.csv'),
]

def main():
    engine = create_engine(
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/?charset=utf8mb4'
    )

    with engine.connect() as conn:
        conn.execute(text(f'CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4'))
        conn.commit()

    engine.dispose()
    engine = create_engine(
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{DB_NAME}?charset=utf8mb4'
    )

    for table_name, file_name in FILES:
        file_path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(file_path):
            print(f'[skip] file not found: {file_path}')
            continue

        print(f'importing {table_name} ...', end=' ')
        df = pd.read_csv(file_path)
        df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=5000)
        print(f'done  {df.shape[0]} rows, {df.shape[1]} cols')

    print(f'\n=== all done ===')
    print(f'DataGrip: {MYSQL_HOST}:{MYSQL_PORT} / {DB_NAME} / {MYSQL_USER}')

    with engine.connect() as conn:
        tables = conn.execute(text('SHOW TABLES')).fetchall()
        print(f'\ntables:')
        for t in tables:
            count = conn.execute(text(f'SELECT COUNT(*) FROM `{t[0]}`')).scalar()
            print(f'  {t[0]:25s}  {count:>8} rows')

if __name__ == '__main__':
    main()