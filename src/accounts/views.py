from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, UserRegisterForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

@login_required(login_url='login')
@admin_only
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

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    """return the products templates"""
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def customer(request, id):
    """return the customer detail"""
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer':customer, 'orders':orders, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
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

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, id):
    """create a function to delete specific order"""
    order = Order.objects.get(id=id)
    if request.method == "POST":
    	order.delete()
    	return redirect('/')

    context = {'order':order}
    return render(request, 'accounts/delete.html', context)

@unauthenticated_user
def userRegister(request):
    """user registration view"""
    form = UserRegisterForm()

    # check the method
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            # import the username to use it in the message
            user = form.cleaned_data.get('username')
            messages.success(request, 'User Was Created Successfully !, welcome, ' + user)
            return redirect('login')
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def userLogin(request):
    """user login view"""
    if request.method == 'POST':

        # grab the username and password for this user from database
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check the authentications of user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'congratulations, you are now logged in !')
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or password are incorrect')
    return render(request, 'accounts/login.html', {})

def userLogout(request):
    """user logout view"""
    logout(request)
    messages.success(request, 'now, you are logged out !')
    return redirect('login')

def userPage(request):
    """create a user page to render user information"""
    context = {}
    return render(request, 'accounts/user.html', context)
