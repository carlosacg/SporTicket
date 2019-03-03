from django.conf.urls import url, include
from apps.events.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', index),
    url(r'events/insertEvents.html', login_required(insertEvent), name='evento_crear' ),
    url(r'events/uploadImage.html(?P<id>\d+)/$', login_required(uploadImage), name='evento_imagen' ),
    url(r'events/listEvents.html', login_required(EventList.as_view()), name='evento_listar' ),
    url(r'events/updateEvents/(?P<pk>\d+)/$', login_required(EventUpdate.as_view()), name='evento_editar' ),
    url(r'events/deleteEvents/(?P<id>\d+)/$', login_required(deleteEvent), name='evento_eliminar' ),
    url(r'events/uploadFile.html', login_required(uploadFile), name='evento_cargar' ),
    url(r'events/viewEvents/(?P<id>\d+)/$', login_required(viewEvent), name='evento_ver' ),

]

