from django.core.management.base import BaseCommand
from django.utils.text import slugify
from shop.models import Category, Product, InventoryItem

class Command(BaseCommand):
    help = 'Seed the database with sample categories and products'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with sample data...')

        # Create categories
        categories_data = [
            {
                'name': 'T-Shirts',
                'image_url': 'https://images.pexels.com/photos/8532616/pexels-photo-8532616.jpeg?auto=compress&cs=tinysrgb&w=800'
            },
            {
                'name': 'Jackets',
                'image_url': 'https://images.pexels.com/photos/1032110/pexels-photo-1032110.jpeg?auto=compress&cs=tinysrgb&w=800'
            },
            {
                'name': 'Shoes',
                'image_url': 'https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=800'
            },
            {
                'name': 'Bags',
                'image_url': 'https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg?auto=compress&cs=tinysrgb&w=800'
            },
            {
                'name': 'Accessories',
                'image_url': 'https://images.pexels.com/photos/3661175/pexels-photo-3661175.jpeg?auto=compress&cs=tinysrgb&w=800'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'image_url': cat_data['image_url']
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            # T-Shirts
            {
                'name': 'Classic Cotton T-Shirt',
                'category': 'T-Shirts',
                'description': 'Premium 100% cotton t-shirt with comfortable fit and durable construction.',
                'price': '450.00',
                'image_url': 'https://images.pexels.com/photos/8532616/pexels-photo-8532616.jpeg?auto=compress&cs=tinysrgb&w=600',
                'sizes': ['S', 'M', 'L', 'XL'],
                'stock': 25
            },
            {
                'name': 'Graphic Print Tee',
                'category': 'T-Shirts',
                'description': 'Stylish graphic print t-shirt made from soft cotton blend fabric.',
                'price': '520.00',
                'image_url': 'https://images.pexels.com/photos/8532616/pexels-photo-8532616.jpeg?auto=compress&cs=tinysrgb&w=600',
                'sizes': ['S', 'M', 'L', 'XL'],
                'stock': 18
            },
            
            # Jackets
            {
                'name': 'Winter Bomber Jacket',
                'category': 'Jackets',
                'description': 'Warm and stylish bomber jacket perfect for cold weather.',
                'price': '1850.00',
                'image_url': 'https://images.pexels.com/photos/1032110/pexels-photo-1032110.jpeg?auto=compress&cs=tinysrgb&w=600',
                'sizes': ['S', 'M', 'L', 'XL'],
                'stock': 12
            },
            {
                'name': 'Denim Jacket',
                'category': 'Jackets',
                'description': 'Classic denim jacket with modern fit and premium quality.',
                'price': '1650.00',
                'image_url': 'https://images.pexels.com/photos/1032110/pexels-photo-1032110.jpeg?auto=compress&cs=tinysrgb&w=600',
                'sizes': ['S', 'M', 'L', 'XL'],
                'stock': 15
            },
            
            # Shoes
            {
                'name': 'Running Sneakers',
                'category': 'Shoes',
                'description': 'Comfortable running shoes with excellent cushioning and support.',
                'price': '2200.00',
                'image_url': 'https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=600',
                'sizes': ['38', '39', '40', '41', '42', '43', '44'],
                'stock': 20
            },
            {
                'name': 'Casual Loafers',
                'category': 'Shoes',
                'description': 'Elegant casual loafers perfect for everyday wear.',
                'price': '1950.00',
                'image_url': 'https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=600',
                'sizes': ['38', '39', '40', '41', '42', '43', '44'],
                'stock': 14
            },
            
            # Bags
            {
                'name': 'Leather Backpack',
                'category': 'Bags',
                'description': 'Premium leather backpack with multiple compartments.',
                'price': '2800.00',
                'image_url': 'https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg?auto=compress&cs=tinysrgb&w=600',
                'sizes': ['One Size'],
                'stock': 8
            },
            {
                'name': 'Canvas Tote Bag',
                'category': 'Bags',
                'description': 'Eco-friendly canvas tote bag perfect for daily use.',
                'price': '850.00',
                'image_url': 'https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg?auto=compress&cs=tinysrgb&w=600',
                'sizes': ['One Size'],
                'stock': 22
            },
            
            # Accessories
            {
                'name': 'Leather Watch',
                'category': 'Accessories',
                'description': 'Elegant leather strap watch with classic design.',
                'price': '1200.00',
                'image_url': 'https://images.pexels.com/photos/3661175/pexels-photo-3661175.jpeg?auto=compress&cs=tinysrgb&w=600',
                'sizes': ['One Size'],
                'stock': 16
            },
            {
                'name': 'Sunglasses',
                'category': 'Accessories',
                'description': 'UV protection sunglasses with modern frame design.',
                'price': '750.00',
                'image_url': 'https://images.pexels.com/photos/3661175/pexels-photo-3661175.jpeg?auto=compress&cs=tinysrgb&w=600',
                'sizes': ['One Size'],
                'stock': 30
            }
        ]

        for product_data in products_data:
            category = categories[product_data['category']]
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'category': category,
                    'slug': slugify(product_data['name']),
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'image_url': product_data['image_url'],
                    'sizes': product_data['sizes']
                }
            )
            
            if created:
                # Create inventory item
                InventoryItem.objects.create(
                    product=product,
                    sku=f'AB-{product.id:04d}',
                    stock=product_data['stock'],
                    reorder_level=5
                )
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded database with sample data!')
        )