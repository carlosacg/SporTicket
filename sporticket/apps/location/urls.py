from django.conf.urls import url, include
from apps.location.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'location/addLocation.html/(?P<event>[^/]+)/(?P<name>[^/]+)/$', login_required(insertLocation), name='add_location' ),
    url(r'location/deleteLocation.html/(?P<id>[^/]+)/(?P<event>[^/]+)/$', login_required(deleteLocation), name='delete_location' ),

]