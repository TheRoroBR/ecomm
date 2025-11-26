"""
Testes Unitários para o Carrinho de Compras
Testam a lógica do carrinho isoladamente
"""
from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from shop.models import Category, Product
from cart.cart import Cart


class CartTest(TestCase):
    """Testes para a classe Cart"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(
            name='Suplementos',
            slug='suplementos'
        )
        self.product1 = Product.objects.create(
            category=self.category,
            name='Whey Protein',
            slug='whey-protein',
            price=Decimal('99.90'),
            available=True,
            stock=50
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name='Creatina',
            slug='creatina',
            price=Decimal('79.90'),
            available=True,
            stock=30
        )
    
    def _get_request_with_session(self):
        """Helper para criar request com sessão"""
        request = self.factory.get('/')
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        return request
    
    def test_cart_initialization(self):
        """Testa se o carrinho é inicializado corretamente"""
        request = self._get_request_with_session()
        cart = Cart(request)
        self.assertIsNotNone(cart.cart)
        self.assertEqual(len(cart), 0)
    
    def test_add_product_to_cart(self):
        """Testa adicionar um produto ao carrinho"""
        request = self._get_request_with_session()
        cart = Cart(request)
        cart.add(self.product1, quantity=2)
        
        self.assertEqual(len(cart), 2)
        self.assertIn(str(self.product1.id), cart.cart)
    
    def test_add_multiple_products(self):
        """Testa adicionar múltiplos produtos diferentes"""
        request = self._get_request_with_session()
        cart = Cart(request)
        
        cart.add(self.product1, quantity=2)
        cart.add(self.product2, quantity=3)
        
        self.assertEqual(len(cart), 5)
        self.assertEqual(len(cart.cart), 2)
    
    def test_update_product_quantity(self):
        """Testa atualizar a quantidade de um produto"""
        request = self._get_request_with_session()
        cart = Cart(request)
        
        cart.add(self.product1, quantity=2)
        cart.add(self.product1, quantity=3, override_quantity=True)
        
        self.assertEqual(len(cart), 3)
        self.assertEqual(cart.cart[str(self.product1.id)]['quantity'], 3)
    
    def test_increment_existing_product(self):
        """Testa incrementar quantidade de produto existente"""
        request = self._get_request_with_session()
        cart = Cart(request)
        
        cart.add(self.product1, quantity=2)
        cart.add(self.product1, quantity=1)
        
        self.assertEqual(len(cart), 3)
        self.assertEqual(cart.cart[str(self.product1.id)]['quantity'], 3)
    
    def test_remove_product_from_cart(self):
        """Testa remover um produto do carrinho"""
        request = self._get_request_with_session()
        cart = Cart(request)
        
        cart.add(self.product1, quantity=2)
        cart.add(self.product2, quantity=1)
        self.assertEqual(len(cart), 3)
        
        cart.remove(self.product1)
        self.assertEqual(len(cart), 1)
        self.assertNotIn(str(self.product1.id), cart.cart)
    
    def test_get_total_price(self):
        """Testa o cálculo do preço total do carrinho"""
        request = self._get_request_with_session()
        cart = Cart(request)
        
        cart.add(self.product1, quantity=2)
        cart.add(self.product2, quantity=1)
        
        expected_total = (Decimal('99.90') * 2) + Decimal('79.90')
        self.assertEqual(cart.get_total_price(), expected_total)
    
    def test_clear_cart(self):
        """Testa limpar o carrinho completamente"""
        request = self._get_request_with_session()
        cart = Cart(request)
        
        cart.add(self.product1, quantity=2)
        cart.add(self.product2, quantity=3)
        self.assertEqual(len(cart), 5)
        
        cart.clear()
        # Após clear, precisa criar nova instância do carrinho para verificar
        cart = Cart(request)
        self.assertEqual(len(cart), 0)
    
    def test_cart_iteration(self):
        """Testa a iteração sobre os itens do carrinho"""
        request = self._get_request_with_session()
        cart = Cart(request)
        
        cart.add(self.product1, quantity=2)
        cart.add(self.product2, quantity=1)
        
        items = list(cart)
        self.assertEqual(len(items), 2)
        
        # Verifica se os itens têm as chaves necessárias
        for item in items:
            self.assertIn('product', item)
            self.assertIn('quantity', item)
            self.assertIn('price', item)
            self.assertIn('total_price', item)
    
    def test_cart_item_total_price(self):
        """Testa o cálculo do preço total de cada item"""
        request = self._get_request_with_session()
        cart = Cart(request)
        
        cart.add(self.product1, quantity=3)
        
        items = list(cart)
        item = items[0]
        
        expected_total = Decimal('99.90') * 3
        self.assertEqual(item['total_price'], expected_total)
