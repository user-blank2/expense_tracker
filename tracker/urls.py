from django.urls import path
from . import views

urlpatterns = [
  path('', views.dashboard,name = 'dashboard'),
  path('add/', views.add_expense, name = 'add_expense'),
  path('edit/<int:pk>/', views.edit_expense, name = 'edit_expense'),
  path('delete/<int:pk>/', views.delete_expense, name = 'delete_expense'),
  path('categories/add/',views.add_category,name = 'add_category'),
  path('expense/<int:pk>/', views.expense_detail, name = 'expense_detail'),
]