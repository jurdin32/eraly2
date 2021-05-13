from rest_framework import routers

from Empresa.viewSet import EstablecimientoViewSet
from Personas.viewSet import UserViewSet
from Producto.viewSet import ProductoViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'producto', ProductoViewSet)
router.register(r'establecimiento', EstablecimientoViewSet)
