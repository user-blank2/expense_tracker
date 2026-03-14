from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Category, Expense
from .forms import ExpenseForm, CategoryForm

def dashboard(request):
    category_id = request.GET.get('category', '')
    search = request.GET.get('search', '')
    active_category = None

    categories = Category.objects.all()

    # Global total always uses ALL expenses
    all_expenses = Expense.objects.all()
    global_total = all_expenses.aggregate(
        Sum('amount'))['amount__sum'] or 0

    # Filtered expenses for the recent list
    expenses = Expense.objects.all().select_related('category')
    if category_id:
        expenses = expenses.filter(category_id=category_id)
        try:
            active_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            active_category = None
    if search:
        expenses = expenses.filter(
            title__icontains=search
        ) | expenses.filter(
            notes__icontains=search
        )

    total_spent = expenses.aggregate(
        Sum('amount'))['amount__sum'] or 0

    # Category totals always based on global total
    category_totals = []
    for category in categories:
        category_sum = category.expenses.aggregate(
            Sum('amount'))['amount__sum'] or 0
        category_totals.append({
            'category': category,
            'total': category_sum,
            'percentage': round((category_sum / global_total * 100)
                if global_total > 0 else 0)
        })

    context = {
        'expenses': expenses[:10],
        'category_totals': category_totals,
        'total_spent': total_spent,
        'global_total': global_total,
        'categories': categories,
        'active_category': active_category,
        'search': search,
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

    return render(request,'tracker/add_expense.html', {'form': form})

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

def add_category(request):
    if request.method == 'POST':
        category = CategoryForm(request.POST)
        if category.is_valid():
            category.save()
            return redirect('dashboard')
    else:
        category = CategoryForm()

    return render(request,'tracker/add_category.html',{'form':category})

def expense_detail(request, pk):
    expense = get_object_or_404(Expense,pk=pk)
    return render(request,'tracker/expense_detail.html',{'expense':expense})
    

