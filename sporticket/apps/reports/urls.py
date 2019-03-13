from django.conf.urls import url, include
from apps.reports.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [

	url(r'^$', login_required(base), name='base'),
	url(r'reports/reports.html', login_required(index), name='indexReports'),
	url(r'sales/saleEvent.html', login_required(reportByDailySales), name='dailySales'),
	url(r'reports/saleEvents.html', login_required(reportByEvents), name='reportEvent'),
	url(r'reports/graphicsReports.html', login_required(graphicsReport), name='graphicsReport'),
	url(r'reports/dailySales.html', login_required(dailyReport), name='dailyReport'),
	url(r'reports/sellerReport.html', login_required(sellerReport), name='sellerReport'),
	url(r'reports/dateRange.html', login_required(reportByDateRange), name='dateRange'),
]