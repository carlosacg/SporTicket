from django.urls import path
from django.conf.urls import url,include

from apps.sales.views import *

urlpatterns = [

    url(r'sales/createSale.html', index_sale),
]