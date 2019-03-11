# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^login/$',views.dologin),
    url(r'^logout/$',views.dologout,name="logout"),
    url(r'^registro/$',views.dosignup,name="registro"),
    url(r'^shop/$',views.tienda,name="tienda"),
    url(r'^shop/producto/(?P<slug>[\w-]+)/$',views.detalleProducto,name="productodetalle"),
    url(r'^shop/mis_pedidos/$',views.pedidosUsuario,name="mis_pedidos"),
    url(r'^shop/mis_pedidos/(?P<pk>\d+)/$',views.detallePedido,name="pedidodetalle"),
    url(r'^shop/mi_perfil/$',views.perfilUsuario,name="mi_perfil"),
    url(r'^shop/carrito/$',views.carrito,name="carrito"),
    url(r'^shop/carrito/update/$',views.updateCarrito,name="updatecarrito"),
    url(r'^shop/carrito/checkout/$',views.checkoutCarrito,name="checkout"),
    url(r'^shop/admin/$',views.adminSite,name="adminhome"),
    url(r'^shop/admin/producto/(?P<slug>[\w-]+)/$',views.adminSiteProductoDetalle,name="adminproductosdetalle"),
    url(r'^shop/admin/producto_nuevo/$',views.adminSiteProductoNuevo,name="adminproductonuevo"),
    url(r'^shop/admin/clientes/$',views.adminSiteClientes,name="adminclientes"),
    url(r'^shop/admin/pedidos/(?P<pk>\d+)/$',views.adminSitePedidosDetalle,name="adminpedidosdetalle"),
    
]