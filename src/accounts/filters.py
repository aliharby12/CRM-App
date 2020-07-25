import django_filters
from .models import *
from django_filters import DateFilter, CharFilter

class OrderFilter(django_filters.FilterSet):
    """create a class to filter the orders"""
    # first we need to filter them by date
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')

    #then we need to filter them by description
    description = CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['date_created', 'customer']
