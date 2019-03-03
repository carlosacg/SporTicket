from django.conf.urls import url, include
from apps.tickets.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'tickets/generateTicket.html/(?P<id>\d+)/$', login_required(generateTickets), name='ticket_crear' ),
    url(r'tickets/addTicket.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', login_required(addTicketView), name='ticket_add' ),
    url(r'tickets/minusTicket.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', login_required(minusTicketView), name='ticket_minus' ),
    url(r'tickets/deleteTickets.html/(?P<id>[^/]+)/(?P<ubication>[^/]+)/$', login_required(deleteTicketsView), name='ticket_delete' ),
    url(r'tickets/addNorth.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', login_required(addNorthView), name='add_north' ),
    url(r'tickets/addSouth.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', login_required(addSouthView), name='add_south' ),
    url(r'tickets/addEast.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', login_required(addEastView), name='add_east' ),
    url(r'tickets/addWest.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', login_required(addWestView), name='add_west' ),
    url(r'tickets/addHigth.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', login_required(addHightView), name='add_higth' ),
    url(r'tickets/addMedium.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', login_required(addMediumView), name='add_medium' ),
    url(r'tickets/addLow.html/(?P<event>[^/]+)/(?P<quantity>[^/]+)/(?P<cost>[^/]+)/$', login_required(addLowView), name='add_low' ),

]