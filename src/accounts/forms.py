from django.forms import ModelForm
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    """create a form to create an order"""
    class Meta:
        model = Order
        fields = '__all__'


class UserRegisterForm(UserCreationForm):
    """create a form to handle user registeration"""
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
