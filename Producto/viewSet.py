from rest_framework import viewsets

from Producto.models import Productos
from Producto.serializer import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductoSerializer