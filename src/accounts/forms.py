from django.forms import ModelForm
from .models import Order

class OrderForm(ModelForm):
    """create a form to create an order"""
    class Meta:
        model = Order
        fields = '__all__'
