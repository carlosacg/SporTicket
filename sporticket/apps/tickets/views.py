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
from django.urls import reverse_lazy,reverse


# Create your views here.

def insertTickets(quantity,ubication,event,state):
    print(quantity,ubication,event,state)
    x=0
    while x < int(quantity):        
        save_data(ubication,event,state) 
        x+=1

def insertLocation(request,event,name,cost):
    print('ENTRO A INSERT LOCATION')
    print(event,name)
    location = Location(event=event, name=name,cost=cost)
    location.save()

def addTicketLocationView(request,ubication,event,quantity):
    print('ENTRO A ADD TICKET CON LOCATION')
    insertTickets(quantity,ubication,event,'Disponible')
    #updateCapacityEvent( event.id ,quantity) 
    return HttpResponseRedirect(reverse('ticket_crear', args=[event.id]))

def addLocationView(request,event,name,cost):
    event =  Event.objects.get(id=event)
    print(event,name)
    print('Entro a addlocationView')
    print(name)
    locations = Location.objects.filter(event=event)
    print(name)
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
            print()
            addLocationView(request,event.id,location_form['name'].value(),location_form['cost'].value())
            return HttpResponseRedirect(reverse('location_crear', args=[id]))
    else:
        context = {'event':event,'location_form':location_form,'locations':locations}              
    return render(request, 'tickets/generateLocations.html',context)   


def renderGlobalTicket(request,id):
    print(id)
    event =  Event.objects.get(id=id)
    object = Event()
    locations = Location.objects.filter(event=id)
    arrayTicket=getListTicket(id)
    print(arrayTicket)
    if request.method=='POST':
        form = TicketLocationForm(request.POST)
        if form.is_valid:
            addTicketLocationView(request, form['location'].value(), event, form['zone'].value())
            updateCapacityEvent( event.id ,int(form['zone'].value()))
            return HttpResponseRedirect(reverse('ticket_crear', args=[id]))
    else:
        form = TicketLocationForm()
    context = {'tickets':arrayTicket,'form':form,'event':event,'locations':locations}                     
    return render(request, 'tickets/generateTicketLocation.html',context)




