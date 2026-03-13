from django.contrib import admin
from . models import Category,Expense
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name','icon','color')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
  list_display = ('title' , 'category' , 'amount' , 'date')
  list_filter = ('category', 'date')
