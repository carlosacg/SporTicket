from django.conf.urls import url, include
from apps.reports.views import *
from apps.reports.views import report_f
from django.contrib.auth.decorators import login_required


urlpatterns = [
	#url(r'reports/reports.html', index_sale),
	url(r'reports/reports.html', login_required(report_f), name='report1'),
	url(r'sales/saleEvent.html', login_required(reportByDailySales), name='dailySales'),
	url(r'reports/saleEvents.html', login_required(reportSaleEvents), name='reportEvent'),
	url(r'reports/graphicsReports.html', login_required(graphicsReport), name='graphicsReport'),
]