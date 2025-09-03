from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['name', 'owner']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.owner.username})"


class InventoryItem(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    minimum_stock_level = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    maximum_stock_level = models.IntegerField(default=100, validators=[MinValueValidator(1)])
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')
    sku = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_updated']
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    @property
    def is_low_stock(self):
        return self.quantity <= self.minimum_stock_level
    
    @property
    def is_out_of_stock(self):
        return self.quantity == 0
    
    @property
    def stock_status(self):
        if self.is_out_of_stock:
            return 'out_of_stock'
        elif self.is_low_stock:
            return 'low_stock'
        elif self.quantity >= self.maximum_stock_level:
            return 'overstocked'
        return 'normal'
    
@property
def total_value(self):
    quantity = self.quantity or 0
    price = self.price or Decimal('0.00')
    return quantity * price



class InventoryChange(models.Model):
    CHANGE_TYPE_CHOICES = [
        ('restock', 'Restock'),
        ('sale', 'Sale'),
        ('adjustment', 'Adjustment'),
        ('damaged', 'Damaged'),
        ('returned', 'Returned'),
    ]
    
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='changes')
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE_CHOICES)
    quantity_changed = models.IntegerField()
    previous_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    reason = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.inventory_item.name} - {self.change_type} ({self.quantity_changed})"
    
    @property
    def is_increase(self):
        return self.quantity_changed > 0
    
    @property
    def is_decrease(self):
        return self.quantity_changed < 0