from django.conf.urls import url, include
from apps.reports.views import *
from apps.reports.views import report_f


urlpatterns = [
	#url(r'reports/reports.html', index_sale),
	url(r'reports/reports.html', report_f, name='report1'),
]