import pandas as pd


# Excel file
file_path = "data/SAP-DataSet.xlsx"


# Read all required sheets
customer_data = pd.read_excel(file_path, sheet_name="KNA1")
order_data = pd.read_excel(file_path, sheet_name="VBAK")
order_item_data = pd.read_excel(file_path, sheet_name="VBAP")
delivery_data = pd.read_excel(file_path, sheet_name="LIKP")
delivery_item_data = pd.read_excel(file_path, sheet_name="LIPS")
shipment_data = pd.read_excel(file_path, sheet_name="VTTK")
shipment_item_data = pd.read_excel(file_path, sheet_name="VTTP")


# Test 1: Check customer IDs are unique
def test_customer_ids_are_unique():
    assert customer_data["Customer ID"].is_unique


# Test 2: Check order IDs are unique
def test_order_ids_are_unique():
    assert order_data["Sales Document"].is_unique


# Test 3: Check order item keys are unique
def test_order_items_are_unique():
    keys = order_item_data["Sales Document"].astype(str) + "_" + \
           order_item_data["Item Number"].astype(str)

    assert keys.is_unique


# Test 4: Check delivery IDs are unique
def test_delivery_ids_are_unique():
    assert delivery_data["Delivery Number"].is_unique


# Test 5: Check shipment IDs are unique
def test_shipment_ids_are_unique():
    assert shipment_data["Shipment Number"].is_unique


# Test 6: Check there are no missing values
def test_customer_data_has_no_missing_values():
    assert customer_data.isnull().sum().sum() == 0


# Test 7: Check order data has no missing values
def test_order_data_has_no_missing_values():
    assert order_data.isnull().sum().sum() == 0


# Test 8: Check delivery data has no missing values
def test_delivery_data_has_no_missing_values():
    assert delivery_data.isnull().sum().sum() == 0

# Test 9: Check that every order has a valid customer
def test_orders_have_valid_customers():
    customer_ids = set(customer_data["Customer ID"])

    for customer_id in order_data["Customer ID"]:
        assert customer_id in customer_ids


# Test 10: Check that every order item belongs to a valid order
def test_order_items_have_valid_orders():
    order_ids = set(order_data["Sales Document"])

    for order_id in order_item_data["Sales Document"]:
        assert order_id in order_ids


# Test 11: Check that every delivery belongs to a valid order
def test_deliveries_have_valid_orders():
    order_ids = set(order_data["Sales Document"])

    for order_id in delivery_data["Sales Document"]:
        assert order_id in order_ids


# Test 12: Check that every delivery item belongs to a valid delivery
def test_delivery_items_have_valid_deliveries():
    delivery_ids = set(delivery_data["Delivery Number"])

    for delivery_id in delivery_item_data["Delivery Number"]:
        assert delivery_id in delivery_ids


# Test 13: Check that every shipment belongs to a valid delivery
def test_shipments_have_valid_deliveries():
    delivery_ids = set(delivery_data["Delivery Number"])

    for delivery_id in shipment_data["Delivery Number"]:
        assert delivery_id in delivery_ids


# Test 14: Check that every shipment item belongs to a valid shipment
def test_shipment_items_have_valid_shipments():
    shipment_ids = set(shipment_data["Shipment Number"])

    for shipment_id in shipment_item_data["Shipment Number"]:
        assert shipment_id in shipment_ids