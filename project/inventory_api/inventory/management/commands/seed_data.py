from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from inventory.models import InventoryItem, Category, InventoryChange
from decimal import Decimal
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with sample inventory data'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=2, help='Number of users to create')
        parser.add_argument('--items', type=int, default=20, help='Number of items per user')

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')

        # Create categories
        categories = [
            ('Electronics', 'Electronic devices and components'),
            ('Clothing', 'Apparel and accessories'),
            ('Books', 'Educational and entertainment books'),
            ('Home & Garden', 'Home improvement and gardening supplies'),
            ('Sports', 'Sports equipment and accessories'),
            ('Office Supplies', 'Office and business supplies'),
        ]

        category_objects = []
        for name, description in categories:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            category_objects.append(category)
            if created:
                self.stdout.write(f'Created category: {name}')

        # Create sample users
        users = []
        for i in range(options['users']):
            username = f'user{i+1}'
            email = f'user{i+1}@example.com'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'User{i+1}',
                    'last_name': 'Sample'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                users.append(user)
                self.stdout.write(f'Created user: {username}')

        # Sample item names by category
        sample_items = {
            'Electronics': [
                'Laptop Computer', 'Wireless Mouse', 'USB Cable', 'Smartphone',
                'Headphones', 'Monitor', 'Keyboard', 'Speaker'
            ],
            'Clothing': [
                'T-Shirt', 'Jeans', 'Sneakers', 'Jacket',
                'Dress Shirt', 'Sweater', 'Cap', 'Belt'
            ],
            'Books': [
                'Programming Guide', 'History Book', 'Novel', 'Cookbook',
                'Science Textbook', 'Biography', 'Art Book', 'Dictionary'
            ],
            'Home & Garden': [
                'Garden Tool', 'Plant Pot', 'Light Bulb', 'Cleaning Supplies',
                'Paint Brush', 'Fertilizer', 'Watering Can', 'Seeds'
            ],
            'Sports': [
                'Basketball', 'Tennis Racket', 'Soccer Ball', 'Running Shoes',
                'Yoga Mat', 'Dumbbells', 'Water Bottle', 'Sports Bag'
            ],
            'Office Supplies': [
                'Pen Set', 'Notebook', 'Stapler', 'File Folder',
                'Printer Paper', 'Desk Lamp', 'Calculator', 'Whiteboard'
            ]
        }

        # Create inventory items for each user
        for user in users:
            items_created = 0
            for category in category_objects:
                items_for_category = min(4, options['items'] // len(category_objects) + 1)
                
                for i in range(items_for_category):
                    if items_created >= options['items']:
                        break
                        
                    item_names = sample_items.get(category.name, ['Sample Item'])
                    name = random.choice(item_names)
                    
                    # Make name unique for this user
                    base_name = name
                    counter = 1
                    while InventoryItem.objects.filter(owner=user, name=name).exists():
                        name = f"{base_name} {counter}"
                        counter += 1

                    item = InventoryItem.objects.create(
                        name=name,
                        description=f"Sample {name.lower()} for inventory management",
                        quantity=random.randint(0, 100),
                        price=Decimal(str(random.uniform(10, 500))).quantize(Decimal('0.01')),
                        category=category,
                        minimum_stock_level=random.randint(5, 20),
                        maximum_stock_level=random.randint(100, 500),
                        priority=random.choice(['low', 'medium', 'high']),
                        owner=user,
                        sku=f"SKU-{random.randint(1000, 9999)}",
                        location=random.choice(['A1', 'B2', 'C3', 'D4', 'Warehouse', 'Store Front'])
                    )
                    
                    # Create some inventory changes
                    for _ in range(random.randint(1, 5)):
                        InventoryChange.objects.create(
                            inventory_item=item,
                            change_type=random.choice(['restock', 'sale', 'adjustment']),
                            quantity_changed=random.randint(-20, 50),
                            previous_quantity=random.randint(0, 100),
                            new_quantity=random.randint(0, 100),
                            reason=f"Sample {random.choice(['restock', 'sale', 'adjustment'])}",
                            changed_by=user
                        )
                    
                    items_created += 1

            self.stdout.write(f'Created {items_created} items for {user.username}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded database with {len(users)} users, '
                f'{len(category_objects)} categories, and sample inventory items'
            )
        )