from django.conf.urls import url, include
from apps.reports.views import *

urlpatterns = [
	url(r'reports/reports.html', index_sale),
	url(r'reports/reports.html', dasd, name='report1'),
]