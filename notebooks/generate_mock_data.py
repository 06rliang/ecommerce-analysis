import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)
output_dir = 'data/raw'
os.makedirs(output_dir, exist_ok=True)

N_CUSTOMERS = 3000
N_PRODUCTS = 500
N_ORDERS = 5000
N_SELLERS = 100

brazilian_states = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'GO', 'DF', 'CE', 'PE', 'ES', 'MT', 'PA', 'PB']
brazilian_cities = {
    'SP': ['Sao Paulo', 'Campinas', 'Guarulhos', 'Santos', 'Ribeirao Preto'],
    'RJ': ['Rio de Janeiro', 'Niteroi', 'Duque de Caxias', 'Nova Iguacu'],
    'MG': ['Belo Horizonte', 'Uberlandia', 'Contagem', 'Juiz de Fora'],
    'RS': ['Porto Alegre', 'Caxias do Sul', 'Pelotas', 'Canoas'],
    'PR': ['Curitiba', 'Londrina', 'Maringa', 'Ponta Grossa'],
    'SC': ['Florianopolis', 'Joinville', 'Blumenau', 'Chapeco'],
    'BA': ['Salvador', 'Feira de Santana', 'Vitoria da Conquista'],
    'GO': ['Goiania', 'Aparecida de Goiania', 'Anapolis'],
    'DF': ['Brasilia'],
    'CE': ['Fortaleza', 'Caucaia', 'Juazeiro do Norte'],
    'PE': ['Recife', 'Jaboatao', 'Olinda'],
    'ES': ['Vitoria', 'Vila Velha', 'Serra'],
    'MT': ['Cuiaba', 'Varzea Grande', 'Rondonopolis'],
    'PA': ['Belem', 'Ananindeua', 'Santarem'],
    'PB': ['Joao Pessoa', 'Campina Grande', 'Santa Rita']
}

product_categories = [
    'electronics', 'furniture', 'home_appliances', 'sports_leisure',
    'computers', 'toys', 'cool_stuff', 'health_beauty', 'fashion_bags',
    'watches_gifts', 'auto', 'pet_shop', 'office_furniture',
    'construction_tools', 'garden_tools', 'audio', 'books',
    'musical_instruments', 'food', 'drinks'
]

payment_types = ['credit_card', 'boleto', 'voucher', 'debit_card']
order_statuses = ['delivered', 'shipped', 'canceled', 'processing', 'invoiced']

print("Generating customers...")
customers = []
unique_ids = [f'c{i:05d}' for i in range(N_CUSTOMERS)]
for i in range(N_CUSTOMERS):
    state = np.random.choice(brazilian_states)
    city = np.random.choice(brazilian_cities[state])
    zip_code = f'{np.random.randint(10000, 99999)}-{np.random.randint(100, 999)}'
    customers.append({
        'customer_id': f'cust{i:05d}',
        'customer_unique_id': unique_ids[np.random.randint(0, N_CUSTOMERS)],
        'customer_zip_code_prefix': zip_code,
        'customer_city': city,
        'customer_state': state
    })
customers_df = pd.DataFrame(customers)
customers_df.to_csv(f'{output_dir}/olist_customers_dataset.csv', index=False)
print(f"  {len(customers_df)} customers saved")

print("Generating products...")
products = []
for i in range(N_PRODUCTS):
    products.append({
        'product_id': f'prod{i:04d}',
        'product_category_name': np.random.choice(product_categories),
        'product_name_lenght': np.random.randint(30, 80),
        'product_description_lenght': np.random.randint(100, 2000),
        'product_photos_qty': np.random.randint(1, 12),
        'product_weight_g': np.random.randint(100, 30000),
        'product_length_cm': np.random.randint(10, 80),
        'product_height_cm': np.random.randint(5, 50),
        'product_width_cm': np.random.randint(10, 60)
    })
products_df = pd.DataFrame(products)
products_df.to_csv(f'{output_dir}/olist_products_dataset.csv', index=False)
print(f"  {len(products_df)} products saved")

print("Generating sellers...")
sellers = []
for i in range(N_SELLERS):
    state = np.random.choice(brazilian_states)
    city = np.random.choice(brazilian_cities[state])
    sellers.append({
        'seller_id': f'sell{i:04d}',
        'seller_zip_code_prefix': f'{np.random.randint(10000, 99999)}-{np.random.randint(100, 999)}',
        'seller_city': city,
        'seller_state': state
    })
