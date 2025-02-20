import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
db = mysql.connector.connect(user='root', password='Saikat@123.bca', host='localhost', database='Ecommerce')
cus = db.cursor()

cus.execute("SELECT * FROM customer")
#data = cus.fetchall()
customer_data = pd.DataFrame(cus.fetchall(), columns=[desc[0] for desc in
cus.description])
print(customer_data.head())
print(customer_data['city'].value_counts())

#plt.pie(customer_data['city'].value_counts())
#plt.show()

cus.execute("SELECT * FROM product")
#data1 = cus.fetchall()
product_data = pd.DataFrame(cus.fetchall(), columns=[desc[0] for desc in
cus.description])
#print(product_data.head())


cus.execute("SELECT * FROM order_details")
#data2 = cus.fetchall()
order_data = pd.DataFrame(cus.fetchall(), columns=[desc[0] for desc in
cus.description])

#print(order_data.head())





# Identify the total number of customers city wise.
df = customer_data['city'].value_counts()
df.plot(kind = 'bar', color='red')
plt.show()


# Identify the most frequent customers based on their order history
df1 = order_data['customer_id'].value_counts().head(10)
df1.plot(kind = 'bar', color = 'blue')
#plt.show()


# Determine the total number of products available by category.
product_category_counts = product_data['category'].value_counts()
print(product_category_counts)

plt.figure(figsize=(10, 5))
plt.bar(product_category_counts.index, product_category_counts.values, color='red')
plt.xlabel("Category")
plt.ylabel("Number of Products")
plt.title("Products Available by Category")
plt.xticks(rotation=45)
plt.show()


# Analyze the distribution of products across sub-categories
subcategory_counts = product_data['sub_category'].value_counts()
print(subcategory_counts)

plt.figure(figsize=(10, 5))
plt.bar(subcategory_counts.index, subcategory_counts.values, color='orange')
plt.xlabel("Sub-Category")
plt.ylabel("Number of Products")
plt.title("Product Distribution by Sub-Category")
plt.xticks(rotation=45)
plt.show()


# Identify products with low stock levels.
low_stock_products = product_data[product_data['stock'] < product_data['stock'].quantile(0.1)]
print(low_stock_products)
low_stock_products['stock'].plot(kind='bar')
plt.title('Low Stock Products')
plt.xlabel('Product ID')
plt.ylabel('Stock Quantity')
plt.show()


# Calculate the average, maximum, and minimum selling prices for products.


# Calculate the top 10 orders product wise.
top_orders = order_data.groupby('product_id')['quantity'].sum().sort_values(ascending=False).head(10)
print(top_orders)
top_orders.plot(kind='bar')
plt.title('Top 10 Ordered Products')
plt.xlabel('Product ID')
plt.ylabel('Total Quantity Ordered')
plt.show()


# Order status distribution
order_status_counts = order_data['order_status'].value_counts()
print(order_status_counts)
order_status_counts.plot(kind='bar')
plt.title('Order Status Distribution')
plt.xlabel('Order Status')
plt.ylabel('Count')
plt.show()


# Identify the most popular products based on order quantity.
popular_products = order_data.groupby('product_id')['quantity'].sum().sort_values(ascending=False)
print(popular_products.head(10))
plt.figure(figsize=(8, 6))
popular_products.head(10).plot(kind='barh', color='skyblue')
plt.title('Top 10 Most Popular Products Based on Order Quantity')
plt.xlabel('Product ID')
plt.ylabel('Total Quantity Ordered')
plt.xticks(rotation=45)
plt.show()


# Total revenue product-wise
order_data['total_revenue'] = order_data['quantity'] * order_data['total_price']
product_revenue = order_data.groupby('product_id')['total_revenue'].sum()
print(product_revenue)
plt.figure(figsize=(10, 5))
product_revenue.sort_values(ascending=False).head(10).plot(kind='bar', color='skyblue')
plt.title('Top 10 Revenue Generating Products')
plt.xlabel('Product ID')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.show()


# Calculate total revenue product category wise percentage
category_revenue = order_data.merge(product_data, on='product_id').groupby('category')['total_revenue'].sum()
print(category_revenue)
category_revenue.plot(kind='pie',autopct='%1.1f%%')
plt.title('Total Revenue by Category')
plt.xlabel('Category')
plt.ylabel('Revenue')
plt.show()


# Most profitable products
product_data['profit'] = product_data['selling_price'] - product_data['original_price']
df_sorted = product_data.sort_values(by='profit', ascending=False)
plt.figure(figsize=(10, 5))
plt.bar(df_sorted['product_name'], df_sorted['profit'], color='blue', edgecolor='black')
plt.xlabel('Product Name')
plt.ylabel('Profit')
plt.title('Most Profitable Products')
plt.xticks(rotation=45)
plt.show()


# Most and least ordered products
product_orders = order_data.merge(product_data, on='product_id').groupby("product_name")["quantity"].sum()
highest_ordered_product = product_orders.idxmax()
lowest_ordered_product = product_orders.idxmin()
highest_quantity = product_orders.max()
lowest_quantity = product_orders.min()
top_bottom_products = {
    highest_ordered_product: highest_quantity,
    lowest_ordered_product: lowest_quantity
}
plt.figure(figsize=(8, 5))
plt.bar(top_bottom_products.keys(), top_bottom_products.values(), color=['green', 'red'])
plt.xlabel("Product Name")
plt.ylabel("Order Quantity")
plt.title("Highest & Lowest Ordered Products")
plt.xticks(rotation=15)
plt.show()