def generateTickets(request,id):
    event =  Event.objects.get(id=id)
    event_type=event.event_type
    object = Event()
    location_form=LocationForm()
    if event_type == 'Beisbol':  #SI EL EVENTO CREADO FUE TIPO BEISBOL
        if request.method == 'POST':
            form = BaseballForm(request.POST)
            if form.is_valid():
                if form['costHigth'].value() != '' and form['higthZone'].value() != '':
                    ticket=Ticket.objects.filter(event=event).filter(ubication='Zona alta').last()
                    if ticket==None:
                        addHightView(request,event,int(form['higthZone'].value()),int(form['costHigth'].value()))
                        #AÑADIR MENSAJE "SE GENERARON int(form['higthZone'].value()) BOLETOS DE LA ZONA ALTA"
                    else: 
                        if int(ticket.cost) == int(form['costHigth'].value()):
                            addHightView(request,event,int(form['higthZone'].value()),int(form['costHigth'].value()))
                        else:
                            print('LOS BOLETOS QUE INTENTA INSERTAR NO TIENEN EL MISMO PRECIO DE LOS ACTUALES')
                            #AÑADIR MENSAJE "LOS BOLETOS QUE INTENTA INSERTAR NO TIENEN EL MISMO PRECIO DE LOS ACTUALES"

                if form['costMediun'].value() != '' and form['mediumZone'].value() != '':
                    ticket=Ticket.objects.filter(event=event).filter(ubication='Zona media').last()
                    if ticket==None:
                        addMediumView(request,event,int(form['mediumZone'].value()),int(form['costMediun'].value()))
                    else:
                        if int(ticket.cost) == int(form['costMediun'].value()):
                            addMediumView(request,event,int(form['mediumZone'].value()),int(form['costMediun'].value()))
                        else:
                            print('LOS BOLETOS QUE INTENTA INSERTAR NO TIENEN EL MISMO PRECIO DE LOS ACTUALES')
                            #AÑADIR MENSAJE "LOS BOLETOS QUE INTENTA INSERTAR NO TIENEN EL MISMO PRECIO DE LOS ACTUALES"
                
                if form['costLow'].value() != '' and form['lowZone'].value() != '':
                    ticket=Ticket.objects.filter(event=event).filter(ubication='Zona baja').last()
                    if ticket==None:
                        addLowView(request,event,int(form['lowZone'].value()),int(form['costLow'].value()))
                    else:
                        if int(ticket.cost) == int(form['costLow'].value()):
                            addLowView(request,event,int(form['lowZone'].value()),int(form['costLow'].value())) 
                        else:
                            print('LOS BOLETOS QUE INTENTA INSERTAR NO TIENEN EL MISMO PRECIO DE LOS ACTUALES')
             
            return HttpResponseRedirect(reverse('ticket_crear', args=[id]))
        else:
            form = BaseballForm()
        arrayTicket=getListTicket(str(event.id))
        context = {'tickets':arrayTicket,'form':form,'event':event}
        
        return render(request, 'tickets/generateTicketBaseball.html',context)
    else:                       #SI EL EVENTO CREADO FUE FUTBOL O TENIS
        if request.method == 'POST':
            form = TicketForm(request.POST)
            if form.is_valid():
                if form['costNorth'].value() != '' and form['northZone'].value() != '':
                    ticket=Ticket.objects.filter(event=event).filter(ubication='Tribuna norte').last()
                    if ticket==None:
                        addNorthView(request,event,int(form['northZone'].value()),int(form['costNorth'].value()))
                    else:
                        if int(ticket.cost) == int(form['costNorth'].value()):
                            addNorthView(request,event,int(form['northZone'].value()),int(form['costNorth'].value()))
                        else:
                            print('LOS BOLETOS QUE INTENTA INSERTAR NO TIENEN EL MISMO PRECIO DE LOS ACTUALES')

                if form['costSouth'].value() != '' and form['southZone'].value() != '':
                    ticket=Ticket.objects.filter(event=event).filter(ubication='Tribuna sur').last()
                    if ticket==None:                  
                        addSouthView(request,event,int(form['southZone'].value()),int(form['costSouth'].value()))
                    else:
                        if int(ticket.cost) == int(form['costSouth'].value()):
                            addSouthView(request,event,int(form['southZone'].value()),int(form['costSouth'].value()))
                        else:
                            print('LOS BOLETOS QUE INTENTA INSERTAR NO TIENEN EL MISMO PRECIO DE LOS ACTUALES')

                if form['costEast'].value() != '' and form['eastZone'].value() != '':
                    ticket=Ticket.objects.filter(event=event).filter(ubication='Tribuna oriente').last()
                    if ticket==None:
                        addEastView(request,event,int(form['eastZone'].value()),int(form['costEast'].value()))
                    else:
                        if int(ticket.cost) == int(form['costEast'].value()):
                            addEastView(request,event,int(form['eastZone'].value()),int(form['costEast'].value()))
                        else: 
                            print('LOS BOLETOS QUE INTENTA INSERTAR NO TIENEN EL MISMO PRECIO DE LOS ACTUALES')

                if form['costWest'].value() != '' and form['westZone'].value() != '':
                    ticket=Ticket.objects.filter(event=event).filter(ubication='Tribuna occidente').last()
                    if ticket==None:
                        addWestView(request,event,int(form['westZone'].value()),int(form['costWest'].value())) 
                    else:
                        if int(ticket.cost) == int(form['costWest'].value()):
                            addWestView(request,event,int(form['westZone'].value()),int(form['costWest'].value())) 
                        else: 
                            print('LOS BOLETOS QUE INTENTA INSERTAR NO TIENEN EL MISMO PRECIO DE LOS ACTUALES')
            return HttpResponseRedirect(reverse('ticket_crear', args=[id]))
        else:
            form = TicketForm()
        arrayTicket=getListTicket( str(event.id) )
        context = {'tickets':arrayTicket,'form':form,'event':event}
        return render(request, 'tickets/generateTicket.html',context)
    

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
    print(location)
    locationArray = Location.objects.filter(name=ubication).filter(event=event)
    arrayTicket=getListTicket( id )
    object = Ticket()
    print(event,location)
    id_location=''
    for locations in locationArray:
        id_location=locations.id
    ticket = Ticket.objects.filter(event=event).filter(location=id_location).last()
    print(ticket)
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

