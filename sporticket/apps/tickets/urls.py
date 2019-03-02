from django.conf.urls import url, include
from apps.tickets.views import *


urlpatterns = [
    url(r'tickets/generateTicket.html/(?P<id>\d+)/$', generateTickets, name='ticket_crear' ),
]