# Identify customers with the highest and lowest order quantities
customer_order_quantities = order_data.groupby('customer_id')['quantity'].sum()
highest_order_customer = customer_order_quantities.idxmax()
highest_order_quantity = customer_order_quantities.max()
highest_customer_name = customer_data[customer_data['customer_id'] == highest_order_customer]['name'].values[0]
lowest_order_customer = customer_order_quantities.idxmin()
lowest_order_quantity = customer_order_quantities.min()
lowest_customer_name = customer_data[customer_data['customer_id'] == lowest_order_customer]['name'].values[0]
print(f'Highest Order Quantity: {highest_order_quantity} by {highest_customer_name}')
print(f'Lowest Order Quantity: {lowest_order_quantity} by {lowest_customer_name}')
plt.figure(figsize=(6, 4))
plt.bar([highest_customer_name, lowest_customer_name], [highest_order_quantity, lowest_order_quantity], color=['green', 'red'])
plt.title('Customers with Highest and Lowest Order Quantities')
plt.xlabel('Customer Name')
plt.ylabel('Total Order Quantity')
plt.show()


# Determine the most preferred payment modes
payment_mode_counts = order_data['payment_mode'].value_counts()
print(payment_mode_counts)
plt.figure(figsize=(8, 6))
payment_mode_counts.plot(kind='bar', color='skyblue')
plt.title('Most Preferred Payment Modes')
plt.xlabel('Payment Mode')
plt.ylabel('Number of Orders')
plt.show()


# Month wise total sales
order_data['order_date'] = pd.to_datetime(order_data['order_date'])
monthly_sales = order_data.groupby(order_data['order_date'].dt.to_period('M'))['total_price'].sum()
print(monthly_sales)
plt.figure(figsize=(10, 6))
monthly_sales.plot(kind='bar', color='lightcoral')
plt.title('Month-wise Total Sales')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.show()


# Month and year wise total sales 
order_data['order_date'] = pd.to_datetime(order_data['order_date'])
monthly_yearly_sales = order_data.groupby(order_data['order_date'].dt.to_period('M'))['total_price'].sum()
print(monthly_yearly_sales)
plt.figure(figsize=(12, 6))
monthly_yearly_sales.plot(kind='bar', color='orange')
plt.title('Month and Year-wise Total Sales')
plt.xlabel('Month-Year')
plt.ylabel('Total Sales')
plt.xticks(rotation=90)
plt.show()


# Identify peak order date
order_data['order_date'] = pd.to_datetime(order_data['order_date'])
daily_order_counts = order_data.groupby(order_data['order_date'].dt.date)['order_id'].count()
peak_order_date = daily_order_counts.idxmax()
peak_order_count = daily_order_counts.max()
print(f'Peak Order Date: {peak_order_date} with {peak_order_count} orders')
plt.figure(figsize=(10, 6))
plt.plot(daily_order_counts.index, daily_order_counts.values, marker='o', color='b')
plt.title('Daily Order Counts with Peak Order Date')
plt.xlabel('Date')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.axvline(x=peak_order_date, color='r', linestyle='--', label=f'Peak: {peak_order_date}')
plt.legend()
plt.show()


# Explore the distribution of customers across different cities.
customer_city_counts = customer_data['city'].value_counts()
print(customer_city_counts)
plt.figure(figsize=(10, 6))
customer_city_counts.plot(kind='bar', color='skyblue')
plt.title('Distribution of Customers Across Cities')
plt.xlabel('City')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45)
plt.show()



# Identify the best selling products
best_selling_products = order_data.groupby('product_id')['quantity'].sum().reset_index()
best_selling_products = best_selling_products.merge(product_data, on='product_id')
best_selling_products = best_selling_products.sort_values(by='quantity', ascending=False)
print(best_selling_products[['product_name', 'quantity']].head(10))
plt.figure(figsize=(10, 6))
plt.bar(best_selling_products['product_name'].head(10), best_selling_products['quantity'].head(10), color='skyblue')
plt.title('Top 10 Best-Selling Products')
plt.xlabel('Product Name')
plt.ylabel('Total Quantity Sold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# Identify top 10 slow-moving products based on low sales.
slow_moving_products = order_data.groupby('product_id')['quantity'].sum().reset_index()
slow_moving_products = slow_moving_products.merge(product_data, on='product_id')
slow_moving_products = slow_moving_products.sort_values(by='quantity', ascending=True)
print(slow_moving_products[['product_name', 'quantity']].head(10))
plt.figure(figsize=(10, 6))
plt.bar(slow_moving_products['product_name'].head(10), slow_moving_products['quantity'].head(10), color='lightcoral')
plt.title('Top 10 Slow-Moving Products (Low Sales)')
plt.xlabel('Product Name')
plt.ylabel('Total Quantity Sold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()



# Display successful and pending payments order counts
payment_status_counts = order_data['order_status'].value_counts()
print(payment_status_counts)
plt.figure(figsize=(8, 6))
payment_status_counts.plot(kind='bar', color=['green', 'orange'])
plt.title('Counts of Successful and Pending Payments')
plt.xlabel('Payment Status')
plt.ylabel('Number of Orders')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()




db.close()
