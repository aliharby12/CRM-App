from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm

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

def createOrder(request):
    """create a view to order create"""
    form = OrderForm()
    if request.method == 'POST':
        """check the method of the request"""
        form = OrderForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')
    form = OrderForm()
    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)
