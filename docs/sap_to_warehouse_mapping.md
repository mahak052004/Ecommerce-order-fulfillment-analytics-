# SAP to Data Warehouse Mapping

## Project

E-Commerce Order Fulfillment Analytics

## Source Dataset

SAP-DataSet.xlsx

The source workbook contains the following SAP-style tables:

- KNA1 - Customer Master
- LFA1 - Vendor Master
- VBAK - Sales Order Header
- VBAP - Sales Order Item
- LIKP - Delivery Header
- LIPS - Delivery Item
- VTTK - Shipment Header
- VTTP - Shipment Item

---

# 1. Customer Master

## Source Table: KNA1

| Source Column | Target Table | Target Column |
|---|---|---|
| Customer ID | dim_customer | customer_id |
| Customer Name | dim_customer | customer_name |
| Country | dim_customer | country |
| Region | dim_customer | region |
| City | dim_customer | city |
| Postal Code | dim_customer | postal_code |
| Street Address | dim_customer | street_address |
| Phone Number | dim_customer | phone_number |
| Email Address | dim_customer | email_address |
| Language | dim_customer | language |
| Tax Number | dim_customer | tax_number |
| Customer Group | dim_customer | customer_group |
| Sales Organization | dim_customer | sales_organization |
| Distribution Channel | dim_customer | distribution_channel |
| Division | dim_customer | division |

Primary Key:

Customer ID

---

# 2. Vendor Master

## Source Table: LFA1

The supplied dataset contains a vendor master table.

| Source Column | Source Table |
|---|---|
| Vendor Number | LFA1 |
| Vendor Name | LFA1 |
| Country | LFA1 |
| Region | LFA1 |
| City | LFA1 |
| Postal Code | LFA1 |
| Street Address | LFA1 |
| Phone Number | LFA1 |
| Email Address | LFA1 |
| Language | LFA1 |
| Tax Number | LFA1 |
| Payment Terms | LFA1 |

Primary Key:

Vendor Number

### Relationship Note

The supplied transactional tables do not contain a Vendor Number field.

Therefore, a reliable relationship between LFA1 and the order/delivery/shipment transaction flow cannot be established from the supplied dataset.

No artificial vendor relationship will be created.

---

# 3. Sales Order Header

## Source Table: VBAK

Target Table:

fact_order

| Source Column | Target Column |
|---|---|
| Sales Document | order_id |
| Order Date | order_date |
| Customer ID | customer_id |
| Order Type | order_type |
| Sales Organization | sales_organization |
| Distribution Channel | distribution_channel |
| Division | division |
| Order Status | order_status |

Primary Key:

Sales Document

Foreign Key:

Customer ID -> dim_customer.customer_id

---

# 4. Sales Order Item

## Source Table: VBAP

Target Table:

fact_order_item

| Source Column | Target Column |
|---|---|
| Sales Document | order_id |
| Item Number | item_number |
| Material Number | material_number |
| Quantity | quantity |
| Net Price | net_price |
| Item Status | item_status |
| Delivery Date | delivery_date |

Composite Primary Key:

Sales Document + Item Number

Foreign Key:

Sales Document -> fact_order.order_id

---

# 5. Delivery Header

## Source Table: LIKP

Target Table:

fact_delivery

| Source Column | Target Column |
|---|---|
| Delivery Number | delivery_id |
| Delivery Date | delivery_date |
| Sales Document | order_id |
| Shipping Point | shipping_point |
| Shipping Type | shipping_type |
| Delivery Status | delivery_status |
| Shipping Status | shipping_status |
| Route | route |
| Delivery Priority | delivery_priority |
| Customer ID | customer_id |

Primary Key:

Delivery Number

Foreign Keys:

Sales Document -> fact_order.order_id

Customer ID -> dim_customer.customer_id

---

# 6. Delivery Item

## Source Table: LIPS

Target Table:

fact_delivery_item

