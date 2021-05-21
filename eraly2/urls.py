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
from rest_framework.authtoken.views import obtain_auth_token

from Empresa.views import *
from Home.views import *
from Personas.views import *
from Producto.views import *
from Store.views import *
from Store.views import _productos, _detalles, _tiendas
from Ventas.views import *
from eraly2 import routes

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("",index),
    path('policies/police',politica),
    path("business/",empresa),
    path("business/edit/<int:id>/",modificar_empresa),

    path("directions/",direcciones),

    path("products/",productos),
    path("products/new/",registarProducto),
    path("products/edit/<int:id>/",productos_detalles),

    path("products/colors/<int:id>/",registrarColores),
    path("products/colors/delete/<int:id>/",eliminarColorProducto),
    path("products/prices/<int:id>/",registrarPrecios),
    path("products/prices/edit/<int:id>/",editarPrecios),
    path("products/prices/delete/<int:id>/",eliminarPrecios),
    path("products/promo/",promociones),
    path("products/promo/price_web/<int:id>/",return_precio_web),
    path("products/promo/edit/<int:id>/",editarPromocion),
    path("products/images/<int:id>/",subir_imagenes_producto),
    path("products/images/delete/<int:id>/", eliminar_imagen),
    path("category/",categorias),
    path("category/edit/<int:id>/",editarCategoria),
    path("subcategory/edit/<int:id>/",editarSubCategoria),
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
    path("business/user_register/",registro_otrosUsuarios),

    path("directions/edit/<int:id>/",modificar_direcciones),
    path("directions/delete/<int:id>/",eliminar_direcciones),

    path("proforms/<id>/",proformas),
    path("proforms/createCLient/<id>/",registroClienteFacturaProforma),
    path("proforms/create/<int:id>/",registrarDocumento),
    path("proforms/detall/<int:id>/",registrarDetallesFacturaProforma),
    path("proforms/edit/<int:id>/", editarDocumentos),
    path("document/proform/<int:id>/",crearDocumentoPDF_Proforma),
    path("document/fac/<int:id>/",crearDocumentoPDF_Factura),
    path("document/list/",listaDocumentos),
    path("billing/<id>/",proformas),

    path("store/autority/",autorizar_ComprasWeb),
    path("store/autority/<slug:hash>/",info_cliente_compra),


    path("giveBack/<int:id>/",anularDocumento),

    path("clients/<int:id>/",registroCLientes),
    path("clients/disable/<int:id>/",deshabilitarCliente),

    path("accounts_receivable/",cuentasCobrar),
    path("accounts_receivable/<int:id>/",abonos),

    path("logout_/",logout_),

    #tienda
    path("store/",tienda),
    path("store/products/",_productos),
    path("store/details/",_detalles),
    path("store/fav/",favoritos),
    path("store/category/",ver_subcategorias),
    path("<slug:slug>/",_tiendas),
    path("store/search/",ver_subcategorias),
    path("store/account/",account),
    path("store/register/",register),
    path("store/login/",login_store_user),
    path("store/dashboard/",dashboard),
    path("store/wishlist/", lista_favoritos),
    path("store/wishlist/detelete/<slug:slug>/", borrar_favoritos),
    path("store/directory/",directorio),
    path("store/directory/delete/<int:n>/",eliminar_directorio),
    path("store/shopp/",misOrdenes),
    path("store/contact/",contact),
    path("store/checkout/",checkout),
    path("store/checkout/pay/",pay),
    #carrito de compras
    path("store/add/cart/",add_carrito),
    path("store/add/cart/deleteItem/",eliminar_item),
    path("store/view/cart/",ver_cart),
    path("store/view/cart/delete/",vaciar_carrito),
    #django restframework:
    path('api/rf/', include('rest_framework.urls')),
    path('api/auth/', obtain_auth_token),
    path('api/', include(routes.router.urls)),






]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'Eraly V.2'