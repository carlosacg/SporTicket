from django.shortcuts import render
from apps.tickets.ticket_form import TicketForm
from apps.tickets.baseball_form import BaseballForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext
import psycopg2
from apps.events.models import Event
from apps.tickets.models import Ticket
from django.db import connection 

# Create your views here.

def insertTickets(quantity,ubication,event,cost,state):
    x=0
    while x < int(quantity):        
        save_data(ubication,event,cost,state) 
        x+=1

def generateTickets(request):
    ticket = Ticket.objects.all()
    event_type=Event.objects.all().last().event_type
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
                insertTickets(higthZone,'Zona alta', Event.objects.all().last(),higtCost,'Disponible')
                insertTickets(mediumZone,'Zona media', Event.objects.all().last(),mediumCost,'Disponible')
                insertTickets(lowZone,'Zona baja', Event.objects.all().last(),lowCost,'Disponible')
                arrayTicket=getListTicket(object.lastEventId()) 
                quantity=int(higthZone)+int(mediumZone)+int(lowZone)
                print (quantity)
                updateCapacityEvent( object.lastEventId(),str(quantity)) 
            return redirect('tickets/generateTicketBaseball.html')
        else:
            form = BaseballForm()
        arrayTicket=getListTicket(str(Event.objects.latest('id')))
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
                
                insertTickets(northZone,'Tribuna norte', Event.objects.all().last(),northCost,'Disponible')
                insertTickets(southZone,'Tribuna sur', Event.objects.all().last(),southCost,'Disponible')
                insertTickets(eastZone,'Tribuna oriente', Event.objects.all().last(),eastCost,'Disponible')                 
                insertTickets(westZone,'Tribuna occidente', Event.objects.all().last(),westCost,'Disponible')                
                arrayTicket=getListTicket( object.lastEventId()) 
                quantity=int(northZone)+int(southZone)+int(eastZone)+int(westZone)
                print (quantity)
                updateCapacityEvent( object.lastEventId(),str(quantity)) 
            return redirect('tickets/generateTicket.html')
        else:
            form = TicketForm()
        arrayTicket=getListTicket( object.lastEventId())
        context = {'tickets':arrayTicket,'form':form}

        print (arrayTicket)
        return render(request, 'tickets/generateTicket.html',context)
    

def save_data(ubication,event,cost,state):
    newTicket = Ticket(ubication=ubication,event=event,cost=cost,state=state)
    newTicket.save()


def getListTicket(event):
    cursor = connection.cursor()
    instruction = "SELECT count(*),ubication,event_id from tickets_ticket WHERE event_id="+event+" GROUP BY ubication,event_id;"
    cursor.execute(instruction)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows


def updateCapacityEvent(event,newCapacity):
    event = Event.objects.get(id=event)
    event.capacity = newCapacity
    event.save()
