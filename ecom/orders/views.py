from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Validate stock for all items first
            insufficient = []
            for item in cart:
                product = item['product']
                qty = item['quantity']
                prod_stock = getattr(product, 'stock', None)
                if prod_stock is not None and qty > prod_stock:
                    insufficient.append((product, prod_stock, qty))

            if insufficient:
                # Notify user and redirect back to cart
                for prod, stock, requested in insufficient:
                    messages.error(request, f"Not enough stock for '{prod.name}': {stock} available, you requested {requested}.")
                return redirect('cart:cart_detail')

            # Everything ok, create order and decrement stock atomically
            with transaction.atomic():
                order = form.save()
                for item in cart:
                    product = item['product']
                    qty = item['quantity']
                    OrderItem.objects.create(order=order,
                                             product=product,
                                             price=item['price'],
                                             quantity=qty)
                    # decrement stock if field exists
                    if hasattr(product, 'stock'):
                        # reload product for latest value
                        product.refresh_from_db()
                        if product.stock is not None:
                            product.stock = max(0, product.stock - qty)
                            product.save()

            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})