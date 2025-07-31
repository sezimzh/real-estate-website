import django_filters
from .models import Estate

class EstateFilter(django_filters.FilterSet):
  price_lte=django_filters.NumberFilter(field_name='price',lookup_expr='lte')
  price_gte=django_filters.NumberFilter(field_name='price',lookup_expr='gte')
  
  class Meta:
        model = Estate
        fields = ['category', 'city','price_lte','price_gte']
