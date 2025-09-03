from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, Count
from .models import Category, InventoryItem, InventoryChange
from .serializers import (
    CategorySerializer, InventoryItemSerializer, InventoryItemDetailSerializer,
    InventoryChangeSerializer, QuantityAdjustmentSerializer
)
from .permissions import IsOwnerOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)


class InventoryItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'quantity', 'price', 'date_added', 'last_updated']
    ordering = ['-last_updated']
    filterset_fields = ['category', 'priority']
    
    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user).select_related('category')
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InventoryItemDetailSerializer
        return InventoryItemSerializer
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get items with low stock levels"""
        low_stock_items = self.get_queryset().filter(
            quantity__lte=models.F('minimum_stock_level')
        )
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        """Get items that are out of stock"""
        out_of_stock_items = self.get_queryset().filter(quantity=0)
        serializer = self.get_serializer(out_of_stock_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overstocked(self, request):
        """Get items that are overstocked"""
        overstocked_items = self.get_queryset().filter(
            quantity__gte=models.F('maximum_stock_level')
        )
        serializer = self.get_serializer(overstocked_items, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get inventory summary statistics"""
        queryset = self.get_queryset()
        
        total_items = queryset.count()
        total_value = queryset.aggregate(
            total=Sum(models.F('quantity') * models.F('price'))
        )['total'] or 0
        
        low_stock_count = queryset.filter(
            quantity__lte=models.F('minimum_stock_level')
        ).count()
        
        out_of_stock_count = queryset.filter(quantity=0).count()
        
        overstocked_count = queryset.filter(
            quantity__gte=models.F('maximum_stock_level')
        ).count()
        
        categories_count = Category.objects.filter(owner=request.user).count()
        
        return Response({
            'total_items': total_items,
            'total_value': total_value,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'overstocked_count': overstocked_count,
            'categories_count': categories_count,
        })
    
    @action(detail=True, methods=['post'])
    def adjust_quantity(self, request, pk=None):
        """Adjust the quantity of an inventory item"""
        item = self.get_object()
        serializer = QuantityAdjustmentSerializer(data=request.data)
        
        if serializer.is_valid():
            quantity_change = serializer.validated_data['quantity_change']
            change_type = serializer.validated_data['change_type']
            reason = serializer.validated_data.get('reason', '')
            notes = serializer.validated_data.get('notes', '')
            
            previous_quantity = item.quantity
            new_quantity = previous_quantity + quantity_change
            
            if new_quantity < 0:
                return Response(
                    {'error': 'Insufficient stock for this operation'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Update item quantity
            item.quantity = new_quantity
            item.save()
            
            # Create inventory change record
            InventoryChange.objects.create(
                inventory_item=item,
                change_type=change_type,
                quantity_changed=quantity_change,
                previous_quantity=previous_quantity,
                new_quantity=new_quantity,
                reason=reason,
                notes=notes,
                changed_by=request.user
            )
            
            return Response({
                'message': 'Quantity adjusted successfully',
                'previous_quantity': previous_quantity,
                'new_quantity': new_quantity,
                'quantity_changed': quantity_change
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryChangeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventoryChangeSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['timestamp', 'change_type']
    ordering = ['-timestamp']
    filterset_fields = ['change_type', 'inventory_item']
    
    def get_queryset(self):
        return InventoryChange.objects.filter(
            inventory_item__owner=self.request.user
        ).select_related('inventory_item', 'changed_by')
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent inventory changes (last 50)"""
        recent_changes = self.get_queryset()[:50]
        serializer = self.get_serializer(recent_changes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get inventory changes grouped by type"""
        change_type = request.query_params.get('type')
        if not change_type:
            return Response(
                {'error': 'Please specify a change type'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        changes = self.get_queryset().filter(change_type=change_type)
        serializer = self.get_serializer(changes, many=True)
        return Response(serializer.data)