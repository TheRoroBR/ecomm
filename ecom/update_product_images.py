import os
import django
from pathlib import Path
from shutil import copy2

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
django.setup()

from shop.models import Product, Category
from django.conf import settings
from datetime import datetime

# Mapeamento de imagens por categoria/tipo de produto
IMAGE_MAPPING = {
    'whey': ['whey.png', ['Whey', 'WHEY']],
    'creatina': ['creatina.png', ['Creatina', 'CREATINA']],
    'bcaa': ['bcaa.png', ['BCAA']],
    'pretreino': ['pretreino.png', ['Cafeina', 'Mix Cafeina', 'Poli aminoacidos', 'Multivitaminas']],
    'barraproteina': ['barraproteina.png', ['Barra de Proteína', 'Barra']],
    'snacks': ['snacks.png', ['Lanche', 'Lanchinho', 'Palitos']],
    'legging': ['legging.png', ['Calça', 'Legging']],
    'anilhaflex': ['anilhaflex.webp', ['Anilha', 'Halter', 'Banda', 'Bolsa', 'Coqueteleira']],
}

def get_image_for_product(product_name):
    """
    Retorna a imagem apropriada baseada no nome do produto
    """
    product_name_lower = product_name.lower()
    
    # Verifica cada categoria no mapeamento
    for key, (image_file, keywords) in IMAGE_MAPPING.items():
        for keyword in keywords:
            if keyword.lower() in product_name_lower:
                return image_file
    
    # Imagem padrão se nenhuma categoria corresponder
    return 'no_image.png'

def update_product_images():
    """
    Atualiza as imagens dos produtos baseado nas categorias
    """
    source_dir = Path(settings.BASE_DIR) / 'shop' / 'static' / 'img'
    media_dir = Path(settings.MEDIA_ROOT) / 'products'
    media_dir.mkdir(parents=True, exist_ok=True)
    
    # Criar estrutura de diretórios com data atual
    now = datetime.now()
    dest_dir = media_dir / str(now.year) / f"{now.month:02d}" / f"{now.day:02d}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    products = Product.objects.all()
    
    print(f"Atualizando {products.count()} produtos...\n")
    
    updated_count = 0
    
    for product in products:
        # Determinar qual imagem usar
        image_file = get_image_for_product(product.name)
        source_image = source_dir / image_file
        
        if not source_image.exists():
            print(f"⚠️  Imagem não encontrada: {image_file}")
            continue
        
        # Criar nome único para o arquivo
        file_extension = source_image.suffix
        dest_file = dest_dir / f'product_{product.id}{file_extension}'
        
        # Copiar a imagem
        copy2(source_image, dest_file)
        
        # Atualizar produto com caminho relativo
        relative_path = f'products/{now.year}/{now.month:02d}/{now.day:02d}/product_{product.id}{file_extension}'
        product.image = relative_path
        product.save()
        
        updated_count += 1
        print(f"✓ {product.name[:50]:50} -> {image_file}")
    
    print(f"\n{'='*80}")
    print(f"✓ Sucesso! {updated_count} produtos atualizados com novas imagens!")
    print(f"{'='*80}")
    
    # Estatísticas por tipo de imagem
    print("\nEstatísticas:")
    for key, (image_file, _) in IMAGE_MAPPING.items():
        count = 0
        for product in products:
            if get_image_for_product(product.name) == image_file:
                count += 1
        if count > 0:
            print(f"  {image_file:25} : {count} produtos")

if __name__ == '__main__':
    update_product_images()
