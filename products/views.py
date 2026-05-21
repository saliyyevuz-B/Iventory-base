from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from suppliers.models import Supplier

@login_required(login_url='login')
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/list.html', {'products': products})

@login_required(login_url='login')
def product_create(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST.get('name'),
            sku=request.POST.get('sku'),
            category=request.POST.get('category'),
            supplier_id=request.POST.get('supplier'),
            price=request.POST.get('price'),
            min_stock=request.POST.get('min_stock'),
        )
        return redirect('product_list')
    return render(request, 'products/form.html', {'suppliers': suppliers})

@login_required(login_url='login')
def product_edit(request, pk):
    if request.user.role != 'admin':
        return redirect('dashboard')
    product = get_object_or_404(Product, pk=pk)
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.sku = request.POST.get('sku')
        product.category = request.POST.get('category')
        product.supplier_id = request.POST.get('supplier')
        product.price = request.POST.get('price')
        product.min_stock = request.POST.get('min_stock')
        product.save()
        return redirect('product_list')
    return render(request, 'products/form.html', {'suppliers': suppliers, 'product': product})

@login_required(login_url='login')
def product_delete(request, pk):
    if request.user.role != 'admin':
        return redirect('dashboard')
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')

@login_required(login_url='login')
def low_stock(request):
    from django.db.models import F
    products = Product.objects.filter(stock__lte=F('min_stock'))
    return render(request, 'products/low_stock.html', {'products': products})