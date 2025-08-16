from django.contrib import admin
from .models import InventoryItem, InventoryChange, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'price', 'owner', 'stock_status', 'last_updated')
    list_filter = ('category', 'priority', 'date_added')
    search_fields = ('name', 'description', 'sku')
    readonly_fields = ('date_added', 'last_updated', 'stock_status', 'total_value')
    ordering = ('-last_updated',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'sku', 'category')
        }),
        ('Stock Information', {
            'fields': ('quantity', 'minimum_stock_level', 'maximum_stock_level')
        }),
        ('Pricing', {
            'fields': ('price', 'total_value')
        }),
        ('Management', {
            'fields': ('owner', 'priority', 'location')
        }),
        ('Timestamps', {
            'fields': ('date_added', 'last_updated'),
            'classes': ('collapse',)
        }),
    )

@admin.register(InventoryChange)
class InventoryChangeAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'change_type', 'quantity_changed', 'changed_by', 'timestamp')
    list_filter = ('change_type', 'timestamp')
    search_fields = ('inventory_item__name', 'reason')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)