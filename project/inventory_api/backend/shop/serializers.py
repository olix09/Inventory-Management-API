from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, InventoryItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image_url']

class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'slug', 'description', 'price', 
                 'image_url', 'sizes', 'active', 'created_at', 'stock']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'size', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user_uid', 'email', 'total', 'status', 'payment_ref', 
                 'shipping_info', 'payment_method', 'created_at', 'items']
        read_only_fields = ['id', 'created_at']

class CreateOrderSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    shipping_info = serializers.DictField()
    payment_method = serializers.CharField(max_length=20)

class InventoryItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = InventoryItem
        fields = ['id', 'product', 'product_name', 'sku', 'stock', 'reorder_level', 'updated_at']

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    message = serializers.CharField()