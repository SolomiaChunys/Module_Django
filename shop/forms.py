from django import forms
from django.core.exceptions import ValidationError
from .models import User, Product, Order, Return
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Enter Email',
                             }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Username',
            }),
        }


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'count')

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price < 0:
            raise ValidationError('The price can`t be negative!')
        return price

