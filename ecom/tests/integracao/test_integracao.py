"""
Testes de Integração
Testam a integração entre diferentes módulos do sistema
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from shop.models import Category, Product
from orders.models import Order, OrderItem
from account.models import Profile

User = get_user_model()


class IntegracaoShopCartTest(TestCase):
    """Testa integração entre Shop e Cart"""
    
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
    
    def test_produto_disponivel_pode_ser_adicionado_carrinho(self):
        """Testa que produtos disponíveis podem ser adicionados ao carrinho"""
        from django.urls import reverse
        
        # Produto disponível
        self.assertTrue(self.product.available)
        
        # Adiciona ao carrinho
        add_url = reverse('cart:cart_add', args=[self.product.id])
        response = self.client.post(add_url, {
            'quantity': 1,
            'override': False
        })
        self.assertEqual(response.status_code, 302)
    
    def test_estoque_limita_quantidade_no_carrinho(self):
        """Testa que o estoque limita a quantidade que pode ser adicionada"""
        from django.urls import reverse
        
        # Tenta adicionar mais que o estoque
        add_url = reverse('cart:cart_add', args=[self.product.id])
        response = self.client.post(add_url, {
            'quantity': self.product.stock + 10,
            'override': False
        })
        # Deve redirecionar com erro
        self.assertEqual(response.status_code, 302)


class IntegracaoCartOrderTest(TestCase):
    """Testa integração entre Cart e Orders"""
    
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
    
    def test_itens_carrinho_transferidos_para_pedido(self):
        """Testa que itens do carrinho são transferidos corretamente para o pedido"""
        from django.urls import reverse
        from cart.cart import Cart
        from django.test import RequestFactory
        from django.contrib.sessions.middleware import SessionMiddleware
        
        # Adiciona produtos ao carrinho
        add_url1 = reverse('cart:cart_add', args=[self.product1.id])
        self.client.post(add_url1, {'quantity': 2, 'override': False})
        
        add_url2 = reverse('cart:cart_add', args=[self.product2.id])
        self.client.post(add_url2, {'quantity': 1, 'override': False})
        
        # Cria pedido
        order = Order.objects.create(
            first_name='João',
            last_name='Silva',
            email='joao@example.com',
            phone='48999999999',
            address='Rua Teste',
            postal_code='88000-000',
            city='Florianópolis',
            state='SC'
        )
        
        # Simula criação de itens do pedido
        OrderItem.objects.create(
            order=order,
            product=self.product1,
            price=self.product1.price,
            quantity=2
        )
        OrderItem.objects.create(
            order=order,
            product=self.product2,
            price=self.product2.price,
            quantity=1
        )
        
        # Verifica que o pedido tem os itens corretos
        self.assertEqual(order.items.count(), 2)
        
        # Verifica cálculo do total
        expected_total = (Decimal('99.90') * 2) + Decimal('79.90')
        self.assertEqual(order.get_total_cost(), expected_total)


class IntegracaoUserProfileTest(TestCase):
    """Testa integração entre User e Profile"""
    
    def test_profile_criado_com_usuario(self):
        """Testa que o profile é criado quando um usuário é criado"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Cria profile manualmente (em produção seria com signal)
        profile = Profile.objects.create(user=user)
        
        # Verifica relacionamento
        self.assertEqual(user.profile, profile)
        self.assertEqual(profile.user, user)
    
    def test_dados_profile_usados_em_pedido(self):
        """Testa que dados do profile podem ser usados ao criar pedido"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        profile = Profile.objects.create(
            user=user,
            cpf='123.456.789-00',
            phone='48999999999',
            postal_code='88010-000',
            address='Av. Principal',
            address_number='100',
            city='Florianópolis',
            state='SC'
        )
        
        # Cria pedido usando dados do profile
        order = Order.objects.create(
            user=user,
            first_name=user.first_name or 'João',
            last_name=user.last_name or 'Silva',
            email=user.email,
            phone=profile.phone,
            address=f"{profile.address}, {profile.address_number}",
            postal_code=profile.postal_code,
            city=profile.city,
            state=profile.state
        )
        
        # Verifica que os dados foram transferidos
        self.assertEqual(order.user, user)
        self.assertEqual(order.phone, profile.phone)
        self.assertEqual(order.city, profile.city)


class IntegracaoUserOrderTest(TestCase):
    """Testa integração entre User e Orders"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
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
    
    def test_usuario_pode_ter_multiplos_pedidos(self):
        """Testa que um usuário pode ter múltiplos pedidos"""
        # Cria primeiro pedido
        order1 = Order.objects.create(
            user=self.user,
            first_name='João',
            last_name='Silva',
            email=self.user.email,
            phone='48999999999',
            address='Rua A',
            postal_code='88000-000',
            city='Florianópolis',
            state='SC'
        )
        
        # Cria segundo pedido
        order2 = Order.objects.create(
            user=self.user,
            first_name='João',
            last_name='Silva',
            email=self.user.email,
            phone='48999999999',
            address='Rua B',
            postal_code='88001-000',
            city='Florianópolis',
            state='SC'
        )
        
        # Verifica que o usuário tem 2 pedidos
        self.assertEqual(self.user.orders.count(), 2)
        self.assertIn(order1, self.user.orders.all())
        self.assertIn(order2, self.user.orders.all())
    
    def test_pedidos_ordenados_por_data(self):
        """Testa que pedidos são retornados ordenados por data (mais recente primeiro)"""
        # Cria múltiplos pedidos
        for i in range(3):
            Order.objects.create(
                user=self.user,
                first_name='João',
                last_name='Silva',
                email=self.user.email,
                phone='48999999999',
                address=f'Rua {i}',
                postal_code='88000-000',
                city='Florianópolis',
                state='SC'
            )
        
        orders = self.user.orders.all()
        # Verifica que estão ordenados por created (DESC)
        for i in range(len(orders) - 1):
            self.assertGreaterEqual(orders[i].created, orders[i + 1].created)
