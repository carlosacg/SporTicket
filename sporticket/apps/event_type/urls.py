from django.conf.urls import url, include
from apps.events.views import *
from django.contrib.auth.decorators import login_required
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'events/insertEvenType.html', login_required(insertEventType), name='tipo_evento_crear' ),
]

urlpatterns = format_suffix_patterns(urlpatterns)