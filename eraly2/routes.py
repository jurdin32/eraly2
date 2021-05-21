from rest_framework import routers
from Personas.viewSet import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
