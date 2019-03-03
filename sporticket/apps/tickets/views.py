from django.shortcuts import render
from apps.tickets.forms import TicketForm
from apps.tickets.forms import BaseballForm
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
import psycopg2
from apps.events.models import Event
from apps.tickets.models import Ticket
from django.db import connection 
from django.urls import reverse_lazy,reverse


# Create your views here.

def insertTickets(quantity,ubication,event,cost,state):
    x=0
    while x < int(quantity):        
        save_data(ubication,event,cost,state) 
        x+=1

def generateTickets(request,id):
    event =  Event.objects.get(id=id)
    event_type=event.event_type
    object = Event()
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
    

def save_data(ubication,event,cost,state):
    newTicket = Ticket(ubication=ubication,event=event,cost=cost,state=state)
    newTicket.save()

def updateCapacityEvent(event,newCapacity):
    event = Event.objects.get(id=event)
    oldCapacity= event.capacity
    event.capacity = newCapacity + oldCapacity
    event.save()

def addTicketView(request,id,ubication):
    event =  Event.objects.get(id=id)
    event_type=event.event_type
    arrayTicket=getListTicket( id )
    object = Ticket()
    print(id)
    ticket = Ticket.objects.filter(event=id).filter(ubication=ubication).last()
    print(ticket.cost,ubication,ticket.event)
    save_ticket(ticket.cost,ubication,ticket.event)
    updateCapacityEvent( event.id ,1) 
    if event_type == 'Beisbol':
        form = BaseballForm()
    else: 
        form = TicketForm()

    context = {'tickets':arrayTicket,'form':form}
    return HttpResponseRedirect(reverse('ticket_crear', args=[id]))

def minusTicketView(request,id,ubication):
    event =  Event.objects.get(id=id)
    event_type=event.event_type
    arrayTicket=getListTicket( id )
    delete_ticket(id,ubication,'one')
    updateCapacityEvent( event.id ,-1)
    if event_type == 'Beisbol':
        form = BaseballForm()
    else: 
        form = TicketForm()

    context = {'tickets':arrayTicket,'form':form}
    return HttpResponseRedirect(reverse('ticket_crear', args=[id]))

def deleteTicketsView(request,id,ubication):
    event =  Event.objects.get(id=id)
    event_type=event.event_type
    arrayTicket=getListTicket( id )
    quantity=Ticket.objects.filter(event=id).filter(ubication=ubication).count()
    delete_ticket(id,ubication,'all')
    updateCapacityEvent( event.id ,-1*quantity)
    if event_type == 'Beisbol':
        form = BaseballForm()
    else: 
        form = TicketForm()
    context = {'tickets':arrayTicket,'form':form}
    return HttpResponseRedirect(reverse('ticket_crear', args=[id]))

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
    instruction = "SELECT count(*),ubication,cost,event_id from tickets_ticket WHERE event_id="+str(event)+" GROUP BY cost,ubication,event_id;"
    cursor.execute(instruction)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
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

def save_ticket(cost,ubication,event):
    newTicket = Ticket(cost=cost,ubication=ubication,event=event,state='Disponible')
    newTicket.save()

def delete_ticket(id,ubication,case):
    if case =='one':
        Ticket.objects.filter(event=id).filter(ubication=ubication).last().delete()
    if case =='all':
        Ticket.objects.filter(event=id).filter(ubication=ubication).delete()

