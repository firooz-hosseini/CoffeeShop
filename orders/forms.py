from django import forms
from .models import OrderItem

class CreateOrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']




