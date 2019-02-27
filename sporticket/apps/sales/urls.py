from django.conf.urls import url, include
from apps.sales.views import *

urlpatterns = [
	#url(r'sales/createSale.html', index_sale),
    #url(r'^$', index),
    #url(r'sales/userSale.html', userSale, name='venta_usuario' ),
	#path('index', index_user, name='index'),
    #path('crear_factura', BillCreate.as_view(), name='base'),/sales/viewsEvent.html
    url(r'sales/viewsEvent.html', listEvent, name='evento_listar' ),
    url(r'sales/createShopping/(?P<id>\d+)/$', createShopping, name='comprar_boletos' ),
    url(r'sales/createSale/(?P<id>\d+)/$', createSale, name='realizar_venta' ),
    url(r'sales/saleEvent.html', listEvent1, name='evento_venta' ),
	


]
