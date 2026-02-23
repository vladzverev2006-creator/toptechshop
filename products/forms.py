from django import forms

from .models import Product, ProductAttribute, ProductVersion


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'status', 'category', 'tags', 'license', 'cover']


class ProductVersionForm(forms.ModelForm):
    class Meta:
        model = ProductVersion
        fields = ['version', 'changelog']


class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ['key', 'value']
