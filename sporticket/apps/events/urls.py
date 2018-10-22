from django.conf.urls import url, include
from apps.events.views import *


urlpatterns = [
    url(r'^$', index),
    url(r'events/insertEvents.html', insertEvent, name='evento_crear' ),
    url(r'events/listEvents.html', EventList.as_view(), name='evento_listar' ),
    url(r'events/updateEvents/(?P<pk>\d+)/$', EventUpdate.as_view(), name='evento_editar' ),
    url(r'events/deleteEvents/(?P<id>\d+)/$', deleteEvent, name='evento_eliminar' ),
    url(r'events/uploadFile.html', uploadFile, name='evento_cargar' ),
    url(r'events/viewEvents/(?P<id>\d+)/$', viewEvent, name='evento_ver' ),

]
