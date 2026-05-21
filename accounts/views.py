from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import F
from .form import RegisterForm, LoginForm

def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'client'
            user.save()
            return redirect('login')
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Username yoki parol xato!')
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard_view(request):
    from products.models import Product
    from suppliers.models import Supplier
    from stock.models import StockIn, StockOut

    today = timezone.now().date()

    context = {
        'total_products': Product.objects.count(),
        'total_suppliers': Supplier.objects.count(),
        'today_stockin': StockIn.objects.filter(created_at__date=today).count(),
        'today_stockout': StockOut.objects.filter(created_at__date=today).count(),
        'low_stock_products': Product.objects.filter(stock__lte=F('min_stock')),
    }
    return render(request, 'dashboard.html', context)



@login_required(login_url='login')
def stats_view(request):
    from products.models import Product
    from suppliers.models import Supplier
    from stock.models import StockIn, StockOut
    from django.db.models import Sum
    from datetime import timedelta

    today = timezone.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    stockin_data = []
    stockout_data = []
    for day in last_7_days:
        stockin_data.append(
            StockIn.objects.filter(created_at__date=day).aggregate(
                total=Sum('quantity'))['total'] or 0
        )
        stockout_data.append(
            StockOut.objects.filter(created_at__date=day).aggregate(
                total=Sum('quantity'))['total'] or 0
        )

    labels = [str(day.strftime('%d-%b')) for day in last_7_days]

    top_products = StockOut.objects.values('product__name').annotate(
        total=Sum('quantity')).order_by('-total')[:5]

    top_suppliers = StockIn.objects.values('supplier__name').annotate(
        total=Sum('quantity')).order_by('-total')[:5]

    context = {
        'labels': labels,
        'stockin_data': stockin_data,
        'stockout_data': stockout_data,
        'top_products': top_products,
        'top_suppliers': top_suppliers,
    }
    return render(request, 'stats.html', context)