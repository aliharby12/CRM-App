from django.shortcuts import render
from .models import *

def home(request):
    """return the dashboard templates"""
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'customers':customers,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending
    }

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    """return the products templates"""
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

def customer(request, id):
    """return the customer detail"""
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    return render(request, 'accounts/customer.html', {'customer':customer, 'orders':orders})
