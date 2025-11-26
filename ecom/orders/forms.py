from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'postal_code',
                  'address', 'city', 'state']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'phone': 'Telefone',
            'address': 'Endereço completo',
            'postal_code': 'CEP',
            'city': 'Cidade',
            'state': 'Estado (UF)',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00000-000'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua, número, complemento'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da cidade'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SC', 'maxlength': '2'}),
        }