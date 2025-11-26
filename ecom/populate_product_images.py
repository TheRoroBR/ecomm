import os
import django
from pathlib import Path
from shutil import copy2

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
django.setup()

from shop.models import Product
from django.conf import settings

def populate_images():
    """
    Populate product images by copying the logo.png to each product
    """
    # Get the source image
    source_image = Path(settings.BASE_DIR) / 'shop' / 'static' / 'img' / 'logo.png'
    
    if not source_image.exists():
        print(f"Source image not found: {source_image}")
        return
    
    # Create media directory if it doesn't exist
    media_dir = Path(settings.MEDIA_ROOT) / 'products'
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all products without images
    products = Product.objects.filter(image='')
    
    print(f"Found {products.count()} products without images")
    
    for product in products:
        # Create year/month/day directory structure
        from datetime import datetime
        now = datetime.now()
        dest_dir = media_dir / str(now.year) / f"{now.month:02d}" / f"{now.day:02d}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Create unique filename based on product id
        dest_file = dest_dir / f'product_{product.id}.png'
        
        # Copy the image
        copy2(source_image, dest_file)
        
        # Update product with relative path
        relative_path = f'products/{now.year}/{now.month:02d}/{now.day:02d}/product_{product.id}.png'
        product.image = relative_path
        product.save()
        
        print(f"Updated product: {product.name} -> {relative_path}")
    
    print(f"\nSuccessfully updated {products.count()} products!")

if __name__ == '__main__':
    populate_images()
