from django.contrib import admin
from .models import Category, InventoryItem, InventoryChange

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'owner')
    ordering = ('name',)


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'category', 'quantity', 'price', 'display_stock_status', 'owner', 'last_updated')
    list_filter = ('category', 'priority', 'owner', 'date_added')
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('date_added', 'last_updated', 'display_total_value', 'display_stock_status')
    ordering = ('-last_updated',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'sku', 'category', 'owner')
        }),
        ('Inventory Details', {
            'fields': ('quantity', 'price', 'minimum_stock_level', 'maximum_stock_level', 'priority', 'location')
        }),
        ('Computed Fields', {
            'fields': ('display_total_value', 'display_stock_status'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('date_added', 'last_updated'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Total Value')
    def display_total_value(self, obj):
        if obj.quantity is not None and obj.price is not None:
            return obj.total_value
        return 0

    @admin.display(description='Stock Status')
    def display_stock_status(self, obj):
        return obj.stock_status


@admin.register(InventoryChange)
class InventoryChangeAdmin(admin.ModelAdmin):
    list_display = ('inventory_item', 'change_type', 'quantity_changed', 'changed_by', 'timestamp')
    list_filter = ('change_type', 'timestamp', 'changed_by')
    search_fields = ('inventory_item__name', 'inventory_item__sku', 'reason')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
