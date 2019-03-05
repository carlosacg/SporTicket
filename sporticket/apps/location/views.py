from django.shortcuts import render
from apps.location.models import Location
from apps.location.models import Event

# Create your views here.

def insertLocation(request,event,name):
    event_object= Event.objects.filter(id=event)
    location = Location(event=event, name=name)
    location.save()
    return redirect('tickets/generateTicket.html/'+str(event))

def deleteLocation(request,id,event):
    Location.objects.filter(id=id).delete()
    return redirect('tickets/generateTicket.html/'+str(event))
