from django import forms
from .models import Expense,Category

class ExpenseForm(forms.ModelForm):
  class Meta:
    model = Expense
    fields = ['title','amount','date','category','notes']

    widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class CategoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ['name','color','icon']