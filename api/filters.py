from django_filters import rest_framework as filters
from . import models


class OrderStatusFilter(filters.FilterSet):
    class Meta:
        model = models.Order
        fields = ['status']
