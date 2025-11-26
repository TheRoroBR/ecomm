"""
Testes Funcionais para Views
Testam o comportamento completo das views incluindo requisições e respostas
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import Category, Product
from orders.models import Order

User = get_user_model()


class ShopViewsTest(TestCase):
    """Testes para as views da loja"""
    
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Suplementos',
            slug='suplementos'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Whey Protein',
            slug='whey-protein',
            price=Decimal('99.90'),
            available=True,
            stock=50
        )
    
    def test_homepage_view(self):
        """Testa se a homepage carrega corretamente"""
        response = self.client.get(reverse('shop:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/homepage.html')
    
    def test_product_list_view(self):
        """Testa a listagem de produtos"""
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertContains(response, self.product.name)
    
    def test_product_list_by_category(self):
        """Testa listagem de produtos por categoria"""
        url = reverse('shop:product_list_by_category', args=[self.category.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
    
    def test_product_detail_view(self):
        """Testa a página de detalhes do produto"""
        url = reverse('shop:product_detail', args=[self.product.id, self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/detail.html')
        self.assertContains(response, self.product.name)
        # Preço é formatado como R$ 99,90 no template
        self.assertContains(response, 'R$ 99,90')
    
    def test_product_not_available(self):
        """Testa que produtos indisponíveis retornam 404"""
        self.product.available = False
        self.product.save()
        
        url = reverse('shop:product_detail', args=[self.product.id, self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_sobre_view(self):
        """Testa a página sobre"""
        response = self.client.get(reverse('shop:sobre'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/sobre.html')
    
    def test_privacidade_view(self):
        """Testa a página de privacidade"""
        response = self.client.get(reverse('shop:privacidade'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/privacidade.html')
    
    def test_termos_view(self):
        """Testa a página de termos"""
        response = self.client.get(reverse('shop:termos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/termos.html')


class CartViewsTest(TestCase):
    """Testes para as views do carrinho"""
    
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Suplementos',
            slug='suplementos'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Creatina',
            slug='creatina',
            price=Decimal('79.90'),
            available=True,
            stock=100
        )
    
    def test_cart_detail_view(self):
        """Testa a página de detalhes do carrinho"""
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
    
    def test_add_product_to_cart(self):
        """Testa adicionar produto ao carrinho via POST"""
        url = reverse('cart:cart_add', args=[self.product.id])
        response = self.client.post(url, {
            'quantity': 2,
            'override': False
        })
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_add_product_exceeding_stock(self):
        """Testa adicionar quantidade maior que o estoque"""
        url = reverse('cart:cart_add', args=[self.product.id])
        response = self.client.post(url, {
            'quantity': 150,  # Estoque é 100
            'override': False
        })
        # Deve redirecionar com mensagem de erro
        self.assertEqual(response.status_code, 302)
    
    def test_remove_product_from_cart(self):
        """Testa remover produto do carrinho"""
        # Primeiro adiciona
        add_url = reverse('cart:cart_add', args=[self.product.id])
        self.client.post(add_url, {'quantity': 1, 'override': False})
        
        # Depois remove
        remove_url = reverse('cart:cart_remove', args=[self.product.id])
        response = self.client.post(remove_url)
        self.assertEqual(response.status_code, 302)
    
    def test_cart_ajax_add(self):
        """Testa adição de produto via AJAX"""
        url = reverse('cart:cart_add', args=[self.product.id])
        response = self.client.post(
            url,
            {'quantity': 2, 'override': False},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_total_items'], 2)
    
    def test_cart_ajax_remove(self):
        """Testa remoção de produto via AJAX"""
        # Adiciona primeiro
        add_url = reverse('cart:cart_add', args=[self.product.id])
        self.client.post(add_url, {'quantity': 1, 'override': False})
        
        # Remove via AJAX
        remove_url = reverse('cart:cart_remove', args=[self.product.id])
        response = self.client.post(
            remove_url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_total_items'], 0)


class AccountViewsTest(TestCase):
    """Testes para as views de conta de usuário"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_register_view_get(self):
        """Testa acesso à página de registro"""
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')
    
    def test_login_view(self):
        """Testa a página de login"""
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
    
    def test_user_login(self):
        """Testa login de usuário"""
        response = self.client.post(reverse('account:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        # Verifica se foi redirecionado após login
        self.assertEqual(response.status_code, 302)
    
    def test_dashboard_requires_login(self):
        """Testa que o dashboard requer autenticação"""
        response = self.client.get(reverse('account:dashboard'))
        # Deve redirecionar para login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/account/login/', response.url)
    
    def test_dashboard_authenticated_user(self):
        """Testa acesso ao dashboard com usuário autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/dashboard.html')


class OrderViewsTest(TestCase):
    """Testes para as views de pedidos"""
    
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Suplementos',
            slug='suplementos'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='BCAA',
            slug='bcaa',
            price=Decimal('49.90'),
            available=True,
            stock=50
        )
    
    def test_order_create_view_empty_cart(self):
        """Testa criar pedido com carrinho vazio"""
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)
    
    def test_order_create_with_items(self):
        """Testa criar pedido com itens no carrinho"""
        # Adiciona item ao carrinho
        add_url = reverse('cart:cart_add', args=[self.product.id])
        self.client.post(add_url, {'quantity': 2, 'override': False})
        
        # Acessa página de criar pedido
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order/create.html')
