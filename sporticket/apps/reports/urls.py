from django.conf.urls import url, include
from apps.reports.views import *
from apps.reports.views import report_f
from django.contrib.auth.decorators import login_required


urlpatterns = [
	#url(r'reports/reports.html', index_sale),
	url(r'reports/reports.html', login_required(report_f), name='report1'),
]