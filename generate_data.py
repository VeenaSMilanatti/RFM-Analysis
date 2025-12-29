import pandas as pd
import numpy as np
from faker import Faker
from datetime import timedelta

fake = Faker()
np.random.seed(42)

NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 500
NUM_TRANSACTIONS = 200000
START_DATE = pd.to_datetime("2022-01-01")
END_DATE = pd.to_datetime("2024-12-31")

# Generate customers
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    join_date = fake.date_between(start_date='-3y', end_date='-1y')
    customers.append([i, fake.country(), join_date])
dim_customer = pd.DataFrame(customers, columns=["customer_id", "country", "join_date"])
dim_customer.to_csv("dim_customer.csv", index=False)

# Generate products
products = []
for i in range(1, NUM_PRODUCTS + 1):
    products.append([f"P{i:04}", fake.word().capitalize()])
dim_product = pd.DataFrame(products, columns=["product_id", "product_name"])
dim_product.to_csv("dim_product.csv", index=False)

# Generate transactions
transactions = []
date_range = (END_DATE - START_DATE).days

customer_ids = dim_customer["customer_id"].values
product_ids = dim_product["product_id"].values

# For weighting top 200 customers as whales:
weights = np.where(customer_ids <= 200, 0.002, 0.998 / (NUM_CUSTOMERS - 200))
weights = weights / weights.sum()  # Normalize to sum 1

for _ in range(NUM_TRANSACTIONS):
    order_date = START_DATE + timedelta(days=np.random.randint(0, date_range))
    quantity = np.random.randint(1, 6)
    customer_id = np.random.choice(customer_ids, p=weights)
    product_id = np.random.choice(product_ids)
    unit_price = round(np.random.uniform(5, 500), 2)
    revenue = round(quantity * unit_price, 2)
    transactions.append([fake.uuid4(), order_date.strftime("%Y-%m-%d"), customer_id, product_id, quantity, revenue])

fact_sales = pd.DataFrame(transactions, columns=["order_id", "order_date", "customer_id", "product_id", "quantity", "revenue"])
fact_sales.to_csv("fact_sales.csv", index=False)

print("✅ Synthetic enterprise data generated successfully")
