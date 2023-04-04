
from rest_framework import serializers


class StockSchema(serializers.Serializer):
    amount = serializers.IntegerField(required=True)


