from django.contrib import admin
from .models import Category, Product, InventoryItem, StockMovement, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'active', 'created_at')
    list_filter = ('category', 'active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [InventoryItemInline]
    
    def stock(self, obj):
        return obj.stock
    stock.short_description = 'Current Stock'

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'sku', 'stock', 'reorder_level', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('product__name', 'sku')

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'change', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('product__name', 'note')
    readonly_fields = ('created_at',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'size')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'total', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('email', 'user_uid')
    readonly_fields = ('user_uid', 'created_at')
    inlines = [OrderItemInline]
    
    actions = ['mark_as_paid', 'mark_as_canceled']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid')
    mark_as_paid.short_description = "Mark selected orders as paid"
    
    def mark_as_canceled(self, request, queryset):
        queryset.update(status='canceled')
    mark_as_canceled.short_description = "Mark selected orders as canceled"