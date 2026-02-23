from django import forms

from .models import Category, Tag


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
