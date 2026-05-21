from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StockIn, StockOut
from products.models import Product
from suppliers.models import Supplier

@login_required(login_url='login')
def stockin_list(request):
    stockins = StockIn.objects.all().order_by('-created_at')
    return render(request, 'stock/stockin_list.html', {'stockins': stockins})

@login_required(login_url='login')
def stockin_create(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    products = Product.objects.all()
    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        product = Product.objects.get(pk=request.POST.get('product'))
        stockin = StockIn(
            product=product,
            supplier_id=request.POST.get('supplier'),
            quantity=int(float(request.POST.get('quantity'))),
            purchase_price=request.POST.get('purchase_price'),
        )
        stockin.save()
        return redirect('stockin_list')
    return render(request, 'stock/stockin_form.html', {
        'products': products,
        'suppliers': suppliers,
    })

@login_required(login_url='login')
def stockout_list(request):
    stockouts = StockOut.objects.all().order_by('-created_at')
    return render(request, 'stock/stockout_list.html', {'stockouts': stockouts})

@login_required(login_url='login')
def stockout_create(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    products = Product.objects.all()
    error = None
    if request.method == 'POST':
        product = Product.objects.get(pk=request.POST.get('product'))
        quantity = int(float(request.POST.get('quantity')))
        customer_name = request.POST.get('customer_name')
        if quantity > product.stock:
            error = f"Omborda faqat {product.stock} dona bor!"
        else:
            StockOut(
                product=product,
                quantity=quantity,
                customer_name=customer_name,
            ).save()
            return redirect('stockout_list')
    return render(request, 'stock/stockout_form.html', {
        'products': products,
        'error': error,
    })