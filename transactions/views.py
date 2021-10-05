import csv
import logging

from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Avg, Sum
from django.db.models.functions import Round
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from django.utils.dateparse import parse_datetime

from .serializers import (FBATransactionCreateSerializer, FBATransactionSerializer, FBATransactionAggregateSerializer)
from .models import FBATransaction
from .aggregators import Median

logger = logging.getLogger(__name__)

class TransactionListViewMixin():
    """
    Mixin that allows filtering the queryset by GET params.

    params:
    type (str): Returns transactions of this type (Order)
    skus (list): Returns transactions with this SKU, should be sent/parsed as a comma separated string if multiple SKU's (N1N-ELDERBERRY-GUMMIES-FBA,N1N-BERBERINE-FBA)
    start (str): Returns transactions occurring after this date/time (2008-11-01T17:34:49%2B07:00)
    end (str): Returns transactions occurring before this date/time (2008-11-01T17:34:49%2B07:00)
    city (str): Returns transactions in this city (NEW BRAUNFELS)
    state (str): Returns transactions in this state (TX)
    postal (str): Returns transactions in this postal address (78130-8371)
    """

    def get_queryset(self):
        params = self.request.GET.dict()
        queryset = FBATransaction.objects
        if 'type' in params:
            queryset = queryset.filter(kind=params.get('type'))
        if 'skus' in params:
            skus = params.get('skus').split(',')
            queryset = queryset.filter(sku__in=skus)
        if 'start' in params:
            start_dt = parse_datetime(params.get('start'))
            queryset = queryset.filter(date_time__gte=start_dt)
        if 'end' in params:
            end_dt = parse_datetime(params.get('end'))
            queryset = queryset.filter(date_time__lte=end_dt)
        if 'city' in params:
            queryset = queryset.filter(city=params.get('city'))
        if 'state' in params:
            queryset = queryset.filter(state=params.get('state'))
        if 'postal' in params:
            queryset = queryset.filter(postal=params.get('postal'))
        return queryset


class TransactionsListCreateView(TransactionListViewMixin, ListCreateAPIView):
    """
    Handles creating transactions
    """

    permission_classes = (AllowAny,)
    serializer_class = FBATransactionSerializer

    def create(self, request, *args, **kwargs):
        # wipe the slate clean.
        FBATransaction.objects.all().delete()
        for _, file in request.FILES.items():
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file, delimiter=',')
            # run sequentially (as opposed to many=True) for better error feedback.
            for row in reader:
                # replace empty strings with None.
                row = {k: v if v else None for k, v in row.items()}
                data = dict(
                    date_time=row.get('date/time'),
                    kind=row.get('type'),
                    tid=row.get('order id'),
                    sku=row.get('sku'),
                    description=row.get('description'),
                    quantity=row.get('quantity'),
                    city=row.get('order city'),
                    state=row.get('order state'),
                    postal=row.get('order postal'),
                    total=row.get('total')
                )
                serializer = FBATransactionCreateSerializer(data=data)
                try:
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                except serializers.ValidationError:
                    logger.exception(row)
                    return Response(
                        f"Encountered Errors:{serializer.errors} For data: {row}", 
                        status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(
            f"Imported {FBATransaction.objects.count()} transactions.",
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data)
        )


class TransactionsStatsView(TransactionListViewMixin, GenericAPIView):
    """
    Returns aggregated stats of transactions by the given filters
    containing the summed, average, and median totals for transactions.
    """
    serializer_class = FBATransactionAggregateSerializer

    def get_queryset(self):
        querySet = super().get_queryset()
        agg = querySet.aggregate(sum=Round(Sum('total')), average=Round(Avg('total')))
        agg['median'] = Median(querySet, 'total').aggregate()
        print(agg)
        # agg = dict(
        #     sum=2, average=2, median=2
        # )
        return agg
    
    def get(self, request):
        data = self.get_queryset()
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
            logger.info(f'Bad stats data: {data}')
            return Response('bad request: {data}', status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)
