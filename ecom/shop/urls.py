from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('produtos/', views.product_list, name='product_list'),
    path('categoria/', views.product_list, name='product_list_category'),
    path('categoria/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('produto/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('sobre/', views.sobre, name='sobre'),
    path('privacidade/', views.privacidade, name='privacidade'),
    path('termos/', views.termos, name='termos'),
]