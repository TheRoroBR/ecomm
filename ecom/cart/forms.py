from django import forms


from django.conf import settings

# Default maximum quantity allowed per add-to-cart action.
# You can override this in your Django settings with CART_MAX_QUANTITY.
DEFAULT_CART_MAX_QTY = getattr(settings, 'CART_MAX_QUANTITY', 100)


class CartAddProductForm(forms.Form):
    # Use an integer field so the user can type or use the browser number
    # control. We set a sensible default max but allow overriding via
    # settings.py (CART_MAX_QUANTITY).
    quantity = forms.IntegerField(
        min_value=1,
        max_value=DEFAULT_CART_MAX_QTY,
        initial=1,
        widget=forms.NumberInput(attrs={
            'min': 1,
            'max': DEFAULT_CART_MAX_QTY,
            'class': 'quantity-input'
        })
    )

    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)