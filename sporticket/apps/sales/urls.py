from django.conf.urls import url, include
from apps.sales.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
	#url(r'sales/createSale.html', index_sale),
    #url(r'^$', index),
    #url(r'sales/userSale.html', userSale, name='venta_usuario' ),
	#path('index', index_user, name='index'),
    #path('crear_factura', BillCreate.as_view(), name='base'),/sales/viewsEvent.html
    url(r'sales/viewsEvent.html', login_required(listEvent), name='evento_listar_compras' ),
    #url(r'sales/createShopping/(?P<id>\d+)/$', login_required(createShopAjax), name='comprar_boletos' ),
    url(r'sales/createShopping/(?P<id>\d+)/$', login_required(createShop), name='comprar_boletos' ),
    url(r'sales/createSale/(?P<id>\d+)/$', login_required(createSale), name='realizar_venta' ),
    url(r'sales/saleEvent.html', login_required(listEvent1), name='evento_venta' ),
    url(r'sales/getShopData.html', login_required(getShopAjax), name='compra_ajax' ),



]
