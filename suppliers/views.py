from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Supplier

@login_required(login_url='login')
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('-created_at')
    return render(request, 'suppliers/list.html', {'suppliers': suppliers})

@login_required(login_url='login')
def supplier_create(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    if request.method == 'POST':
        Supplier.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            company=request.POST.get('company'),
            address=request.POST.get('address', ''),
        )
        return redirect('supplier_list')
    return render(request, 'suppliers/form.html')

@login_required(login_url='login')
def supplier_delete(request, pk):
    if request.user.role != 'admin':
        return redirect('dashboard')
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('supplier_list')