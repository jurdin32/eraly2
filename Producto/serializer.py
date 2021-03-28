
from rest_framework import serializers

from Empresa.serializer import EstablecimientoSerializer
from Producto.models import Productos


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = ['id','establecimiento','nombre', 'descripcion','hash',]

