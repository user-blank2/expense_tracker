from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Category, Expense
from .forms import ExpenseForm

def dashboard(request):
    expenses = Expense.objects.all().select_related('category')
    categories = Category.objects.all()

    total_spent = expenses.aggregate(
        Sum('amount'))['amount__sum'] or 0

    category_totals = []
    for category in categories:
        category_sum = category.expenses.aggregate(
            Sum('amount'))['amount__sum'] or 0
        category_totals.append({
            'category': category,
            'total': category_sum,
            'percentage': round((category_sum / total_spent * 100)
                if total_spent > 0 else 0)
        })

    context = {
        'expenses': expenses[:10],
        'category_totals': category_totals,
        'total_spent': total_spent,
    }
    return render(request, 'tracker/dashboard.html', context)


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request,'tracker/dashboard.html', {'form': form})

def edit_expense(request,pk):
    expense = get_object_or_404(Expense,pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form =ExpenseForm(instance = expense)
    return render(request,'tracker/edit_expense.html',{'form':form , 'expense':expense})
    
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})