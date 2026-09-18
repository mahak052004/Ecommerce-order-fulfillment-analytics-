import pandas as pd

file_path = "data/SAP-DataSet.xlsx"

excel_file = pd.ExcelFile(file_path)

print("Excel sheets:")
print(excel_file.sheet_names)

print("\n" + "=" * 60)

for sheet in excel_file.sheet_names:
    df = pd.read_excel(file_path, sheet_name=sheet)

    print(f"\nTABLE: {sheet}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumn names:")
    print(list(df.columns))

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())

    print("=" * 60)