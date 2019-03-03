from django.conf.urls import url, include
from apps.tickets.views import *


urlpatterns = [
    url(r'tickets/generateTicket.html/(?P<id>\d+)/$', generateTickets, name='ticket_crear' ),
    url(r'tickets/addTicket.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', addTicketView, name='ticket_add' ),
    url(r'tickets/minusTicket.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', minusTicketView, name='ticket_minus' ),
    url(r'tickets/deleteTickets.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', deleteTicketsView, name='ticket_delete' ),

]