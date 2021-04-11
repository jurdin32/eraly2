from rest_framework import routers

from Empresa.viewSet import EstablecimientoViewSet
from Producto.viewSet import ProductoViewSet

router = routers.DefaultRouter()
router.register(r'producto', ProductoViewSet)
router.register(r'establecimiento', EstablecimientoViewSet)