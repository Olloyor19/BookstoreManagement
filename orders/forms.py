from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_type', 'quantity']
        widgets = {
            'order_type': forms.RadioSelect(),
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }