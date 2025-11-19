def homepage(request):
    categories = Category.objects.all()
    # Exibe só produtos em destaque (exemplo: os 8 mais recentes)
    featured_products = Product.objects.filter(available=True).order_by('-created')[:8]
    return render(request, 'shop/homepage.html', {
        'categories': categories,
        'featured_products': featured_products,
    })
from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    # Pass a simple scalar for the currently selected category (slug)
    # so templates can compare literals safely without complex inline
    # expressions that the template parser may misinterpret.
    return render(request,
                  'shop/product/list.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products,
                      'current_category_slug': category.slug if category else None,
                  })


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    # If product has stock, set the form's max attribute to the stock value
    if hasattr(product, 'stock') and product.stock is not None:
        try:
            cart_product_form.fields['quantity'].widget.attrs['max'] = product.stock
        except Exception:
            # If form structure changes, ignore and use default
            pass
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})