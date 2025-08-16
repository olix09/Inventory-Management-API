import django_filters
from django.db import models
from .models import InventoryItem, Category

class InventoryItemFilter(django_filters.FilterSet):
    """Advanced filtering for inventory items"""
    
    # Price range filtering
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    price_range = django_filters.RangeFilter(field_name='price')
    
    # Quantity filtering
    quantity_min = django_filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    quantity_max = django_filters.NumberFilter(field_name='quantity', lookup_expr='lte')
    
    # Date filtering
    date_added_after = django_filters.DateTimeFilter(field_name='date_added', lookup_expr='gte')
    date_added_before = django_filters.DateTimeFilter(field_name='date_added', lookup_expr='lte')
    
    # Stock status filtering
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')
    out_of_stock = django_filters.BooleanFilter(method='filter_out_of_stock')
    overstocked = django_filters.BooleanFilter(method='filter_overstocked')
    
    # Category filtering
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    
    # Text search
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = InventoryItem
        fields = {
            'name': ['exact', 'icontains'],
            'sku': ['exact', 'icontains'],
            'priority': ['exact'],
            'location': ['exact', 'icontains'],
        }

    def filter_low_stock(self, queryset, name, value):
        """Filter items with low stock"""
        if value:
            return queryset.filter(quantity__lte=models.F('minimum_stock_level'))
        return queryset

    def filter_out_of_stock(self, queryset, name, value):
        """Filter items that are out of stock"""
        if value:
            return queryset.filter(quantity=0)
        return queryset

    def filter_overstocked(self, queryset, name, value):
        """Filter items that are overstocked"""
        if value:
            return queryset.filter(quantity__gte=models.F('maximum_stock_level'))
        return queryset

    def filter_search(self, queryset, name, value):
        """Search across multiple fields"""
        if value:
            return queryset.filter(
                models.Q(name__icontains=value) |
                models.Q(description__icontains=value) |
                models.Q(sku__icontains=value) |
                models.Q(category__name__icontains=value)
            )
        return queryset