from rest_framework import viewsets

from Empresa.models import Establecimiento
from Empresa.serializer import EstablecimientoSerializer


class EstablecimientoViewSet(viewsets.ModelViewSet):
    queryset = Establecimiento.objects.all()
    serializer_class = EstablecimientoSerializer