import os 
import pandas as pd
import mysql.connector


# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="ecommerce_order_fulfillment"
)

cursor = connection.cursor()

print("Connected to MySQL")

file_path = "data/SAP-DataSet.xlsx"


# --------------------------------------------------
# Load Customer Data - KNA1
# --------------------------------------------------

customer_data = pd.read_excel(file_path, sheet_name="KNA1")

customer_data = customer_data.rename(columns={
    "Customer ID": "customer_id",
    "Customer Name": "customer_name",
    "Country": "country",
    "Region": "region",
    "City": "city",
    "Postal Code": "postal_code",
    "Street Address": "street_address",
    "Phone Number": "phone_number",
    "Email Address": "email_address",
    "Language": "language",
    "Tax Number": "tax_number",
    "Customer Group": "customer_group",
    "Sales Organization": "sales_organization",
    "Distribution Channel": "distribution_channel",
    "Division": "division"
})

customer_query = """
INSERT IGNORE INTO dim_customer
(
    customer_id, customer_name, country, region, city,
    postal_code, street_address, phone_number, email_address,
    language, tax_number, customer_group, sales_organization,
    distribution_channel, division
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for index, row in customer_data.iterrows():
    values = (
        row["customer_id"],
        row["customer_name"],
        row["country"],
        row["region"],
        row["city"],
        row["postal_code"],
        row["street_address"],
        row["phone_number"],
        row["email_address"],
        row["language"],
        row["tax_number"],
        row["customer_group"],
        row["sales_organization"],
        row["distribution_channel"],
        row["division"]
    )

    cursor.execute(customer_query, values)

print("Customer data checked successfully")


# --------------------------------------------------
# Load Order Data - VBAK
# --------------------------------------------------

order_data = pd.read_excel(file_path, sheet_name="VBAK")

order_data = order_data.rename(columns={
    "Sales Document": "order_id",
    "Order Date": "order_date",
    "Customer ID": "customer_id",
    "Order Type": "order_type",
    "Sales Organization": "sales_organization",
    "Distribution Channel": "distribution_channel",
    "Division": "division",
    "Order Status": "order_status"
})

order_query = """
INSERT IGNORE INTO fact_order
(
    order_id, order_date, customer_id, order_type,
    sales_organization, distribution_channel, division, order_status
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

for index, row in order_data.iterrows():
    values = (
        row["order_id"],
        row["order_date"],
        row["customer_id"],
        row["order_type"],
        row["sales_organization"],
        row["distribution_channel"],
        row["division"],
        row["order_status"]
    )

    cursor.execute(order_query, values)

print("Order data checked successfully")


# --------------------------------------------------
# Load Order Item Data - VBAP
# --------------------------------------------------

order_item_data = pd.read_excel(file_path, sheet_name="VBAP")

order_item_data = order_item_data.rename(columns={
    "Sales Document": "order_id",
    "Item Number": "item_number",
    "Material Number": "material_number",
    "Quantity": "quantity",
    "Net Price": "net_price",
    "Item Status": "item_status",
    "Delivery Date": "delivery_date"
})

order_item_query = """
INSERT IGNORE INTO fact_order_item
(
    order_id, item_number, material_number, quantity,
    net_price, item_status, delivery_date
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for index, row in order_item_data.iterrows():
    values = (
        row["order_id"],
        row["item_number"],
        row["material_number"],
        row["quantity"],
        row["net_price"],
        row["item_status"],
        row["delivery_date"]
    )

    cursor.execute(order_item_query, values)

print("Order item data checked successfully")


# --------------------------------------------------
# Load Delivery Data - LIKP
# --------------------------------------------------

delivery_data = pd.read_excel(file_path, sheet_name="LIKP")

delivery_data = delivery_data.rename(columns={
    "Delivery Number": "delivery_id",
    "Delivery Date": "delivery_date",
    "Sales Document": "order_id",
    "Shipping Point": "shipping_point",
    "Shipping Type": "shipping_type",
    "Delivery Status": "delivery_status",
    "Shipping Status": "shipping_status",
    "Route": "route",
    "Delivery Priority": "delivery_priority",
    "Customer ID": "customer_id"
})

delivery_query = """
INSERT IGNORE INTO fact_delivery
(
    delivery_id, delivery_date, order_id, shipping_point,
    shipping_type, delivery_status, shipping_status,
    route, delivery_priority, customer_id
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for index, row in delivery_data.iterrows():
    values = (
        row["delivery_id"],
        row["delivery_date"],
        row["order_id"],
        row["shipping_point"],
        row["shipping_type"],
        row["delivery_status"],
        row["shipping_status"],
        row["route"],
        row["delivery_priority"],
        row["customer_id"]
    )

    cursor.execute(delivery_query, values)

print("Delivery data checked successfully")


# --------------------------------------------------
# Load Delivery Item Data - LIPS
# --------------------------------------------------

delivery_item_data = pd.read_excel(
    file_path,
    sheet_name="LIPS"
)

print("Number of delivery items:", len(delivery_item_data))

delivery_item_data = delivery_item_data.rename(columns={
    "Delivery Number": "delivery_id",
    "Item Number": "item_number",
    "Material Number": "material_number",
    "Delivered Quantity": "delivered_quantity",
    "Net Price": "net_price",
    "Delivery Status": "delivery_status",
    "Customer ID": "customer_id",
    "Sales Document": "order_id",
    "Sales Item": "sales_item",
    "Delivery Date": "delivery_date"
})

delivery_item_query = """
INSERT IGNORE INTO fact_delivery_item
(
    delivery_id,
    item_number,
    material_number,
    delivered_quantity,
    net_price,
    delivery_status,
    customer_id,
    order_id,
    sales_item,
    delivery_date
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for index, row in delivery_item_data.iterrows():

    values = (
        row["delivery_id"],
        row["item_number"],
        row["material_number"],
        row["delivered_quantity"],
        row["net_price"],
        row["delivery_status"],
        row["customer_id"],
        row["order_id"],
        row["sales_item"],
        row["delivery_date"]
    )

    cursor.execute(delivery_item_query, values)

# --------------------------------------------------
# Load Shipment Data - VTTK
# --------------------------------------------------

shipment_data = pd.read_excel(
    file_path,
    sheet_name="VTTK"
)

print("Number of shipments:", len(shipment_data))

shipment_data = shipment_data.rename(columns={
    "Shipment Number": "shipment_id",
    "Shipment Date": "shipment_date",
    "Sales Document": "order_id",
    "Delivery Number": "delivery_id",
    "Shipping Point": "shipping_point",
    "Carrier": "carrier",
    "Shipment Status": "shipment_status",
    "Route": "route",
    "Shipping Type": "shipping_type",
    "Customer ID": "customer_id"
})

shipment_query = """
INSERT IGNORE INTO fact_shipment
(
    shipment_id,
    shipment_date,
    order_id,
    delivery_id,
    shipping_point,
    carrier,
    shipment_status,
    route,
    shipping_type,
    customer_id
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for index, row in shipment_data.iterrows():

    values = (
        row["shipment_id"],
        row["shipment_date"],
        row["order_id"],
        row["delivery_id"],
        row["shipping_point"],
        row["carrier"],
        row["shipment_status"],
        row["route"],
        row["shipping_type"],
        row["customer_id"]
    )

    cursor.execute(shipment_query, values)

print("Shipment data loaded successfully")

# --------------------------------------------------
# Load Shipment Item Data - VTTP
# --------------------------------------------------

shipment_item_data = pd.read_excel(
    file_path,
    sheet_name="VTTP"
)

print("Number of shipment items:", len(shipment_item_data))

shipment_item_data = shipment_item_data.rename(columns={
    "Shipment Number": "shipment_id",
    "Item Number": "item_number",
    "Material Number": "material_number",
    "Shipped Quantity": "shipped_quantity",
    "Item Status": "item_status",
    "Delivery Number": "delivery_id",
    "Customer ID": "customer_id",
    "Sales Document": "order_id",
    "Sales Item": "sales_item",
    "Shipment Date": "shipment_date"
})

shipment_item_query = """
INSERT IGNORE INTO fact_shipment_item
(
    shipment_id,
    item_number,
    material_number,
    shipped_quantity,
    item_status,
    delivery_id,
    customer_id,
    order_id,
    sales_item,
    shipment_date
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for index, row in shipment_item_data.iterrows():

    values = (
        row["shipment_id"],
        row["item_number"],
        row["material_number"],
        row["shipped_quantity"],
        row["item_status"],
        row["delivery_id"],
        row["customer_id"],
        row["order_id"],
        row["sales_item"],
        row["shipment_date"]
    )

    cursor.execute(shipment_item_query, values)

print("Shipment item data loaded successfully")

# Save changes
connection.commit()

print("Delivery item data loaded successfully")


# Close connection
cursor.close()
connection.close()

print("ETL process completed")