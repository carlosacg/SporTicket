from django.conf.urls import url, include
from apps.tickets.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [

    url(r'tickets/generateTicket.html/(?P<id>\d+)/$', login_required(renderGlobalTicket), name='ticket_crear' ),
    url(r'tickets/generateLocation.html/(?P<id>\d+)/$', login_required(insertLocationView), name='location_crear' ),
    url(r'tickets/addTicket.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', login_required(addTicketView), name='ticket_add' ),
    url(r'tickets/minusTicket.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', login_required(minusTicketView), name='ticket_minus' ),
    url(r'tickets/deleteTickets.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', login_required(deleteTicketsView), name='ticket_delete' ),
    url(r'tickets/deleteLocations.html/(?P<event>[^/]+)/(?P<id>[^/]+)/$', login_required(deleteLocationsView), name='location_delete' ),
    url(r'location/addLocation.html/(?P<event>[^/]+)/(?P<name>[^/]+)/$', login_required(addLocationView), name='add_location' ),

]