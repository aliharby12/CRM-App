from django.shortcuts import render


def home(request):
    """return the dashboard templates"""
    return render(request, 'accounts/dashboard.html')

def products(request):
    """return the products templates"""
    return render(request, 'accounts/products.html')
    
def customer(request):
    """return the customer templates"""
    return render(request, 'accounts/customer.html')