| Source Column | Target Column |
|---|---|
| Delivery Number | delivery_id |
| Item Number | item_number |
| Material Number | material_number |
| Delivered Quantity | delivered_quantity |
| Net Price | net_price |
| Delivery Status | delivery_status |
| Customer ID | customer_id |
| Sales Document | order_id |
| Sales Item | sales_item |
| Delivery Date | delivery_date |

Composite Primary Key:

Delivery Number + Item Number

Foreign Keys:

Delivery Number -> fact_delivery.delivery_id

Sales Document -> fact_order.order_id

Customer ID -> dim_customer.customer_id

---

# 7. Shipment Header

## Source Table: VTTK

Target Table:

fact_shipment

| Source Column | Target Column |
|---|---|
| Shipment Number | shipment_id |
| Shipment Date | shipment_date |
| Sales Document | order_id |
| Delivery Number | delivery_id |
| Shipping Point | shipping_point |
| Carrier | carrier |
| Shipment Status | shipment_status |
| Route | route |
| Shipping Type | shipping_type |
| Customer ID | customer_id |

Primary Key:

Shipment Number

Foreign Keys:

Delivery Number -> fact_delivery.delivery_id

Sales Document -> fact_order.order_id

Customer ID -> dim_customer.customer_id

---

# 8. Shipment Item

## Source Table: VTTP

Target Table:

fact_shipment_item

| Source Column | Target Column |
|---|---|
| Shipment Number | shipment_id |
| Item Number | item_number |
| Material Number | material_number |
| Shipped Quantity | shipped_quantity |
| Item Status | item_status |
| Delivery Number | delivery_id |
| Customer ID | customer_id |
| Sales Document | order_id |
| Sales Item | sales_item |
| Shipment Date | shipment_date |

Composite Primary Key:

Shipment Number + Item Number

Foreign Keys:

Shipment Number -> fact_shipment.shipment_id

Delivery Number -> fact_delivery.delivery_id

Sales Document -> fact_order.order_id

Customer ID -> dim_customer.customer_id

---

# 9. Data Validation Results

The source dataset was validated using Python before SQL implementation.

## Key Uniqueness

All tested primary/composite keys were unique.

Validated keys:

- KNA1: Customer ID
- LFA1: Vendor Number
- VBAK: Sales Document
- VBAP: Sales Document + Item Number
- LIKP: Delivery Number
- LIPS: Delivery Number + Item Number
- VTTK: Shipment Number
- VTTP: Shipment Number + Item Number

## Referential Integrity

The following references were validated successfully:

- Customer references
- Sales order references
- Delivery references
- Shipment references

## Cross-table Consistency

The following relationships were validated successfully:

- LIPS Delivery -> Sales Document
- VTTK Delivery -> Sales Document
- VTTP Shipment -> Delivery

No invalid references or duplicate keys were found during validation.

---

# 10. Source Data Limitations

The supplied workbook contains eight source tables.

The following limitations were identified:

1. LFA1 contains vendor information but no transaction table contains Vendor Number, so a vendor-to-transaction relationship cannot be reliably established.

2. Material master information is not provided through a separate MARA table in the supplied workbook.

3. Inventory movement information is not provided through a separate MKPF table in the supplied workbook.

4. Missing source information will not be artificially generated.

5. Analytical requirements that depend on unavailable source fields will be identified and documented.

---

# 11. Planned Technology Stack

## Python

Used for:

- Data inspection
- Data validation
- Data cleaning/transformation
- Loading data into MySQL

## MySQL

Used for:

- Data warehouse creation
- Relational data modelling
- SQL transformations
- Analytical queries

## Power BI

Used for:

- Data visualization
- KPI dashboards
- Order analysis
- Delivery analysis
- Shipment analysis
- Fulfillment performance analysis

## GitHub

Used for:

- Version control
- Project documentation
- Source code
- SQL scripts
- Power BI project files