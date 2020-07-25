from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('products', views.products, name='products'),
    path('customer', views.customer, name='customer'),
    path('customer/<str:id>', views.customer, name='customer'),
    path('create-order', views.createOrder, name='create-order'),
    path('update-order/<str:id>/', views.updateOrder, name="update-order"),

]
