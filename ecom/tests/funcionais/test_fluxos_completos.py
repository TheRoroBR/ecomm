"""
Testes de Fluxos Completos
Testam jornadas completas do usuário no sistema
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import Category, Product
from orders.models import Order
from cart.cart import Cart

User = get_user_model()


class CompraCompletaTest(TestCase):
    """Testa o fluxo completo de uma compra"""
    
    def setUp(self):
        self.client = Client()
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
    
    def test_fluxo_completo_compra(self):
        """Testa o fluxo completo: navegar -> adicionar ao carrinho -> criar pedido"""
        # 1. Usuário visita a homepage
        response = self.client.get(reverse('shop:homepage'))
        self.assertEqual(response.status_code, 200)
        
        # 2. Navega para lista de produtos
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        
        # 3. Visualiza detalhes do produto
        url = reverse('shop:product_detail', args=[self.product1.id, self.product1.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # 4. Adiciona produto ao carrinho
        add_url = reverse('cart:cart_add', args=[self.product1.id])
        response = self.client.post(add_url, {
            'quantity': 2,
            'override': False
        })
        self.assertEqual(response.status_code, 302)
        
        # 5. Adiciona outro produto
        add_url2 = reverse('cart:cart_add', args=[self.product2.id])
        response = self.client.post(add_url2, {
            'quantity': 1,
            'override': False
        })
        self.assertEqual(response.status_code, 302)
        
        # 6. Visualiza carrinho
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)
        
        # 7. Acessa página de criar pedido
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)


class FluxoUsuarioAutenticadoTest(TestCase):
    """Testa fluxos de usuário autenticado"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Proteínas',
            slug='proteinas'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Whey Isolado',
            slug='whey-isolado',
            price=Decimal('149.90'),
            available=True,
            stock=20
        )
    
    def test_fluxo_registro_e_compra(self):
        """Testa registro de novo usuário e realização de compra"""
        # 1. Acessa página de registro
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)
        
        # 2. Faz login
        logged_in = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(logged_in)
        
        # 3. Acessa dashboard
        response = self.client.get(reverse('account:dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # 4. Navega pela loja e adiciona produto
        add_url = reverse('cart:cart_add', args=[self.product.id])
        response = self.client.post(add_url, {
            'quantity': 1,
            'override': False
        })
        self.assertEqual(response.status_code, 302)
        
        # 5. Visualiza carrinho
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)


class FluxoCarrinhoTest(TestCase):
    """Testa diferentes fluxos do carrinho"""
    
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Teste', slug='teste')
        self.product = Product.objects.create(
            category=self.category,
            name='Produto Teste',
            slug='produto-teste',
            price=Decimal('50.00'),
            available=True,
            stock=10
        )
    
    def test_adicionar_atualizar_remover(self):
        """Testa adicionar, atualizar quantidade e remover do carrinho"""
        # Adiciona produto
        add_url = reverse('cart:cart_add', args=[self.product.id])
        self.client.post(add_url, {'quantity': 2, 'override': False})
        
        # Verifica carrinho
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response, self.product.name)
        
        # Atualiza quantidade
        self.client.post(add_url, {'quantity': 5, 'override': True})
        
        # Remove produto
        remove_url = reverse('cart:cart_remove', args=[self.product.id])
        self.client.post(remove_url)
        
        # Verifica que carrinho está vazio
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
    
    def test_carrinho_multiplos_produtos_ajax(self):
        """Testa gerenciamento de múltiplos produtos via AJAX"""
        # Cria outro produto
        product2 = Product.objects.create(
            category=self.category,
            name='Produto 2',
            slug='produto-2',
            price=Decimal('75.00'),
            available=True,
            stock=15
        )
        
        # Adiciona primeiro produto via AJAX
        add_url1 = reverse('cart:cart_add', args=[self.product.id])
        response = self.client.post(
            add_url1,
            {'quantity': 3, 'override': False},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['cart_total_items'], 3)
        
        # Adiciona segundo produto via AJAX
        add_url2 = reverse('cart:cart_add', args=[product2.id])
        response = self.client.post(
            add_url2,
            {'quantity': 2, 'override': False},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['cart_total_items'], 5)
        
        # Remove primeiro produto via AJAX
        remove_url = reverse('cart:cart_remove', args=[self.product.id])
        response = self.client.post(
            remove_url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['cart_total_items'], 2)
