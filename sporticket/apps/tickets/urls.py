from django.conf.urls import url, include
from apps.tickets.views import *


urlpatterns = [
    url(r'tickets/generateTicket.html', generateTickets, name='ticket_crear' ),
    url(r'tickets/generateTicketBaseball.html', generateTickets, name='ticket_crear' ),
]