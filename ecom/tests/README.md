# 🧪 Suite de Testes - E-commerce Saúde e Forma

## 📋 Visão Geral

Esta é a suite completa de testes do projeto E-commerce Saúde e Forma, organizada em diferentes categorias para garantir a qualidade e funcionalidade do sistema.

## 🗂️ Estrutura de Testes

```
tests/
├── unitarios/              # Testes Unitários
│   ├── test_models.py      # Testa modelos isoladamente
│   ├── test_cart.py        # Testa lógica do carrinho
│   └── test_forms.py       # Testa validação de formulários
│
├── funcionais/             # Testes Funcionais
│   ├── test_views.py       # Testa views e requisições HTTP
│   └── test_fluxos_completos.py  # Testa jornadas de usuário
│
└── integracao/             # Testes de Integração
    └── test_integracao.py  # Testa integração entre módulos
```

## 🎯 Tipos de Testes

### 1. Testes Unitários (`unitarios/`)

Testam componentes individuais isoladamente, sem dependências externas.

**Cobertura:**

- ✅ Models (Category, Product, Order, OrderItem, Profile)
- ✅ Classe Cart (adicionar, remover, atualizar, calcular totais)
- ✅ Formulários (CartAddProductForm, OrderCreateForm)

**Características:**

- Rápidos de executar
- Isolados (não dependem de banco de dados real)
- Testam lógica de negócio específica

### 2. Testes Funcionais (`funcionais/`)

Testam funcionalidades completas da aplicação, incluindo requisições HTTP e respostas.

**Cobertura:**

- ✅ Views da loja (homepage, lista de produtos, detalhes)
- ✅ Views do carrinho (adicionar, remover, atualizar via AJAX)
- ✅ Views de conta de usuário (registro, login, dashboard)
- ✅ Views de pedidos (criar pedido)
- ✅ Fluxos completos de compra
- ✅ Fluxos de usuário autenticado
- ✅ Fluxos do carrinho (AJAX e tradicional)

**Características:**

- Testam comportamento real da aplicação
- Simulam ações de usuários
- Verificam códigos de resposta HTTP
- Validam templates renderizados

### 3. Testes de Integração (`integracao/`)

Testam a integração entre diferentes módulos do sistema.

**Cobertura:**

- ✅ Integração Shop ↔ Cart (produtos disponíveis, controle de estoque)
- ✅ Integração Cart ↔ Orders (transferência de itens)
- ✅ Integração User ↔ Profile (relacionamento OneToOne)
- ✅ Integração User ↔ Orders (múltiplos pedidos por usuário)

**Características:**

- Testam comunicação entre módulos
- Verificam fluxo de dados
- Validam relacionamentos entre entidades

## 🚀 Como Executar os Testes

### Todos os testes

```powershell
cd ecom
python manage.py test tests
```

### Por categoria

```powershell
# Apenas testes unitários
python manage.py test tests.unitarios

# Apenas testes funcionais
python manage.py test tests.funcionais

# Apenas testes de integração
python manage.py test tests.integracao
```

### Teste específico

```powershell
# Testar um arquivo específico
python manage.py test tests.unitarios.test_models

# Testar uma classe específica
python manage.py test tests.unitarios.test_models.ProductModelTest

# Testar um método específico
python manage.py test tests.unitarios.test_models.ProductModelTest.test_product_creation
```

### Com cobertura de código

```powershell
# Instalar coverage
pip install coverage

# Executar testes com cobertura
coverage run --source='.' manage.py test tests

# Gerar relatório
coverage report

# Gerar relatório HTML
coverage html
# Abrir htmlcov/index.html no navegador
```

### Com verbosidade

```powershell
# Modo verboso (mostra cada teste executado)
python manage.py test tests --verbosity=2

# Modo muito verboso (debug)
python manage.py test tests --verbosity=3
```

## 📊 Estatísticas de Cobertura

### Testes Unitários

- **test_models.py**: 15 testes
  - 4 testes para Category
  - 4 testes para Product
  - 4 testes para Order
  - 2 testes para OrderItem
  - 3 testes para Profile

- **test_cart.py**: 11 testes
  - Inicialização do carrinho
  - Adicionar produtos
  - Atualizar quantidades
  - Remover produtos
  - Cálculos de totais
  - Iteração sobre itens

- **test_forms.py**: 7 testes
  - Validação de CartAddProductForm
  - Validação de OrderCreateForm

### Testes Funcionais

- **test_views.py**: 19 testes
  - 7 testes de ShopViews
  - 6 testes de CartViews
  - 4 testes de AccountViews
  - 2 testes de OrderViews

- **test_fluxos_completos.py**: 5 testes
  - Fluxo completo de compra
  - Fluxo de usuário autenticado
  - Fluxos do carrinho

### Testes de Integração

- **test_integracao.py**: 7 testes
  - Integração Shop-Cart
  - Integração Cart-Order
  - Integração User-Profile
  - Integração User-Order

**Total: 64 testes**

## 🎨 Convenções de Nomenclatura

- Classes de teste: `NomeDoComponenteTest`
- Métodos de teste: `test_descricao_do_comportamento`
- Fixtures: `setUp()` para cada classe de teste

## 🔍 Exemplos de Uso

### Verificar se produto está disponível

```python
def test_product_creation(self):
    self.assertTrue(self.product.available)
```

### Testar adição ao carrinho via AJAX

```python
def test_cart_ajax_add(self):
    response = self.client.post(
        url,
        {'quantity': 2, 'override': False},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    self.assertEqual(response.status_code, 200)
    data = response.json()
    self.assertTrue(data['success'])
```

### Testar fluxo completo

```python
def test_fluxo_completo_compra(self):
    # 1. Visitar homepage
    # 2. Ver lista de produtos
    # 3. Ver detalhes
    # 4. Adicionar ao carrinho
    # 5. Ver carrinho
    # 6. Criar pedido
```

## 🐛 Debugging de Testes

### Ver print statements nos testes

```powershell
python manage.py test tests --verbosity=2 --debug-mode
```

### Parar no primeiro erro

```powershell
python manage.py test tests --failfast
```

### Manter banco de dados após testes

```powershell
python manage.py test tests --keepdb
```

## 📝 Boas Práticas

1. ✅ **Sempre execute os testes antes de commit**
2. ✅ **Escreva testes para novos recursos**
3. ✅ **Mantenha testes isolados e independentes**
4. ✅ **Use nomes descritivos para os testes**
5. ✅ **Teste casos de sucesso e falha**
6. ✅ **Verifique edge cases**
7. ✅ **Mantenha setUp() limpo e organizado**

## 🔄 Integração Contínua

Estes testes podem ser integrados em pipelines de CI/CD:

```yaml
# Exemplo para GitHub Actions
- name: Run Tests
  run: |
    python manage.py test tests --verbosity=2
    
- name: Coverage Report
  run: |
    coverage run --source='.' manage.py test tests
    coverage report
```

## 📚 Recursos Adicionais

- [Django Testing Documentation](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

## 🤝 Contribuindo

Ao adicionar novos recursos:

1. Crie testes unitários para a lógica de negócio
2. Adicione testes funcionais para as views
3. Crie testes de integração se houver interação entre módulos
4. Atualize este README com as estatísticas de cobertura
