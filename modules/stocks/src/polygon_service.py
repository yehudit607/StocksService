import asyncio
from http import HTTPStatus
from typing import Dict, Any, Optional

import pytz
from aiohttp import ClientSession
from rest_framework import status

from api.exceptions import StocksException
from modules.stocks.helpers.constants import API_KEY
from modules.stocks.src.marketwatch_service import scrape_performance_data
from datetime import datetime, timedelta, time
from pandas.tseries.offsets import BDay

from datetime import date
from pandas.tseries.offsets import BDay


def get_last_trading_day(reference_date: Optional[date] = None) -> date:
    # If no reference_date is provided, use the current date in the US/Eastern timezone
    if reference_date is None:
        reference_date = datetime.now(pytz.timezone('US/Eastern')).date()
    # Return the previous business day
    return (reference_date - BDay(1)).date()


async def fetch_stock_data(stock_symbol: str) -> Dict[str, Any]:
    last_trading_day = get_last_trading_day()
    date = last_trading_day.strftime("%Y-%m-%d")

    async with ClientSession() as session:
        stock_data_task = asyncio.ensure_future(fetch_polygon_stock_data(stock_symbol, date, session))
        performance_data_task = asyncio.ensure_future(scrape_performance_data(stock_symbol, session))

        stock_data, performance_data = await asyncio.gather(stock_data_task, performance_data_task)

    stock_data["performance"] = performance_data
    date = stock_data.get("from", None)
    if date:
        stock_data["from_field"] = datetime.strptime(date, "%Y-%m-%d")
    stock_data["amount"] = 0

    return stock_data


async def fetch_polygon_stock_data(stock_symbol: str, date: str, session: ClientSession) -> Dict[str, Any]:
    url = f"https://api.polygon.io/v1/open-close/{stock_symbol}/{date}?apiKey={API_KEY}"
    async with session.get(url) as response:
        if response.status != status.HTTP_200_OK:
            raise StocksException(
                "failed to fetch stock data",
                HTTPStatus.BAD_REQUEST,
            )
        stock_data = await response.json()
    return stock_data
