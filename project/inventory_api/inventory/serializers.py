from rest_framework import serializers
from .models import InventoryItem, InventoryChange, Category

class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'item_count']
        read_only_fields = ['id', 'created_at']

    def get_item_count(self, obj):
        """Get count of items in this category"""
        return obj.items.count()

class InventoryItemSerializer(serializers.ModelSerializer):
    """Serializer for InventoryItem model"""
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_low_stock = serializers.ReadOnlyField()
    is_out_of_stock = serializers.ReadOnlyField()
    stock_status = serializers.ReadOnlyField()
    total_value = serializers.ReadOnlyField()

    class Meta:
        model = InventoryItem
        fields = [
            'id', 'name', 'description', 'quantity', 'price', 'category', 
            'category_name', 'minimum_stock_level', 'maximum_stock_level',
            'priority', 'owner', 'owner_username', 'date_added', 'last_updated',
            'sku', 'location', 'is_low_stock', 'is_out_of_stock', 'stock_status',
            'total_value'
        ]
        read_only_fields = ['id', 'owner', 'date_added', 'last_updated']

    def validate_quantity(self, value):
        """Validate quantity is not negative"""
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value

    def validate_price(self, value):
        """Validate price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate(self, data):
        """Cross-field validation"""
        minimum_stock = data.get('minimum_stock_level', 0)
        maximum_stock = data.get('maximum_stock_level', 1000)
        
        if minimum_stock >= maximum_stock:
            raise serializers.ValidationError(
                "Minimum stock level must be less than maximum stock level"
            )
        
        return data

    def create(self, validated_data):
        """Create inventory item with current user as owner"""
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class InventoryChangeSerializer(serializers.ModelSerializer):
    """Serializer for InventoryChange model"""
    inventory_item_name = serializers.CharField(source='inventory_item.name', read_only=True)
    changed_by_username = serializers.CharField(source='changed_by.username', read_only=True)
    is_increase = serializers.ReadOnlyField()
    is_decrease = serializers.ReadOnlyField()

    class Meta:
        model = InventoryChange
        fields = [
            'id', 'inventory_item', 'inventory_item_name', 'change_type',
            'quantity_changed', 'previous_quantity', 'new_quantity',
            'reason', 'notes', 'changed_by', 'changed_by_username',
            'timestamp', 'is_increase', 'is_decrease'
        ]
        read_only_fields = [
            'id', 'changed_by', 'timestamp', 'previous_quantity', 'new_quantity'
        ]

    def create(self, validated_data):
        """Create inventory change and update item quantity"""
        validated_data['changed_by'] = self.context['request'].user
        
        inventory_item = validated_data['inventory_item']
        quantity_change = validated_data['quantity_changed']
        
        # Record current state
        validated_data['previous_quantity'] = inventory_item.quantity
        validated_data['new_quantity'] = inventory_item.quantity + quantity_change
        
        # Validate new quantity won't be negative
        if validated_data['new_quantity'] < 0:
            raise serializers.ValidationError(
                f"Cannot reduce quantity by {abs(quantity_change)}. "
                f"Current quantity is {inventory_item.quantity}"
            )
        
        # Update inventory item quantity
        inventory_item.quantity = validated_data['new_quantity']
        inventory_item.save()
        
        return super().create(validated_data)

class InventoryItemDetailSerializer(InventoryItemSerializer):
    """Detailed serializer including change history"""
    recent_changes = serializers.SerializerMethodField()
    change_count = serializers.SerializerMethodField()

    class Meta(InventoryItemSerializer.Meta):
        fields = InventoryItemSerializer.Meta.fields + ['recent_changes', 'change_count']

    def get_recent_changes(self, obj):
        """Get recent changes for this item"""
        recent_changes = obj.changes.all()[:5]  # Last 5 changes
        return InventoryChangeSerializer(recent_changes, many=True).data

    def get_change_count(self, obj):
        """Get total number of changes for this item"""
        return obj.changes.count()