def addNorthView(request,event,quantity,cost):
    print(event,quantity,cost)
    event_type=event.event_type
    arrayTicket=getListTicket( event.id )
    insertTickets(quantity,'Tribuna norte',event,cost,'Disponible')
    updateCapacityEvent( event.id ,quantity) 
    form = TicketForm()
    context = {'tickets':arrayTicket,'form':form}
    return HttpResponseRedirect(reverse('ticket_crear', args=[event.id]))

def addSouthView(request,event,quantity,cost):
    print(event,quantity,cost)
    event_type=event.event_type
    arrayTicket=getListTicket( event.id )
    insertTickets(quantity,'Tribuna sur',event,cost,'Disponible')
    updateCapacityEvent( event.id ,quantity) 
    form = TicketForm()
    context = {'tickets':arrayTicket,'form':form}
    return HttpResponseRedirect(reverse('ticket_crear', args=[event.id]))

def addEastView(request,event,quantity,cost):
    print(event,quantity,cost)
    event_type=event.event_type
    arrayTicket=getListTicket( event.id )
    insertTickets(quantity,'Tribuna oriente',event,cost,'Disponible')
    updateCapacityEvent( event.id ,quantity) 
    form = TicketForm()
    context = {'tickets':arrayTicket,'form':form}
    return HttpResponseRedirect(reverse('ticket_crear', args=[event.id]))

def addWestView(request,event,quantity,cost):
    print(event,quantity,cost)
    event_type=event.event_type
    arrayTicket=getListTicket( event.id )
    insertTickets(quantity,'Tribuna occidente',event,cost,'Disponible')
    updateCapacityEvent( event.id ,quantity) 
    form = TicketForm()
    context = {'tickets':arrayTicket,'form':form}
    return HttpResponseRedirect(reverse('ticket_crear', args=[event.id]))

def addHightView(request,event,quantity,cost):
    print(event,quantity,cost)
    event_type=event.event_type
    arrayTicket=getListTicket( event.id )
    insertTickets(quantity,'Zona alta',event,cost,'Disponible')
    updateCapacityEvent( event.id ,quantity) 
    form = BaseballForm()
    context = {'tickets':arrayTicket,'form':form}
    return HttpResponseRedirect(reverse('ticket_crear', args=[event.id]))

def getListTicket(event):
    cursor = connection.cursor()
    instruction = "SELECT count(*),location_location.name,location_location.cost from tickets_ticket,location_location WHERE location_location.id=tickets_ticket.location_id AND tickets_ticket.event_id="+str(event)+" GROUP BY location_location.cost,location_location.name;"
    cursor.execute(instruction)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    print(instruction)
    print(rows)
    return rows
    
def addMediumView(request,event,quantity,cost):
    print(event,quantity,cost)
    event_type=event.event_type
    arrayTicket=getListTicket( event.id )
    insertTickets(quantity,'Zona media',event,cost,'Disponible')
    updateCapacityEvent( event.id ,quantity) 
    form = BaseballForm()
    context = {'tickets':arrayTicket,'form':form}
    return HttpResponseRedirect(reverse('ticket_crear', args=[event.id]))

def addLowView(request,event,quantity,cost):
    print(event,quantity,cost)
    event_type=event.event_type
    arrayTicket=getListTicket( event.id )
    insertTickets(quantity,'Zona baja',event,cost,'Disponible')
    updateCapacityEvent( event.id ,quantity) 
    form = BaseballForm()
    context = {'tickets':arrayTicket,'form':form}
    return HttpResponseRedirect(reverse('ticket_crear', args=[event.id]))

def save_ticket(location,event):
    newTicket = Ticket(location=location,event=event,state='Disponible')
    newTicket.save()

def delete_ticket(id,location,case):
    if case =='one':
        Ticket.objects.filter(event=id).filter(location=location).last().delete()
    if case =='all':
        Ticket.objects.filter(event=id).filter(location=location).delete()

