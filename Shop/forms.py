from Shop.models import Product
from django import forms


class AddProductForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput)
    producer = forms.CharField(widget = forms.TextInput)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Product
        fields = ['name', 'producer', 'description', 'price', 'image']
