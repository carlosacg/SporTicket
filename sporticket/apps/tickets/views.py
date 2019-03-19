from django.shortcuts import render
from apps.location.forms import LocationForm
from apps.tickets.forms import TicketLocationForm
from apps.location.models import Location
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
import psycopg2
from apps.events.models import Event
from apps.tickets.models import Ticket
from django.db import connection 
from django.contrib import messages
from django.urls import reverse_lazy,reverse


# Create your views here.

def insertTickets(quantity,ubication,event,state):
    print(quantity,ubication,event,state)
    x=0
    while x < int(quantity):        
        save_data(ubication,event,state) 
        x+=1

def insertLocation(request,event,name,cost):
    location = Location(event=event, name=name,cost=cost)
    location.save()

def addTicketLocationView(request,ubication,event,quantity):
    insertTickets(quantity,ubication,event,'Disponible')
    return HttpResponseRedirect(reverse('ticket_crear', args=[event.id]))

def addLocationView(request,event,name,cost):
    event =  Event.objects.get(id=event)
    locations = Location.objects.filter(event=event)
    insertLocation(request,event,name,cost)
    return HttpResponseRedirect(reverse('ticket_crear', args=[event.id]))

def insertLocationView(request,id):
    event =  Event.objects.get(id=id)
    object = Event()
    locations = Location.objects.filter(event=id)
    location_form=LocationForm()

    if request.method == 'POST':
        location_form = LocationForm(request.POST)
        if location_form.is_valid:
            location_repeat=Location.objects.all().filter(event=event).filter(name=location_form['name'].value())
            if location_repeat.first() == None:
                addLocationView(request,event.id,location_form['name'].value(),location_form['cost'].value())
                messages.success(request,'Localidad agregada exitosamente')
                return HttpResponseRedirect(reverse('location_crear', args=[id]))
            else:
                messages.error(request,'Error, localidad repetida')
                return HttpResponseRedirect(reverse('location_crear', args=[id]))
    else:
        context = {'event':event,'location_form':location_form,'locations':locations}              
    return render(request, 'tickets/generateLocations.html',context)   


def renderGlobalTicket(request,id):
    event =  Event.objects.get(id=id)
    locations = Location.objects.filter(event=id)
    arrayTicket=getListTicket(id)
    if request.method=='POST':
        form = TicketLocationForm(request.POST)
        if form.is_valid:
            addTicketLocationView(request, form['location'].value(), event, form['zone'].value())
            updateCapacityEvent( event.id ,int(form['zone'].value()))
            location=Location.objects.get(id=int(form['location'].value()))
            print(location)
            print(location.name)
            messages.success(request,'Boletos de la localidad '+location.name+' agregados exitosamente')
            return HttpResponseRedirect(reverse('ticket_crear', args=[id]))
    else:
        form = TicketLocationForm()
        form.query(event)
    context = {'tickets':arrayTicket,'form':form,'event':event,'locations':locations}                     
    return render(request, 'tickets/generateTicketLocation.html',context)


def save_data(ubication,event,state):
    location= Location.objects.get(id=ubication)
    newTicket = Ticket(location=location,event=event,state=state)
    newTicket.save()

def updateCapacityEvent(event,newCapacity):
    event = Event.objects.get(id=event)
    oldCapacity= event.capacity
    event.capacity = newCapacity + oldCapacity
    event.save()

def addTicketView(request,id,ubication):
    event =  Event.objects.get(id=id)
    location = Location.objects.filter(name=ubication).get(event=event)
    locationArray = Location.objects.filter(name=ubication).filter(event=event)
    arrayTicket=getListTicket( id )
    object = Ticket()
    id_location=''
    for locations in locationArray:
        id_location=locations.id
    ticket = Ticket.objects.filter(event=event).filter(location=id_location).last()
    save_ticket(location,ticket.event)
    updateCapacityEvent( event.id ,1) 
    return HttpResponseRedirect(reverse('ticket_crear', args=[id]))

def minusTicketView(request,id,ubication):
    event =  Event.objects.get(id=id)
    location = Location.objects.filter(name=ubication).get(event=event)
    event_type=event.event_type
    arrayTicket=getListTicket( id )
    delete_ticket(id,location,'one')
    updateCapacityEvent( event.id ,-1)
    return HttpResponseRedirect(reverse('ticket_crear', args=[id]))

def deleteTicketsView(request,id,ubication):
    event =  Event.objects.get(id=id)
    location = Location.objects.filter(name=ubication).get(event=event)
    event_type=event.event_type
    arrayTicket=getListTicket( id )
    quantity=Ticket.objects.filter(event=id).filter(location=location).count()
    delete_ticket(id,location,'all')
    updateCapacityEvent( event.id ,-1*quantity)
    return HttpResponseRedirect(reverse('ticket_crear', args=[id]))

def deleteLocationsView(request,id,event):
    Location.objects.filter(id=id).delete()
    return HttpResponseRedirect(reverse('location_crear', args=[event]))

def getListTicket(event):
    cursor = connection.cursor()
    instruction = "SELECT count(*),location_location.name,location_location.cost from tickets_ticket,location_location WHERE location_location.id=tickets_ticket.location_id AND tickets_ticket.event_id="+str(event)+" GROUP BY location_location.cost,location_location.name;"
    cursor.execute(instruction)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows
   
def save_ticket(location,event):
    newTicket = Ticket(location=location,event=event,state='Disponible')
    newTicket.save()

def delete_ticket(id,location,case):
    if case =='one':
        Ticket.objects.filter(event=id).filter(location=location).last().delete()
    if case =='all':
        Ticket.objects.filter(event=id).filter(location=location).delete()

