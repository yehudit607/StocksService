from datetime import datetime
from typing import Dict, Any
from asgiref.sync import sync_to_async
from django.core.cache import cache

from StocksAPIProject.settings import CELERY_TIMEOUT
from api.models import Stock
from modules.core.exceptions import get_session_logger
from modules.stocks.src.polygon_service import fetch_stock_data, get_last_trading_day

logger = get_session_logger()


class StockService:

    @staticmethod
    async def fetch_stock_data_async(stock_symbol: str) -> Dict[str, Any]:
        return await fetch_stock_data(stock_symbol)

    @staticmethod
    async def update_or_create_stock_async(stock_data: Dict[str, Any], stock_instance: Stock) -> Stock:
        # Update each field individually
        stock_instance.status = stock_data.get("status")
        stock_instance.from_field = stock_data.get("from")
        stock_instance.open = stock_data.get("open")
        stock_instance.high = stock_data.get("high")
        stock_instance.low = stock_data.get("low")
        stock_instance.close = stock_data.get("close")
        stock_instance.volume = stock_data.get("volume")
        stock_instance.after_hours = stock_data.get("afterHours")
        stock_instance.pre_market = stock_data.get("preMarket")
        stock_instance.performance = stock_data.get("performance")

        await sync_to_async(stock_instance.save)()

        return stock_instance

    @staticmethod
    async def get_stock_data(stock_symbol: str) -> Stock:
        stock_data = await sync_to_async(cache.get)(stock_symbol)
        logger.debug("get ", stock_data)

        use_cache = False

        if stock_data:
            stock_date = stock_data.get('from_field')

            if get_last_trading_day(stock_date.date()):
                use_cache = True

        if not use_cache:
            stock_data = await StockService.fetch_stock_data_async(stock_symbol)
            result = await sync_to_async(cache.set)(stock_symbol, stock_data, CELERY_TIMEOUT)
            logger.debug(f"Setting data to Redis for key {stock_symbol}: {result}")

            stock_instance, created = await sync_to_async(Stock.objects.get_or_create)(symbol=stock_symbol)
            stock_instance = await StockService.update_or_create_stock_async(stock_data, stock_instance)
        else:
            stock_instance = await sync_to_async(Stock.objects.get)(symbol=stock_symbol)

        return stock_instance
