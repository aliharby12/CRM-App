from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory
from .filters import OrderFilter

def home(request):
    """return the dashboard templates"""
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    out_of_delivery = orders.filter(status='Out of delivery').count()

    context = {
        'orders':orders,
        'customers':customers,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'out_of_delivery':out_of_delivery
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
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer, 'orders':orders, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

def createOrder(request, id):
    """create a view to order create"""
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
    customer = Customer.objects.get(id=id)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
    	formset = OrderFormSet(request.POST, instance=customer)
    	if formset.is_valid():
    		formset.save()
    		return redirect('/')

    context = {'form':formset}
    return render(request, 'accounts/order_form.html', context)


def updateOrder(request, id):
    """create a function to edit specific order"""
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    if request.method == 'POST':
    	form = OrderForm(request.POST, instance=order)
    	if form.is_valid():
    		form.save()
    		return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, id):
    """create a function to delete specific order"""
    order = Order.objects.get(id=id)
    if request.method == "POST":
    	order.delete()
    	return redirect('/')

    context = {'order':order}
    return render(request, 'accounts/delete.html', context)
