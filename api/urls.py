from django.urls import path
from .views.stocks_views import StockListCreateView

urlpatterns = [
    path('stock/<str:stock_symbol>/', StockListCreateView.as_view(), name='stock_list_create_view'),
]
