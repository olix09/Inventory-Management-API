from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from decimal import Decimal

class Category(models.Model):
    """Category model for inventory items"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    """Model for inventory items"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    # Basic Information
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Pricing and Quantity
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text="Current stock quantity"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Price per unit"
    )
    
    # Categorization
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='items'
    )
    
    # Stock Management
    minimum_stock_level = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        help_text="Minimum stock level before low stock alert"
    )
    maximum_stock_level = models.PositiveIntegerField(
        default=1000,
        validators=[MinValueValidator(1)],
        help_text="Maximum stock capacity"
    )
    
    # Priority and Status
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    
    # User Association
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inventory_items'
    )
    
    # Timestamps
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Additional Information
    sku = models.CharField(max_length=50, blank=True, help_text="Stock Keeping Unit")
    location = models.CharField(max_length=100, blank=True, help_text="Storage location")

    class Meta:
        ordering = ['-last_updated']
        unique_together = ['name', 'owner']

    def __str__(self):
        return f"{self.name} ({self.quantity} in stock)"

    @property
    def is_low_stock(self):
        """Check if item is below minimum stock level"""
        return self.quantity <= self.minimum_stock_level

    @property
    def is_out_of_stock(self):
        """Check if item is out of stock"""
        return self.quantity == 0

    @property
    def stock_status(self):
        """Get stock status string"""
        if self.is_out_of_stock:
            return "Out of Stock"
        elif self.is_low_stock:
            return "Low Stock"
        elif self.quantity >= self.maximum_stock_level:
            return "Overstocked"
        else:
            return "In Stock"

    @property
    def total_value(self):
        """Calculate total value of current stock"""
        return self.quantity * self.price

class InventoryChange(models.Model):
    """Model to track inventory changes"""
    CHANGE_TYPES = [
        ('restock', 'Restock'),
        ('sale', 'Sale'),
        ('adjustment', 'Adjustment'),
        ('damaged', 'Damaged'),
        ('returned', 'Returned'),
    ]

    inventory_item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='changes'
    )
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPES)
    quantity_changed = models.IntegerField(
        help_text="Positive for additions, negative for reductions"
    )
    previous_quantity = models.PositiveIntegerField()
    new_quantity = models.PositiveIntegerField()
    
    # Change Details
    reason = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    
    # User and Timestamp
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='inventory_changes'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.inventory_item.name}: {self.change_type} ({self.quantity_changed:+d})"

    @property
    def is_increase(self):
        """Check if this change increased inventory"""
        return self.quantity_changed > 0

    @property
    def is_decrease(self):
        """Check if this change decreased inventory"""
        return self.quantity_changed < 0