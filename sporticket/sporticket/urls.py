
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('apps.events.urls')),
    url(r'^', include('apps.tickets.urls')),
	url(r'^', include('apps.users.urls')),
]
