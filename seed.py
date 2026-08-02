import pandas as pd
from datetime import datetime
from database import transactions

CSV_FILE = 'Sales_Data_Import.csv'

COLUMN_MAP = {
    'Order ID': 'order_id',
    'Order Date': 'order_date',
    'Customer ID': 'customer_id',
    'Customer Name': 'customer_name',
    'Region': 'region',
    'Category': 'category',
    'Product': 'product',
    'Quantity': 'quantity',
    'Unit Price': 'unit_price',
    'Total Amount': 'total_amount',
    'Payment Method': 'payment_method',
    'Status': 'status',
}


def parse_numeric(value):
    if pd.isna(value):
        return 0.0
    try:
        text = str(value).replace('$', '').replace(',', '').strip()
        return float(text) if text != '' else 0.0
    except (ValueError, TypeError):
        return 0.0


def parse_date(value):
    if pd.isna(value):
        return None
    text = str(value).strip()
    for fmt in ('%d-%m-%Y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    result = pd.to_datetime(text, errors='coerce')
    return result.to_pydatetime() if not pd.isna(result) else None


def normalize_row(row):
    return {
        'order_id': str(row.get('Order ID', row.get('order_id', ''))).strip(),
        'order_date': parse_date(row.get('Order Date', row.get('order_date', ''))),
        'customer_id': str(row.get('Customer ID', row.get('customer_id', ''))).strip(),
        'customer_name': str(row.get('Customer Name', row.get('customer_name', ''))).strip(),
        'region': str(row.get('Region', row.get('region', ''))).strip(),
        'category': str(row.get('Category', row.get('category', ''))).strip(),
        'product': str(row.get('Product', row.get('product', ''))).strip(),
        'quantity': int(row.get('Quantity', row.get('quantity', 0)) or 0),
        'unit_price': parse_numeric(row.get('Unit Price', row.get('Unit Price ($)', row.get('unit_price', 0)))),
        'total_amount': parse_numeric(row.get('Total Amount', row.get('Total Amount ($)', row.get('total_amount', 0)))),
        'payment_method': str(row.get('Payment Method', row.get('payment_method', ''))).strip(),
        'status': str(row.get('Status', row.get('status', ''))).strip(),
    }


def seed_database():
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print('CSV file is empty or not found. Please check Sales_Data_Import.csv')
        return

    documents = [normalize_row(row) for _, row in df.iterrows()]
    if not documents:
        print('No rows found to insert.')
        return

    transactions.delete_many({})
    result = transactions.insert_many(documents)
    print(f'Inserted {len(result.inserted_ids)} documents into {transactions.full_name}.')


if __name__ == '__main__':
    seed_database()
