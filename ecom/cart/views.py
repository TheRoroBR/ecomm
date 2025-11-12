from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib import messages


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        qty = cd['quantity']
        override = cd.get('override', False)

        # Determine current quantity in cart
        current_qty = 0
        existing = cart.cart.get(str(product.id))
        if existing:
            current_qty = existing.get('quantity', 0)

        # Determine the prospective new quantity depending on override
        new_total = qty if override else current_qty + qty

        # If product has a stock attribute, enforce it
        product_stock = getattr(product, 'stock', None)
        if product_stock is not None and new_total > product_stock:
            messages.error(request, f"Only {product_stock} unit(s) of '{product.name}' available. You tried to add {new_total}.")
            # Redirect back to the referring page if possible
            ref = request.META.get('HTTP_REFERER')
            if ref:
                return redirect(ref)
            return redirect('shop:product_list')

        cart.add(product=product,
                 quantity=qty,
                 override_quantity=override)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})