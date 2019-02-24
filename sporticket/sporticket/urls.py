
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from apps.users.views import userLogin, userLogout, success
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('apps.events.urls')),
    url(r'^', include('apps.tickets.urls')),
	url(r'^', include('apps.users.urls')),
	url(r'^', include('apps.sales.urls')),
	url(r'^', include('apps.reports.urls')),
	url(r'^login/', userLogin, name="userLogin"),
	url(r'^success/', success, name="userSuccess"),
	url(r'^logout/', userLogout, name="userLogout"),
	url(r'^oauth/', include('social_django.urls', namespace='social')),  

]
