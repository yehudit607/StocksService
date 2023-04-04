from django.db import models


class Stock(models.Model):
    after_hours = models.FloatField(null=True)
    close = models.FloatField(null=True)
    from_field = models.CharField(null=True, max_length=50)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)
    open = models.FloatField(null=True)
    pre_market = models.FloatField(null=True)
    status = models.CharField(null=True, max_length=50)
    symbol = models.CharField(max_length=10)
    volume = models.IntegerField(null=True)
    performance = models.JSONField(null=True)
    amount = models.IntegerField(null=True, default=0)
