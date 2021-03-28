from rest_framework import routers

from Producto.viewSet import ProductoViewSet

router = routers.DefaultRouter()
router.register(r'producto', ProductoViewSet)