from rest_framework import viewsets, permissions
from .models import StockIn, StockOut
from .serializers import StockInSerializer, StockOutSerializer

class StockInViewSet(viewsets.ModelViewSet):
    queryset = StockIn.objects.all()
    serializer_class = StockInSerializer
    permission_classes = [permissions.IsAuthenticated]

class StockOutViewSet(viewsets.ModelViewSet):
    queryset = StockOut.objects.all()
    serializer_class = StockOutSerializer
    permission_classes = [permissions.IsAuthenticated]