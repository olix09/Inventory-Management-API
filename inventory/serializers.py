from rest_framework import serializers
from .models import Category, InventoryItem, InventoryChange


class CategorySerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'created_at', 'items_count')
        read_only_fields = ('id', 'created_at')
    
    def get_items_count(self, obj):
        return obj.items.count()
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class InventoryItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    stock_status = serializers.ReadOnlyField()
    total_value = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    is_out_of_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = InventoryItem
        fields = (
            'id', 'name', 'description', 'quantity', 'price', 'category', 'category_name',
            'minimum_stock_level', 'maximum_stock_level', 'priority', 'sku', 'location',
            'date_added', 'last_updated', 'stock_status', 'total_value', 'is_low_stock', 'is_out_of_stock'
        )
        read_only_fields = ('id', 'date_added', 'last_updated')
    
    def validate_maximum_stock_level(self, value):
        minimum_stock_level = self.initial_data.get('minimum_stock_level', 0)
        if value <= minimum_stock_level:
            raise serializers.ValidationError("Maximum stock level must be greater than minimum stock level")
        return value
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class InventoryItemDetailSerializer(InventoryItemSerializer):
    changes_count = serializers.SerializerMethodField()
    recent_changes = serializers.SerializerMethodField()
    
    class Meta(InventoryItemSerializer.Meta):
        fields = InventoryItemSerializer.Meta.fields + ('changes_count', 'recent_changes')
    
    def get_changes_count(self, obj):
        return obj.changes.count()
    
    def get_recent_changes(self, obj):
        recent_changes = obj.changes.all()[:5]
        return InventoryChangeSerializer(recent_changes, many=True).data


class InventoryChangeSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='inventory_item.name', read_only=True)
    item_sku = serializers.CharField(source='inventory_item.sku', read_only=True)
    changed_by_username = serializers.CharField(source='changed_by.username', read_only=True)
    is_increase = serializers.ReadOnlyField()
    is_decrease = serializers.ReadOnlyField()
    
    class Meta:
        model = InventoryChange
        fields = (
            'id', 'inventory_item', 'item_name', 'item_sku', 'change_type',
            'quantity_changed', 'previous_quantity', 'new_quantity', 'reason',
            'notes', 'changed_by', 'changed_by_username', 'timestamp',
            'is_increase', 'is_decrease'
        )
        read_only_fields = ('id', 'timestamp', 'changed_by')
    
    def validate_quantity_changed(self, value):
        if value == 0:
            raise serializers.ValidationError("Quantity changed cannot be zero")
        return value


class QuantityAdjustmentSerializer(serializers.Serializer):
    quantity_change = serializers.IntegerField()
    change_type = serializers.ChoiceField(choices=InventoryChange.CHANGE_TYPE_CHOICES)
    reason = serializers.CharField(max_length=200, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_quantity_change(self, value):
        if value == 0:
            raise serializers.ValidationError("Quantity change cannot be zero")
        return value