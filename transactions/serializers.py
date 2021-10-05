import pytz
import datetime

from django.db.models import Q
from rest_framework import serializers

from .models import FBATransaction


class FBATransactionCreateSerializer(serializers.ModelSerializer):

    date_time = serializers.CharField()  # can't use DateTimeField(input_formats), see: validate_date_time

    def validate_date_time(self, dt):
        try:
            # strip timezone to enable parsing: https://bugs.python.org/issue22377
            dt_unaware = dt.replace(' PDT', '').replace(' PST', '')
            date_time = datetime.datetime.strptime(dt_unaware, "%b %d, %Y %I:%M:%S %p")
            date_time = date_time.replace(tzinfo=pytz.timezone("America/Los_Angeles"))
            return date_time
        except:
            raise serializers.ValidationError(f"Unable to parse date/time: {dt}")

    class Meta:
        model = FBATransaction
        exclude = []


class FBATransactionSerializer(serializers.ModelSerializer):

    _kind = serializers.CharField(source='kind')
    _id = serializers.CharField(source='tid')

    def get_fields(self):
        # fix reserved words
        result = super().get_fields()
        result['type'] = result.pop('_kind')
        result['id'] = result.pop('_id')
        return result

    class Meta:
        model = FBATransaction
        exclude = ['tid','kind']


class FBATransactionAggregateSerializer(serializers.Serializer):

    summation = serializers.DecimalField(max_digits=16, decimal_places=2)
    average = serializers.DecimalField(max_digits=16, decimal_places=2)
    median = serializers.DecimalField(max_digits=16, decimal_places=2)

    def get_fields(self):
        # fix reserved words
        result = super().get_fields()
        result['sum'] = result.pop('summation')
        return result
