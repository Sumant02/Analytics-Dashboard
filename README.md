# Analytics Dashboard

A production-ready Sales & Customer Analytics Dashboard built with:
- FastAPI + PyMongo
- Jinja2 templates with React loaded via CDN
- Tailwind CSS and Chart.js
- MongoDB for transaction analytics

## What is included
- `main.py` - FastAPI backend with HTML rendering and API endpoints
- `database.py` - MongoDB connection setup
- `seed.py` - CSV seed script for populating the `transactions` collection
- `templates/index.html` - dashboard UI with React and Chart.js
- `Sales_Data_Import.csv` - sample transaction dataset
- `requirements.txt` - Python dependencies
- `SalesDashboard.postman_collection.json` - Postman collection for API testing
- `SalesDashboard.postman_environment.json` - Postman environment sample
- `test_connection.py` - MongoDB connection validation helper script

## Project structure

```
Analytics Dashboard/
├── Sales_Data_Import.csv
├── .env.example
├── .gitignore
├── README.md
├── database.py
├── main.py
├── seed.py
├── requirements.txt
├── test_connection.py
├── templates/
│   └── index.html
├── SalesDashboard.postman_collection.json
└── SalesDashboard.postman_environment.json
```

## Setup and install

1. Create a Python virtual environment and activate it.

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Create `.env` from `.env.example` and update the MongoDB connection string.

```powershell
copy .env.example .env
```

4. Configure `MONGO_URI` in `.env` for either MongoDB Atlas or a local MongoDB instance.

## Seed the database

Run the seed script to import `Sales_Data_Import.csv` into the `transactions` collection.

```powershell
python seed.py
```

## Run the application

```powershell
uvicorn main:app --reload --port 8000
```

Open the dashboard at:

```
http://localhost:8000
```

## API endpoints

- `GET /api/sales` - Returns transaction records filtered by query parameters
- `GET /api/sales/summary` - Returns KPIs, monthly sales trends, and category breakdowns

### Supported query parameters
- `customer_name`
- `category`
- `product`
- `min_amount`
- `max_amount`
- `start_date` (ISO `YYYY-MM-DD`)
- `end_date` (ISO `YYYY-MM-DD`)

## Postman testing

Import `SalesDashboard.postman_collection.json` into Postman and use the `localhost` environment to test the API endpoints.

## Notes

- Do not commit `.env`; it is ignored by `.gitignore`.
- If using MongoDB Atlas, install `dnspython` for SRV support via `requirements.txt`.
- For local MongoDB, ensure `mongod` is running before seeding or starting the app.
