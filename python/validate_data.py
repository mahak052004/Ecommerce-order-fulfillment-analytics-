import pandas as pd

FILE_PATH = "data/SAP-DataSet.xlsx"

# Load all tables
tables = pd.read_excel(
    FILE_PATH,
    sheet_name=None
)

KNA1 = tables["KNA1"]
LFA1 = tables["LFA1"]
VBAK = tables["VBAK"]
VBAP = tables["VBAP"]
LIKP = tables["LIKP"]
LIPS = tables["LIPS"]
VTTK = tables["VTTK"]
VTTP = tables["VTTP"]


def check_unique(df, columns, table_name):
    duplicates = df[df.duplicated(subset=columns, keep=False)]

    print(f"\n{table_name} - Key: {columns}")

    if duplicates.empty:
        print("PASS: Key is unique.")
    else:
        print("FAIL: Duplicate key values found:")
        print(duplicates[columns].to_string(index=False))


def check_reference(child_df, child_column, parent_df, parent_column,
                    child_table, parent_table):
    child_values = set(child_df[child_column])
    parent_values = set(parent_df[parent_column])

    missing = child_values - parent_values

    print(
        f"\n{child_table}.{child_column} "
        f"-> {parent_table}.{parent_column}"
    )

    if not missing:
        print("PASS: All references are valid.")
    else:
        print("FAIL: Invalid references found:")
        print(sorted(missing))


print("=" * 70)
print("SHOPX DATA VALIDATION")
print("=" * 70)


# ---------------------------------------------------------
# 1. PRIMARY / COMPOSITE KEY UNIQUENESS
# ---------------------------------------------------------

print("\n\n1. KEY UNIQUENESS CHECKS")
print("-" * 70)

check_unique(
    KNA1,
    ["Customer ID"],
    "KNA1"
)

check_unique(
    LFA1,
    ["Vendor Number"],
    "LFA1"
)

check_unique(
    VBAK,
    ["Sales Document"],
    "VBAK"
)

check_unique(
    VBAP,
    ["Sales Document", "Item Number"],
    "VBAP"
)

check_unique(
    LIKP,
    ["Delivery Number"],
    "LIKP"
)

check_unique(
    LIPS,
    ["Delivery Number", "Item Number"],
    "LIPS"
)

check_unique(
    VTTK,
    ["Shipment Number"],
    "VTTK"
)

check_unique(
    VTTP,
    ["Shipment Number", "Item Number"],
    "VTTP"
)


# ---------------------------------------------------------
# 2. CUSTOMER REFERENCES
# ---------------------------------------------------------

print("\n\n2. CUSTOMER REFERENCE CHECKS")
print("-" * 70)

check_reference(
    VBAK,
    "Customer ID",
    KNA1,
    "Customer ID",
    "VBAK",
    "KNA1"
)

check_reference(
    LIKP,
    "Customer ID",
    KNA1,
    "Customer ID",
    "LIKP",
    "KNA1"
)

check_reference(
    LIPS,
    "Customer ID",
    KNA1,
    "Customer ID",
    "LIPS",
    "KNA1"
)

check_reference(
    VTTK,
    "Customer ID",
    KNA1,
    "Customer ID",
    "VTTK",
    "KNA1"
)

check_reference(
    VTTP,
    "Customer ID",
    KNA1,
    "Customer ID",
    "VTTP",
    "KNA1"
)


# ---------------------------------------------------------
# 3. ORDER REFERENCES
# ---------------------------------------------------------

print("\n\n3. SALES ORDER REFERENCE CHECKS")
print("-" * 70)

check_reference(
    VBAP,
    "Sales Document",
    VBAK,
    "Sales Document",
    "VBAP",
    "VBAK"
)

check_reference(
    LIKP,
    "Sales Document",
    VBAK,
    "Sales Document",
    "LIKP",
    "VBAK"
)

check_reference(
    LIPS,
    "Sales Document",
    VBAK,
    "Sales Document",
    "LIPS",
    "VBAK"
)

check_reference(
    VTTK,
    "Sales Document",
    VBAK,
    "Sales Document",
    "VTTK",
    "VBAK"
)

check_reference(
    VTTP,
    "Sales Document",
    VBAK,
    "Sales Document",
    "VTTP",
    "VBAK"
)


# ---------------------------------------------------------
# 4. DELIVERY REFERENCES
# ---------------------------------------------------------

print("\n\n4. DELIVERY REFERENCE CHECKS")
print("-" * 70)

check_reference(
    LIPS,
    "Delivery Number",
    LIKP,
    "Delivery Number",
    "LIPS",
    "LIKP"
)

check_reference(
    VTTK,
    "Delivery Number",
    LIKP,
    "Delivery Number",
    "VTTK",
    "LIKP"
)

check_reference(
    VTTP,
    "Delivery Number",
    LIKP,
    "Delivery Number",
    "VTTP",
    "LIKP"
)


# ---------------------------------------------------------
# 5. SHIPMENT REFERENCES
# ---------------------------------------------------------

print("\n\n5. SHIPMENT REFERENCE CHECKS")
print("-" * 70)

check_reference(
    VTTP,
    "Shipment Number",
    VTTK,
    "Shipment Number",
    "VTTP",
    "VTTK"
)


# ---------------------------------------------------------
# 6. CROSS-TABLE CONSISTENCY
# ---------------------------------------------------------

print("\n\n6. CROSS-TABLE CONSISTENCY CHECKS")
print("-" * 70)

# LIPS Delivery -> Sales Document should agree with LIKP
likp_mapping = LIKP.set_index("Delivery Number")["Sales Document"]

lips_expected_sales = LIPS["Delivery Number"].map(likp_mapping)

lips_mismatch = LIPS[
    lips_expected_sales != LIPS["Sales Document"]
]

print("\nLIPS Delivery -> Sales Document consistency")

if lips_mismatch.empty:
    print("PASS: LIPS sales documents match LIKP.")
else:
    print("FAIL: Mismatches found:")
    print(
        lips_mismatch[
            ["Delivery Number", "Sales Document"]
        ].to_string(index=False)
    )


# VTTK Delivery -> Sales Document should agree with LIKP
vttk_expected_sales = VTTK["Delivery Number"].map(likp_mapping)

vttk_mismatch = VTTK[
    vttk_expected_sales != VTTK["Sales Document"]
]

print("\nVTTK Delivery -> Sales Document consistency")

if vttk_mismatch.empty:
    print("PASS: VTTK sales documents match LIKP.")
else:
    print("FAIL: Mismatches found:")
    print(
        vttk_mismatch[
            ["Shipment Number", "Delivery Number", "Sales Document"]
        ].to_string(index=False)
    )


# VTTP Shipment -> Delivery should agree with VTTK
vttk_delivery_mapping = VTTK.set_index(
    "Shipment Number"
)["Delivery Number"]

vttp_expected_delivery = VTTP["Shipment Number"].map(
    vttk_delivery_mapping
)

vttp_mismatch = VTTP[
    vttp_expected_delivery != VTTP["Delivery Number"]
]

print("\nVTTP Shipment -> Delivery consistency")

if vttp_mismatch.empty:
    print("PASS: VTTP deliveries match VTTK.")
else:
    print("FAIL: Mismatches found:")
    print(
        vttp_mismatch[
            ["Shipment Number", "Delivery Number"]
        ].to_string(index=False)
    )


print("\n" + "=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)