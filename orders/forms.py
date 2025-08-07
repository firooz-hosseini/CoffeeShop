from django import forms
from .models import OrderItem, Comment

class CreateOrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add your comment...'}),
        }