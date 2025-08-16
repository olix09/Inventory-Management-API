from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Sum, Count
from decimal import Decimal
from .models import InventoryItem, InventoryChange, Category
from .serializers import (
    InventoryItemSerializer, 
    InventoryChangeSerializer, 
    InventoryItemDetailSerializer,
    CategorySerializer
)
from .filters import InventoryItemFilter

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request,
        # but write permissions only to the owner of the object.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class InventoryItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing inventory items with advanced filtering and search
    """
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = InventoryItemFilter
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['name', 'quantity', 'price', 'date_added', 'last_updated']
    ordering = ['-last_updated']

    def get_queryset(self):
        """Return inventory items for the current user"""
        return InventoryItem.objects.filter(owner=self.request.user).select_related('category', 'owner')

    def get_serializer_class(self):
        """Use detailed serializer for retrieve action"""
        if self.action == 'retrieve':
            return InventoryItemDetailSerializer
        return InventoryItemSerializer

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get items with low stock levels"""
        queryset = self.get_queryset().filter(
            quantity__lte=models.F('minimum_stock_level')
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'items': serializer.data
        })

    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """Get items that are out of stock"""
        queryset = self.get_queryset().filter(quantity=0)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'items': serializer.data
        })

    @action(detail=False, methods=['get'])
    def overstocked(self, request):
        """Get items that are overstocked"""
        queryset = self.get_queryset().filter(
            quantity__gte=models.F('maximum_stock_level')
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'items': serializer.data
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get inventory summary statistics"""
        queryset = self.get_queryset()
        
        total_items = queryset.count()
        total_quantity = queryset.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_value = sum(item.total_value for item in queryset)
        
        low_stock_count = queryset.filter(
            quantity__lte=models.F('minimum_stock_level')
        ).count()
        
        out_of_stock_count = queryset.filter(quantity=0).count()
        
        categories_data = Category.objects.filter(
            items__owner=request.user
        ).annotate(
            item_count=Count('items')
        ).values('name', 'item_count')

        return Response({
            'total_items': total_items,
            'total_quantity': total_quantity,
            'total_value': total_value,
            'low_stock_items': low_stock_count,
            'out_of_stock_items': out_of_stock_count,
            'categories': list(categories_data)
        })

    @action(detail=True, methods=['post'])
    def adjust_quantity(self, request, pk=None):
        """Manually adjust item quantity with reason"""
        item = self.get_object()
        quantity_change = request.data.get('quantity_change')
        reason = request.data.get('reason', '')
        notes = request.data.get('notes', '')
        
        if quantity_change is None:
            return Response(
                {'error': 'quantity_change is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            quantity_change = int(quantity_change)
        except ValueError:
            return Response(
                {'error': 'quantity_change must be an integer'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create inventory change record
        change_data = {
            'inventory_item': item,
            'change_type': 'adjustment',
            'quantity_changed': quantity_change,
            'reason': reason,
            'notes': notes
        }
        
        change_serializer = InventoryChangeSerializer(
            data=change_data, 
            context={'request': request}
        )
        
        if change_serializer.is_valid():
            change_serializer.save()
            item.refresh_from_db()
            
            return Response({
                'message': 'Quantity adjusted successfully',
                'item': InventoryItemSerializer(item).data,
                'change': change_serializer.data
            })
        
        return Response(change_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InventoryChangeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing inventory changes (read-only)
    Changes are created through the InventoryItemViewSet or separate API
    """
    serializer_class = InventoryChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['change_type', 'inventory_item']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        """Return changes for current user's inventory items"""
        return InventoryChange.objects.filter(
            inventory_item__owner=self.request.user
        ).select_related('inventory_item', 'changed_by')

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent inventory changes"""
        queryset = self.get_queryset()[:20]  # Last 20 changes
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get changes grouped by type"""
        change_types = InventoryChange.CHANGE_TYPES
        result = {}
        
        for change_type, display_name in change_types:
            changes = self.get_queryset().filter(change_type=change_type)[:10]
            result[change_type] = {
                'display_name': display_name,
                'count': changes.count(),
                'changes': InventoryChangeSerializer(changes, many=True).data
            }
        
        return Response(result)