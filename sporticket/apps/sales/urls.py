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
    url(r'sales/myShops.html', login_required(listShops), name='listar_compras' ),
    url(r'^sales_ajax/$', login_required(GetDataAjaxView.as_view()), name='get_data_ajax' ),
    url(r'^sales/createShopping/(?P<id>\d+)/$', login_required(createShop), name='comprar_boletos' ),
    url(r'sales/createSale/(?P<id>\d+)/$', login_required(createSale), name='realizar_venta' ),
    url(r'sales/viewSales', login_required(viewSales), name='listar_ventas' ),
    url(r'getDailySales/', login_required(getDailySales), name='getDailySales' ),
    url(r'getEventsForTypes/', login_required(getEventsForTypes), name='getEventsForTypes' ),
    url(r'getNewEvent/', login_required(getNewEvent), name='getNewEvent' ),
    url(r'getBill/', login_required(getBill), name='getBill' ),
    url(r'finishSale/', login_required(finishSale), name='finishSale' ),
    url(r'sales/saleEvent.html', login_required(listEvent1), name='evento_venta' ),
    url(r'sales/listEventsSale.html', login_required(newSales), name='listar_ventas1' ),
]
