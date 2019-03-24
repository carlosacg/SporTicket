from django.conf.urls import url, include
from apps.events.views import *
from django.contrib.auth.decorators import login_required
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', login_required(index), name='indexEvents'),
    url(r'events/insertEvents.html', login_required (insertEvent), name='evento_crear' ),
    url(r'events/insertEvenType.html', login_required(insertEventType), name='tipo_evento_crear' ),
    url(r'events/uploadImage.html(?P<id>\d+)/$', login_required(uploadImage), name='evento_imagen' ),
    url(r'events/listEvents.html', EventList.as_view(), name='evento_listar' ),
    url(r'events/updateEvents/(?P<pk>\d+)/$', EventUpdate.as_view(), name='evento_editar' ),
    url(r'events/deleteEvents/(?P<id>\d+)/$', login_required(deleteEvent), name='evento_eliminar' ),
    url(r'events/uploadFile.html', login_required(uploadFile), name='evento_cargar' ),
    url(r'events/viewEvents/(?P<id>\d+)/$', login_required(viewEvent), name='evento_ver' ),
    url(r'^events/$', EventsSerialList.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', EventsSerialDetail.as_view()),
    url(r'events/loadReferredEvents.html', login_required(referredEvents), name='evento_eventos' ),

]

urlpatterns = format_suffix_patterns(urlpatterns)