sellers_df = pd.DataFrame(sellers)
sellers_df.to_csv(f'{output_dir}/olist_sellers_dataset.csv', index=False)
print(f"  {len(sellers_df)} sellers saved")

print("Generating orders...")
orders = []
order_items = []
payments = []
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = (end_date - start_date).days

for i in range(N_ORDERS):
    order_id = f'ord{i:06d}'
    customer_id = f'cust{np.random.randint(0, N_CUSTOMERS):05d}'
    status = np.random.choice(order_statuses, p=[0.85, 0.08, 0.02, 0.03, 0.02])

    purchase_time = start_date + timedelta(days=np.random.randint(0, date_range),
                                           hours=np.random.randint(0, 24),
                                           minutes=np.random.randint(0, 60))
    approved_time = purchase_time + timedelta(hours=np.random.randint(1, 24))
    carrier_time = approved_time + timedelta(days=np.random.randint(1, 5))
    delivery_time = carrier_time + timedelta(days=np.random.randint(2, 15))
    estimated_time = carrier_time + timedelta(days=np.random.randint(5, 20))

    if status in ['canceled', 'processing']:
        carrier_time = None
        delivery_time = None
        estimated_time = None

    orders.append({
        'order_id': order_id,
        'customer_id': customer_id,
        'order_status': status,
        'order_purchase_timestamp': purchase_time.strftime('%Y-%m-%d %H:%M:%S'),
        'order_approved_at': approved_time.strftime('%Y-%m-%d %H:%M:%S') if approved_time else None,
        'order_delivered_carrier_date': carrier_time.strftime('%Y-%m-%d %H:%M:%S') if carrier_time else None,
        'order_delivered_customer_date': delivery_time.strftime('%Y-%m-%d %H:%M:%S') if delivery_time else None,
        'order_estimated_delivery_date': estimated_time.strftime('%Y-%m-%d %H:%M:%S') if estimated_time else None
    })

    n_items = np.random.randint(1, 4)
    for j in range(n_items):
        product = products[np.random.randint(0, N_PRODUCTS)]
        seller = sellers[np.random.randint(0, N_SELLERS)]
        price = round(np.random.uniform(15, 3000), 2)
        freight = round(np.random.uniform(5, 100), 2)

        order_items.append({
            'order_id': order_id,
            'order_item_id': j + 1,
            'product_id': product['product_id'],
            'seller_id': seller['seller_id'],
            'shipping_limit_date': (carrier_time or approved_time).strftime('%Y-%m-%d %H:%M:%S'),
            'price': price,
            'freight_value': freight
        })

    total_value = sum(item['price'] + item['freight_value'] for item in order_items[-n_items:])
    n_payments = np.random.randint(1, 3)
    for p in range(n_payments):
        payments.append({
            'order_id': order_id,
            'payment_sequential': p + 1,
            'payment_type': np.random.choice(payment_types, p=[0.7, 0.2, 0.05, 0.05]),
            'payment_installments': np.random.randint(1, 12),
            'payment_value': round(total_value / n_payments, 2)
        })

orders_df = pd.DataFrame(orders)
orders_df.to_csv(f'{output_dir}/olist_orders_dataset.csv', index=False)
print(f"  {len(orders_df)} orders saved")

order_items_df = pd.DataFrame(order_items)
order_items_df.to_csv(f'{output_dir}/olist_order_items_dataset.csv', index=False)
print(f"  {len(order_items_df)} order items saved")

payments_df = pd.DataFrame(payments)
payments_df.to_csv(f'{output_dir}/olist_order_payments_dataset.csv', index=False)
print(f"  {len(payments_df)} payments saved")

category_translation = pd.DataFrame({
    'product_category_name': product_categories,
    'product_category_name_english': [c.replace('_', ' ').title() for c in product_categories]
})
category_translation.to_csv(f'{output_dir}/product_category_name_translation.csv', index=False)
print(f"  {len(category_translation)} category translations saved")

print("\n=== Data generation complete! ===")
print(f"Files saved to: {output_dir}/")
print("\nFiles:")
for f in os.listdir(output_dir):
    size = os.path.getsize(f'{output_dir}/{f}')
    print(f"  {f} ({size/1024:.0f} KB)")
