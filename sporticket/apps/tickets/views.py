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
    ticket = Ticket.objects.all()
    event =  Event.objects.get(id=id)
    event_type=event.event_type
    print(event_type)
    object = Event()

    if event_type == 'Beisbol':  #SI EL EVENTO CREADO FUE TIPO BEISBOL
        if request.method == 'POST':
            form = BaseballForm(request.POST)
            if form.is_valid():
                higtCost=form['costHigth'].value()
                mediumCost=form['costMediun'].value()
                lowCost=form['costLow'].value()
                higthZone=form['higthZone'].value()
                mediumZone=form['mediumZone'].value()
                lowZone=form['lowZone'].value()
                print(event_type)
                print(higtCost+"-"+higthZone+"-"+mediumCost+"-"+mediumZone+"-"+lowZone+"-"+lowCost)
                insertTickets(higthZone,'Zona alta', event, higtCost,'Disponible')
                insertTickets(mediumZone,'Zona media', event, mediumCost,'Disponible')
                insertTickets(lowZone,'Zona baja', event, lowCost,'Disponible')
                arrayTicket=getListTicket(event.id) 
                quantity=int(higthZone)+int(mediumZone)+int(lowZone)
                print (quantity)
                updateCapacityEvent( event.id,str(quantity)) 
            return HttpResponseRedirect(reverse('ticket_crear', args=[id]))
        else:
            form = BaseballForm()
        arrayTicket=getListTicket(str(event.id))
        context = {'tickets':arrayTicket,'form':form}
        
        return render(request, 'tickets/generateTicketBaseball.html',context)
    else:                       #SI EL EVENTO CREADO FUE FUTBOL O TENIS
        if request.method == 'POST':
            form = TicketForm(request.POST)
            if form.is_valid():
                northCost=form['costNorth'].value()
                southCost=form['costSouth'].value()
                eastCost=form['costEast'].value()
                westCost=form['costWest'].value()
                northZone=form['northZone'].value()
                southZone=form['southZone'].value()
                eastZone=form['eastZone'].value()
                westZone=form['westZone'].value()
                
                insertTickets(northZone,'Tribuna norte', event,northCost,'Disponible')
                insertTickets(southZone,'Tribuna sur', event,southCost,'Disponible')
                insertTickets(eastZone,'Tribuna oriente', event,eastCost,'Disponible')                 
                insertTickets(westZone,'Tribuna occidente',event,westCost,'Disponible')                
                arrayTicket=getListTicket( str(event.id) ) 
                quantity=int(northZone)+int(southZone)+int(eastZone)+int(westZone)
                print (quantity)
                updateCapacityEvent( event.id ,str(quantity)) 
            return HttpResponseRedirect(reverse('ticket_crear', args=[id]))
        else:
            form = TicketForm()
        arrayTicket=getListTicket( str(event.id) )
        context = {'tickets':arrayTicket,'form':form}

        print (arrayTicket)
        return render(request, 'tickets/generateTicket.html',context)
    

def save_data(ubication,event,cost,state):
    newTicket = Ticket(ubication=ubication,event=event,cost=cost,state=state)
    newTicket.save()


def getListTicket(event):
    cursor = connection.cursor()
    instruction = "SELECT count(*),ubication,event_id from tickets_ticket WHERE event_id="+str(event)+" GROUP BY ubication,event_id;"
    cursor.execute(instruction)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows


def updateCapacityEvent(event,newCapacity):
    event = Event.objects.get(id=event)
    event.capacity = newCapacity
    event.save()
