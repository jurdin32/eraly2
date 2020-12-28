"""eraly2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from Empresa.views import *
from Home.views import *
from Producto.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("",index),

    path("business/",empresa),
    path("business/edit/<int:id>/",modificar_empresa),

    path("directions/",direcciones),

    path("products/",productos),
    path("products/edit/<int:id>/",productos_detalles),

    path("category/",categorias),
    path("category/edit/<int:id>/",editarCategoria),
    path("category/remove/<int:id>/",eliminarCategoria),
    path("subcategory/edit/<int:id>/",editarSubCategoria),
    path("subcategory/remove/<int:id>/",eliminarSubcategoria),


    path("category/<int:id>/",subcategorias),

    path("suppliers/",proveedores),
    path("suppliers/edit/<int:id>/",editarProveedor),
    path("suppliers/delete/<int:id>/",eliminarProveedor),

    path("suppliers/activity/<int:id>/",actividadesProveedor),
    path("suppliers/activity/delete/<int:id>/",eliminarActividades),
    path("suppliers/type/<int:id>/",tipoProveedor),
    path("suppliers/type/delete/<int:id>/",eliminartipoProveedor),
    path("suppliers/direction/<int:id>/",direccionProveedor),
    path("suppliers/direction/delete/<int:id>/",eliminarDireccionProveedores),

    path("kardex/", kardex),
    path("business/remove/",eliminar_empresa),
    path("business/direcction/<int:idEmpresa>/",crear_direcciones),
    path("directions/edit/<int:id>/",modificar_direcciones),
    path("directions/delete/<int:id>/",eliminar_direcciones),
    path("logout_/",logout_),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Eraly V.2'