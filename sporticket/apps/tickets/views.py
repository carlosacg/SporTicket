from django.shortcuts import render
from apps.tickets.ticket_form import TicketForm
from apps.tickets.baseball_form import BaseballForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext
import psycopg2
from apps.events.models import Event
from apps.tickets.models import Ticket

# Create your views here.
def connect(): #CONEXION ALTERNATIVA PARA DAR INSTRUCCIONES A LA BD SIN NECESIDAD DE UN FORM
    conn = psycopg2.connect(" \
        dbname=sporticket \
        user=postgres \
        password=1625606")
    return conn


def insertTickets(quantity,ubication,event,cost,state):
    x=0
    while x < int(quantity):        
        save_data(ubication,event,cost,state) 
        x+=1

def generateTickets(request):
    ticket = Ticket.objects.all()
    event_type=get_data(str(Event.objects.latest('id')))
    print(event_type)
    print(request.method)

    if event_type == 'BEISBOL':  #SI EL EVENTO CREADO FUE TIPO BEISBOL
        if request.method == 'POST':
            form = BaseballForm(request.POST)
            if form.is_valid():
                higtCost=form['costHigth'].value()
                mediumCost=form['costMediun'].value()
                lowCost=form['costLow'].value()
                higthZone=form['higthZone'].value()
                mediumZone=form['mediumZone'].value()
                lowZone=form['lowZone'].value()
                event_type=get_data(str(Event.objects.latest('id')))
                print(event_type)
                print(higtCost+"-"+higthZone+"-"+mediumCost+"-"+mediumZone+"-"+lowZone+"-"+lowCost)
                insertTickets(higthZone,'ZONA ALTA',str(Event.objects.latest('id')),higtCost,'DISPONIBLE')
                insertTickets(mediumZone,'ZONA MEDIA',str(Event.objects.latest('id')),mediumCost,'DISPONIBLE')
                insertTickets(lowZone,'ZONA BAJA',str(Event.objects.latest('id')),lowCost,'DISPONIBLE')
                arrayTicket=getListTicket(str(Event.objects.latest('id'))) 
                quantity=int(higthZone)+int(mediumZone)+int(lowZone)
                print (quantity)
                updateCapacityEvent(str(Event.objects.latest('id')),str(quantity)) 
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
                
                insertTickets(northZone,'TRIBUNA NORTE',str(Event.objects.latest('id')),northCost,'DISPONIBLE')
                insertTickets(southZone,'TRIBUNA SUR',str(Event.objects.latest('id')),southCost,'DISPONIBLE')
                insertTickets(eastZone,'TRIBUNA ORIENTE',str(Event.objects.latest('id')),eastCost,'DISPONIBLE')                 
                insertTickets(westZone,'TRIBUNA OCCIDENTE',str(Event.objects.latest('id')),westCost,'DISPONIBLE')                
                arrayTicket=getListTicket(str(Event.objects.latest('id'))) 
                quantity=int(northZone)+int(southZone)+int(eastZone)+int(westZone)
                print (quantity)
                updateCapacityEvent(str(Event.objects.latest('id')),str(quantity)) 
            return redirect('tickets/generateTicket.html')
        else:
            form = TicketForm()
        arrayTicket=getListTicket(str(Event.objects.latest('id')))
        context = {'tickets':arrayTicket,'form':form}

        print (arrayTicket)
        return render(request, 'tickets/generateTicket.html',context)
    

def save_data(ubication,event,cost,state):
    conn = connect()
    cursor = conn.cursor()
    instruction = "INSERT INTO tickets_ticket VALUES (nextval(\'tickets_ticket_id_seq\'),"+cost+",\'"+ubication+"\',"+event+",\'"+state+"\');"
    print (instruction)
    cursor.execute(instruction)
    conn.commit()
    print ("GENERO TICKET")
    conn.close()

def get_data(event):
    conn = connect()
    cursor = conn.cursor()
    instruction = "SELECT event_type FROM events_event WHERE id="+event+";"
    cursor.execute(instruction)
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return str(row[0])

def getListTicket(event):
    conn = connect()
    cursor = conn.cursor()
    instruction = "SELECT count(*),ubication,event_id from tickets_ticket WHERE event_id="+event+" GROUP BY ubication,event_id;"
    cursor.execute(instruction)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows


def updateCapacityEvent(event,newCapacity):
    conn = connect()
    cursor = conn.cursor()
    instruction = "UPDATE events_event SET capacity=capacity+"+newCapacity+" WHERE id="+event+";"
    print (instruction)
    cursor.execute(instruction)
    conn.commit()
    conn.close()
