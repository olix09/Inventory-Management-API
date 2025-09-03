from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal
import json

from .models import Category, Product, Order, OrderItem, InventoryItem, StockMovement
from .serializers import (
    CategorySerializer, ProductSerializer, OrderSerializer, 
    CreateOrderSerializer, InventoryItemSerializer, ContactSerializer
)

@api_view(['GET'])
def category_list(request):
    """List all categories"""
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_list(request):
    """List products, optionally filtered by category"""
    category_slug = request.GET.get('category')
    
    queryset = Product.objects.filter(active=True)
    
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)
    
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    """Get product details"""
    product = get_object_or_404(Product, pk=pk, active=True)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inventory_list(request):
    """List inventory items (admin only)"""
    inventory_items = InventoryItem.objects.select_related('product').all()
    serializer = InventoryItemSerializer(inventory_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """Create a new order"""
    serializer = CreateOrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    
    try:
        with transaction.atomic():
            # Calculate total
            total = Decimal('0.00')
            order_items_data = []
            
            for item_data in data['items']:
                product = get_object_or_404(Product, id=item_data['product_id'])
                quantity = int(item_data['quantity'])
                
                # Check stock
                if product.stock < quantity:
                    return Response(
                        {'error': f'Insufficient stock for {product.name}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                price = Decimal(str(product.price))
                subtotal = price * quantity
                total += subtotal
                
                order_items_data.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price,
                    'size': item_data.get('size', ''),
                    'subtotal': subtotal
                })
            
            # Create order
            order = Order.objects.create(
                user_uid=request.user['uid'],
                email=request.user['email'],
                total=total,
                shipping_info=data['shipping_info'],
                payment_method=data['payment_method']
            )
            
            # Create order items and update stock
            for item_data in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    product=item_data['product'],
                    quantity=item_data['quantity'],
                    price=item_data['price'],
                    size=item_data['size']
                )
                
                # Update inventory (simplified - assumes single inventory item per product)
                inventory_item = InventoryItem.objects.filter(product=item_data['product']).first()
                if inventory_item:
                    inventory_item.stock -= item_data['quantity']
                    inventory_item.save()
                    
                    # Record stock movement
                    StockMovement.objects.create(
                        product=item_data['product'],
                        change=-item_data['quantity'],
                        reason='sale',
                        note=f'Order #{order.id}'
                    )
            
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list(request):
    """List user's orders"""
    orders = Order.objects.filter(user_uid=request.user['uid']).prefetch_related('items__product')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_cbe(request):
    """Process checkout with CBE"""
    # This is a placeholder implementation
    # In production, integrate with actual CBE API
    
    serializer = CreateOrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # TODO: Integrate with CBE API
    # 1. Validate payment details
    # 2. Process payment with CBE
    # 3. Handle payment confirmation
    
    # For now, create order and simulate payment
    order_response = create_order(request)
    if order_response.status_code == 201:
        order_data = order_response.data
        return Response({
            'payment_url': f'https://cbe-payment-gateway.com/pay?ref={order_data["id"]}',
            'order_id': order_data['id'],
            'status': 'payment_initiated'
        })
    
    return order_response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_telebirr(request):
    """Process checkout with Telebirr"""
    # This is a placeholder implementation
    # In production, integrate with actual Telebirr API
    
    serializer = CreateOrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # TODO: Integrate with Telebirr API
    # 1. Validate payment details
    # 2. Process payment with Telebirr
    # 3. Handle payment confirmation
    
    # For now, create order and simulate payment
    order_response = create_order(request)
    if order_response.status_code == 201:
        order_data = order_response.data
        return Response({
            'payment_url': f'https://telebirr-gateway.com/pay?ref={order_data["id"]}',
            'order_id': order_data['id'],
            'status': 'payment_initiated'
        })
    
    return order_response

@api_view(['POST'])
def contact_submit(request):
    """Handle contact form submission"""
    serializer = ContactSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    try:
        # Send email
        subject = f"Contact Form: Message from {data['name']}"
        message = f"""
        Name: {data['name']}
        Email: {data['email']}
        
        Message:
        {data['message']}
        """
        
        send_mail(
            subject,
            message,
            data['email'],
            [settings.CONTACT_RECEIVER_EMAIL],
            fail_silently=False,
        )
        
        return Response({'message': 'Message sent successfully'})
        
    except Exception as e:
        return Response(
            {'error': 'Failed to send message'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )