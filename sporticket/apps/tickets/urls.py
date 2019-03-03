from django.conf.urls import url, include
from apps.tickets.views import *


urlpatterns = [
    url(r'tickets/generateTicket.html/(?P<id>\d+)/$', generateTickets, name='ticket_crear' ),
    url(r'tickets/addTicket.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', addTicketView, name='ticket_add' ),
    url(r'tickets/minusTicket.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', minusTicketView, name='ticket_minus' ),
    url(r'tickets/deleteTickets.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', deleteTicketsView, name='ticket_delete' ),
    url(r'tickets/addNorth.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', addNorthView, name='add_north' ),
    url(r'tickets/addSouth.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', addSouthView, name='add_south' ),
    url(r'tickets/addEast.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', addEastView, name='add_east' ),
    url(r'tickets/addWest.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', addWestView, name='add_west' ),
    url(r'tickets/addHigth.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', addHightView, name='add_higth' ),
    url(r'tickets/addMedium.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', addMediumView, name='add_medium' ),
    url(r'tickets/addLow.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', addLowView, name='add_low' ),

]