"""
Testes Unitários para Models
Testam a lógica de negócio dos modelos isoladamente
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from shop.models import Category, Product
from orders.models import Order, OrderItem
from account.models import Profile

User = get_user_model()


class CategoryModelTest(TestCase):
    """Testes para o modelo Category"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Suplementos',
            slug='suplementos'
        )
    
    def test_category_creation(self):
        """Testa se a categoria é criada corretamente"""
        self.assertEqual(self.category.name, 'Suplementos')
        self.assertEqual(self.category.slug, 'suplementos')
    
    def test_category_str_representation(self):
        """Testa a representação string da categoria"""
        self.assertEqual(str(self.category), 'Suplementos')
    
    def test_category_get_absolute_url(self):
        """Testa se a URL da categoria é gerada corretamente"""
        expected_url = f'/categoria/suplementos/'
        self.assertEqual(self.category.get_absolute_url(), expected_url)


class ProductModelTest(TestCase):
    """Testes para o modelo Product"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Proteínas',
            slug='proteinas'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Whey Protein',
            slug='whey-protein',
            description='Proteína de alta qualidade',
            price=Decimal('99.90'),
            available=True,
            stock=50
        )
    
    def test_product_creation(self):
        """Testa se o produto é criado corretamente"""
        self.assertEqual(self.product.name, 'Whey Protein')
        self.assertEqual(self.product.price, Decimal('99.90'))
        self.assertEqual(self.product.stock, 50)
        self.assertTrue(self.product.available)
    
    def test_product_str_representation(self):
        """Testa a representação string do produto"""
        self.assertEqual(str(self.product), 'Whey Protein')
    
    def test_product_category_relationship(self):
        """Testa o relacionamento entre produto e categoria"""
        self.assertEqual(self.product.category, self.category)
        self.assertIn(self.product, self.category.products.all())
    
    def test_product_get_absolute_url(self):
        """Testa se a URL do produto é gerada corretamente"""
        expected_url = f'/produto/{self.product.id}/whey-protein/'
        self.assertEqual(self.product.get_absolute_url(), expected_url)


class OrderModelTest(TestCase):
    """Testes para o modelo Order"""
    
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
            name='Creatina',
            slug='creatina',
            price=Decimal('79.90'),
            available=True,
            stock=100
        )
        self.order = Order.objects.create(
            user=self.user,
            first_name='João',
            last_name='Silva',
            email='joao@example.com',
            phone='48999999999',
            address='Rua Teste, 123',
            postal_code='88000-000',
            city='Florianópolis',
            state='SC'
        )
    
    def test_order_creation(self):
        """Testa se o pedido é criado corretamente"""
        self.assertEqual(self.order.first_name, 'João')
        self.assertEqual(self.order.last_name, 'Silva')
        self.assertEqual(self.order.user, self.user)
        self.assertFalse(self.order.paid)
    
    def test_order_str_representation(self):
        """Testa a representação string do pedido"""
        self.assertEqual(str(self.order), f'Order {self.order.id}')
    
    def test_order_get_total_cost(self):
        """Testa o cálculo do custo total do pedido"""
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=2
        )
        expected_cost = Decimal('79.90') * 2
        self.assertEqual(self.order.get_total_cost(), expected_cost)
    
    def test_order_multiple_items_cost(self):
        """Testa o custo total com múltiplos itens"""
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal('79.90'),
            quantity=2
        )
        product2 = Product.objects.create(
            category=self.category,
            name='BCAA',
            slug='bcaa',
            price=Decimal('49.90'),
            available=True,
            stock=50
        )
        OrderItem.objects.create(
            order=self.order,
            product=product2,
            price=product2.price,
            quantity=1
        )
        expected_cost = (Decimal('79.90') * 2) + Decimal('49.90')
        self.assertEqual(self.order.get_total_cost(), expected_cost)


class OrderItemModelTest(TestCase):
    """Testes para o modelo OrderItem"""
    
    def setUp(self):
        self.category = Category.objects.create(name='Teste', slug='teste')
        self.product = Product.objects.create(
            category=self.category,
            name='Produto Teste',
            slug='produto-teste',
            price=Decimal('100.00'),
            available=True,
            stock=10
        )
        self.order = Order.objects.create(
            first_name='Test',
            last_name='User',
            email='test@test.com',
            phone='48999999999',
            address='Test St',
            postal_code='88000-000',
            city='Test City',
            state='SC'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=self.product.price,
            quantity=3
        )
    
    def test_order_item_creation(self):
        """Testa se o item do pedido é criado corretamente"""
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 3)
        self.assertEqual(self.order_item.price, Decimal('100.00'))
    
    def test_order_item_get_cost(self):
        """Testa o cálculo do custo do item"""
        expected_cost = Decimal('100.00') * 3
        self.assertEqual(self.order_item.get_cost(), expected_cost)


class ProfileModelTest(TestCase):
    """Testes para o modelo Profile"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='profileuser',
            email='profile@example.com',
            password='pass123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            cpf='123.456.789-00',
            phone='48987654321',
            postal_code='88010-000',
            address='Av. Principal',
            address_number='100',
            city='Florianópolis',
            state='SC'
        )
    
    def test_profile_creation(self):
        """Testa se o perfil é criado corretamente"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.cpf, '123.456.789-00')
        self.assertEqual(self.profile.city, 'Florianópolis')
    
    def test_profile_str_representation(self):
        """Testa a representação string do perfil"""
        expected = f'Profile of {self.user.username}'
        self.assertEqual(str(self.profile), expected)
    
    def test_profile_one_to_one_relationship(self):
        """Testa o relacionamento OneToOne com User"""
        self.assertEqual(self.user.profile, self.profile)
