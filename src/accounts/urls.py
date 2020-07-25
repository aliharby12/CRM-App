from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('products', views.products, name='products'),
    path('customer', views.customer, name='customer'),
    path('customer/<int:id>/', views.customer, name='customer'),
    path('create-order/<int:id>/', views.createOrder, name='create-order'),
    path('update-order/<int:id>/', views.updateOrder, name='update-order'),
    path('delete-order/<int:id>/', views.deleteOrder, name='delete-order'),

]
