from django.db import models
                
import datetime
import pytz


# Create your models here.
# https://docs.djangoproject.com/en/3.1/topics/db/models/
# After writing model definition, run "./manage.py makemigrations" and then "./manage.py migrate"
class FBATransaction(models.Model):
    """
    A single transaction from the FBA transaction report download
    """
    KIND_CHOICES = [
        ('Order','Order'),
        ('FBA Inventory Fee','FBA Inventory Fee'),
        ('Adjustment','Adjustment'),
        ('FBA Customer Return Fee','FBA Customer Return Fee'),
        ('Transfer','Transfer'),
        ('Refund','Refund'),
        ('Order_Retrocharge','Order_Retrocharge'),
    ]

    tid = models.CharField(max_length=50, null=True)
    date_time = models.DateTimeField()
    kind = models.CharField(max_length=32, null=True, choices=KIND_CHOICES)  
    sku = models.CharField(max_length=32, null=True)
    description = models.CharField(max_length=250, default='')
    quantity = models.IntegerField(null=True)
    total =  models.DecimalField(max_digits=7, decimal_places=2, null=True)
    city = models.CharField(max_length=32, null=True)
    state = models.CharField(max_length=32, null=True)
    postal = models.CharField(max_length=16, null=True)

    class Meta:
        db_table = "fba_transactions"
        indexes = [
            models.Index(fields=['total']),
        ]

