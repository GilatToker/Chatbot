import pandas as pd
import numpy as np

# Set the seed for reproducibility
np.random.seed(0)

# Define order status options
order_statuses = [
    "Processing", "Shipped", "Delivered", "On Hold",
    "Cancelled", "Returned", "Awaiting Payment"
]

# Define additional columns for the orders
order_dates = pd.date_range(start='2023-01-01', periods=1000, freq='D')  # Sequential dates starting from 2023-01-01

# Generate 1000 sample order_ids and order statuses
order_ids = [f"{str(i).zfill(4)}{chr(65 + (i % 26))}" for i in range(1001, 2001)]  # Generate IDs in the format 1001A, 1002B, ..., 2000Z
statuses = np.random.choice(order_statuses, size=1000)  # Randomly pick statuses for each order

# Create a DataFrame
orders_df = pd.DataFrame({
    "order_id": order_ids,
    "order_status": statuses,
    "order_date": order_dates,
})
# Save to CSV file
orders_df.to_csv('Orders.csv', index=False)


