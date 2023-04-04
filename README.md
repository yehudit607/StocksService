# StocksService
Stock Data API is a web application that allows users to fetch and manage stock data using a RESTful API. The application fetches stock data from an external service, caches the data using Redis, and stores the data in a Django database. Users can get stock data, as well as add or update their stock records.

Features

Fetch stock data from an external service (Polygon.io)
Cache stock data using Redis for improved performance
Store and manage stock data in a Django database
User authentication and authorization
RESTful API for fetching and updating stock data

Prerequisites

Docker
Docker Compose

Installation

Clone the repository:

git clone https://github.com/yourusername/StockDataAPI.git
cd StockDataAPI
Build the Docker images:

docker-compose build
Run the services:
docker-compose up -d
This command will start the Django application, Redis, and PostgreSQL services.

Run database migrations:
docker-compose exec web python manage.py migrate
Create a superuser (optional):

docker-compose exec web python manage.py createsuperuser
Follow the prompts to create a superuser account for the Django admin site.

Usage
API Endpoints
Get stock data: GET /api/stocks/{stock_symbol}/
Add stock units: POST /api/stocks/{stock_symbol}/
Request body: {"amount": <integer>}
Example
Fetch stock data for the AAPL stock:


 GET http://localhost:8000/api/stocks/AAPL/
Add 10 units of the AAPL stock to your record:

curl -X POST -H "Content-Type: application/json" -d '{"amount": 10}' http://localhost:8000/api/stocks/AAPL/
