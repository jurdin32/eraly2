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
from ckeditor_demo.demo_application.tests.test_deprecation import generator_with_filename_and_request
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from Empresa.views import *
from Home.views import *
from Personas.views import registroCLientes, deshabilitarCliente
from Producto.views import *
from Store.views import *
from Store.views import _productos, _detalles, _tiendas
from Ventas.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("",index),

    path("business/",empresa),
    path("business/edit/<int:id>/",modificar_empresa),

    path("directions/",direcciones),

    path("products/",productos),
    path("products/new/",registarProducto),
    path("products/edit/<int:id>/",productos_detalles),

    path("products/colors/<int:id>/",registrarColores),
    path("products/colors/delete/<int:id>/",eliminarColorProducto),
    path("products/prices/<int:id>/",registrarPrecios),
    path("products/prices/delete/<int:id>/",eliminarPrecios),
    path("products/images/<int:id>/",subir_imagenes_producto), #subir archivos

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
    path("kardex/products/<int:id>/", kardex_producto),
    path("inventory/", inventario),

    path("business/remove/",eliminar_empresa),
    path("business/direcction/<int:idEmpresa>/",crear_direcciones),
    path("directions/edit/<int:id>/",modificar_direcciones),
    path("directions/delete/<int:id>/",eliminar_direcciones),
    path("proforms/<id>/",proformas),
    path("proforms/createCLient/<id>/",registroClienteFacturaProforma),
    path("proforms/create/<int:id>/",registrarDocumento),
    path("proforms/detall/<int:id>/",registrarDetallesFacturaProforma),

    path("proforms/edit/<int:id>/",editarDocumentos),
    path("giveBack/<int:id>/",anularDocumento),

    path("billing/<id>/",facturas),

    path("document/proform/<int:id>/",crearDocumentoPDF_Proforma),
    path("document/fac/<int:id>/",crearDocumentoPDF_Factura),
    path("document/list/",listaDocumentos),

    path("clients/<int:id>/",registroCLientes),
    path("clients/disable/<int:id>/",deshabilitarCliente),

    path("accounts_receivable/",cuentasCobrar),
    path("accounts_receivable/<int:id>/",abonos),
    path("accounts_receivable/print/<int:id>/",crearAbonosPDF),

    path("logout_/",logout_),

    #tienda
    path("store/",tienda),
    path("store/products/",_productos),
    path("store/details/",_detalles),
    path("store/stores/",_tiendas),
    path("store/ejemplo/",ejemplo),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Eraly V.2'