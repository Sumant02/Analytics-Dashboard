import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pymongo import ASCENDING, DESCENDING
import jinja2

from database import transactions

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(BASE_DIR, 'templates')),
    autoescape=jinja2.select_autoescape(['html', 'xml']),
)


def build_filter(
    customer_name: Optional[str],
    category: Optional[str],
    product: Optional[str],
    min_amount: Optional[float],
    max_amount: Optional[float],
    start_date: Optional[str],
    end_date: Optional[str],
):
    filter_query = {}

    if customer_name:
        filter_query['customer_name'] = {'$regex': customer_name, '$options': 'i'}
    if category:
        filter_query['category'] = {'$regex': category, '$options': 'i'}
    if product:
        filter_query['product'] = {'$regex': product, '$options': 'i'}
    if min_amount is not None or max_amount is not None:
        amount_query = {}
        if min_amount is not None:
            amount_query['$gte'] = min_amount
        if max_amount is not None:
            amount_query['$lte'] = max_amount
        filter_query['total_amount'] = amount_query
    if start_date or end_date:
        date_query = {}
        if start_date:
            date_query['$gte'] = datetime.fromisoformat(start_date)
        if end_date:
            date_query['$lte'] = datetime.fromisoformat(end_date)
        filter_query['order_date'] = date_query

    return filter_query


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    template = jinja_env.get_template('index.html')
    return HTMLResponse(template.render())


@app.get('/api/sales')
async def get_sales(
    customer_name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    product: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    filter_query = build_filter(customer_name, category, product, min_amount, max_amount, start_date, end_date)
    cursor = transactions.find(filter_query).sort('order_date', DESCENDING).limit(1000)
    results = []
    for doc in cursor:
        results.append({
            'order_id': doc.get('order_id'),
            'order_date': doc.get('order_date').isoformat() if doc.get('order_date') else None,
            'customer_name': doc.get('customer_name'),
            'region': doc.get('region'),
            'category': doc.get('category'),
            'product': doc.get('product'),
            'quantity': doc.get('quantity'),
            'unit_price': doc.get('unit_price'),
            'total_amount': doc.get('total_amount'),
            'payment_method': doc.get('payment_method'),
            'status': doc.get('status'),
        })

    return JSONResponse({'data': results})


@app.get('/api/sales/summary')
async def get_sales_summary(
    customer_name: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    product: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    filter_query = build_filter(customer_name, category, product, min_amount, max_amount, start_date, end_date)
    pipeline = [
        {'$match': filter_query} if filter_query else {'$match': {}},
        {
            '$facet': {
                'summary': [
                    {
                        '$group': {
                            '_id': None,
                            'total_sales': {'$sum': '$total_amount'},
                            'total_orders': {'$sum': 1},
                            'average_order_value': {'$avg': '$total_amount'},
                        }
                    }
                ],
                'category_breakdown': [
                    {
                        '$group': {
                            '_id': '$category',
                            'total_sales': {'$sum': '$total_amount'},
                            'orders': {'$sum': 1},
                        }
                    },
                    {'$sort': {'total_sales': -1}}
                ],
                'monthly_trends': [
                    {
                        '$group': {
                            '_id': {
                                'year': {'$year': '$order_date'},
                                'month': {'$month': '$order_date'},
                            },
                            'total_sales': {'$sum': '$total_amount'},
                            'orders': {'$sum': 1},
                        }
                    },
                    {
                        '$sort': {
                            '_id.year': ASCENDING,
                            '_id.month': ASCENDING,
                        }
                    }
                ],
            }
        }
    ]

    stats = list(transactions.aggregate(pipeline))[0]
    summary = stats['summary'][0] if stats['summary'] else {
        'total_sales': 0,
        'total_orders': 0,
        'average_order_value': 0,
    }
    monthly_trends = [
        {
            'month': f"{item['_id']['year']}-{item['_id']['month']:02d}",
            'total_sales': item['total_sales'],
            'orders': item['orders'],
        }
        for item in stats['monthly_trends']
    ]
    category_breakdown = [
        {
            'category': item['_id'] or 'Unknown',
            'total_sales': item['total_sales'],
            'orders': item['orders'],
        }
        for item in stats['category_breakdown']
    ]

    return JSONResponse(
        {
            'total_sales': summary['total_sales'],
            'total_orders': summary['total_orders'],
            'average_order_value': summary['average_order_value'],
            'category_breakdown': category_breakdown,
            'monthly_trends': monthly_trends,
        }
    )
