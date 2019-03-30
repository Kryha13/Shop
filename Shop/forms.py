
from imagekit import ImageSpec, register
from pilkit.processors import ResizeToFill

from Shop.models import Product, Order
from django import forms


class AddProductForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput)
    producer = forms.CharField(widget = forms.TextInput)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Product
        fields = ['name', 'producer', 'description', 'price', 'image']


quantity_choices = [(i, str(i)) for i in range(1, 10)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=quantity_choices,
                                      coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['products']

