import json
from asgiref.sync import sync_to_async
from django.views import View

from api.exceptions import StocksException, stocks_exception
from api.schemas.stocks_scemas import StockSchema
from api.serializers.stock_serializers import StockSerializer
from modules.core.exceptions import general_exception
from modules.stocks.services.stock_service import StockService
from modules.core import IsAuthenticatedOrDev
from django.http import JsonResponse
from http import HTTPStatus


class StockListCreateView(View):
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticatedOrDev]

    async def get(self, request, *args, **kwargs) -> JsonResponse:
        try:
            stock_symbol = kwargs.get("stock_symbol")
            stock_data = await StockService.get_stock_data(stock_symbol)

            if not stock_data:
                return JsonResponse({"error": "Not Found"}, status=HTTPStatus.NOT_FOUND)

            return JsonResponse(self.serializer_class(stock_data).data, status=HTTPStatus.OK)

        except StocksException as ex:
            return stocks_exception(ex)

        except Exception as ex:
            return general_exception()

    async def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            stock_symbol = kwargs.get("stock_symbol")
            body = request.body
            body_data = json.loads(body)
            stock_data = StockSchema(data=body_data)

            if stock_data.is_valid():
                amount = stock_data.validated_data.get("amount", 0)
                stock_instance = await StockService.get_stock_data(stock_symbol)

                if not stock_instance:
                    return JsonResponse({"error": "Not Found"}, status=HTTPStatus.NOT_FOUND)

                stock_instance.amount += amount
                await sync_to_async(stock_instance.save)()

                return JsonResponse(
                    {"message": f"{amount} units of stock {stock_symbol} were added to your stock record"},
                    status=HTTPStatus.CREATED)
            else:
                raise StocksException(
                    f"Stock data is not valid with errors: {stock_data.errors}",
                    HTTPStatus.BAD_REQUEST,
                )

        except StocksException as ex:
            return stocks_exception(ex)

        except Exception as ex:
            return general_exception()

