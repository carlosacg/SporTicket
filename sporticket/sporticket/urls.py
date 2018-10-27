
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from apps.users.views import userLogin, userLogout, success

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('apps.events.urls')),
    url(r'^', include('apps.tickets.urls')),
	url(r'^', include('apps.users.urls')),
	url(r'^login/', userLogin, name="userLogin"),
	url(r'^success/', success, name="userSuccess"),
	url(r'^logout/', userLogout, name="userLogout"),
]
