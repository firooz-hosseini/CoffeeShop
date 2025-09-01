from django import forms

from .models import Comment, CartItem


class CreateCartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add your comment...'}),
        }