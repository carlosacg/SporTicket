from django.urls import path
from .views import BillCreate
app_name='sales'
urlpatterns = [
	path('index', index_user, name='index'),
    path('crear_factura', BillCreate.as_view(), name='base'),
]