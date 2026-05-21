"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from products.api_views import ProductViewSet
from suppliers.api_views import SupplierViewSet
from stock.api_views import StockInViewSet, StockOutViewSet
from accounts.api_views import RegisterAPIView, LoginAPIView

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'stock-in', StockInViewSet)
router.register(r'stock-out', StockOutViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('products/', include('products.urls')),
    path('', include('stock.urls')),

    # API
    path('api/', include(router.urls)),
    path('api/auth/register/', RegisterAPIView.as_view()),
    path('api/auth/login/', LoginAPIView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)