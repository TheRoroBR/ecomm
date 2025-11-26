"""
Testes Unitários para Formulários
Testam a validação e comportamento dos forms
"""
from django.test import TestCase
from cart.forms import CartAddProductForm
from orders.forms import OrderCreateForm


class CartAddProductFormTest(TestCase):
    """Testes para o formulário de adicionar produto ao carrinho"""
    
    def test_valid_form(self):
        """Testa formulário com dados válidos"""
        form_data = {'quantity': 5, 'override': False}
        form = CartAddProductForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_quantity_required(self):
        """Testa que quantidade é obrigatória"""
        form_data = {'override': False}
        form = CartAddProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)
    
    def test_quantity_min_value(self):
        """Testa valor mínimo da quantidade"""
        form_data = {'quantity': 0, 'override': False}
        form = CartAddProductForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_quantity_max_value(self):
        """Testa valor máximo da quantidade"""
        form_data = {'quantity': 1000, 'override': False}
        form = CartAddProductForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_override_default_false(self):
        """Testa que override tem valor padrão False"""
        form_data = {'quantity': 1}
        form = CartAddProductForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertFalse(form.cleaned_data['override'])


class OrderCreateFormTest(TestCase):
    """Testes para o formulário de criar pedido"""
    
    def test_valid_form(self):
        """Testa formulário com todos os dados válidos"""
        form_data = {
            'first_name': 'João',
            'last_name': 'Silva',
            'email': 'joao@example.com',
            'phone': '48999999999',
            'address': 'Rua Teste, 123',
            'postal_code': '88000-000',
            'city': 'Florianópolis',
            'state': 'SC'
        }
        form = OrderCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_required_fields(self):
        """Testa que campos obrigatórios são validados"""
        form = OrderCreateForm(data={})
        self.assertFalse(form.is_valid())
        
        required_fields = ['first_name', 'last_name', 'email', 'address', 
                          'postal_code', 'city']
        for field in required_fields:
            self.assertIn(field, form.errors)
    
    def test_email_validation(self):
        """Testa validação do campo email"""
        form_data = {
            'first_name': 'João',
            'last_name': 'Silva',
            'email': 'email_invalido',
            'phone': '48999999999',
            'address': 'Rua Teste',
            'postal_code': '88000-000',
            'city': 'Florianópolis',
            'state': 'SC'
        }
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
