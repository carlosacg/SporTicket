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
        dbname=sport_db \
        user=andres \
        password=123456")
    return conn


def insertTickets(quantity,ubication,event,cost,state):
    x=0
    while x < int(quantity):        
        save_data(ubication,event,cost,state) 
        x+=1

def generateTickets(request):
    ticket = Ticket.objects.all()
    context = {'tickets':ticket}
    event_type=get_data(str(Event.objects.latest('id')))
    if event_type == 'BEISBOL': 
        if request.method == 'POST':
            form = BaseballForm(request.POST)
            if form.is_valid():
                cost=form['cost'].value()
                ubication=form['ubication'].value()
                quantity=form['quantity'].value()
                state=form['state'].value()
                event_type=get_data(str(Event.objects.latest('id')))
                print(event_type)
                print(cost+"-"+ubication+"-"+quantity+"-"+str(Event.objects.latest('id'))+"-"+state)
                insertTickets(quantity,ubication,str(Event.objects.latest('id')),cost,state) 
            return redirect('tickets/generateTicket.html')
        else:
            form = BaseballForm()
        return render(request, 'tickets/generateTicket.html',{'form':form},context)
    else:
        if request.method == 'POST':
            form = TicketForm(request.POST)
            if form.is_valid():
                cost=form['cost'].value()
                ubication=form['ubication'].value()
                quantity=form['quantity'].value()
                state=form['state'].value()
                event_type=get_data(str(Event.objects.latest('id')))
                print(event_type)
                print(cost+"-"+ubication+"-"+quantity+"-"+str(Event.objects.latest('id'))+"-"+state)
                insertTickets(quantity,ubication,str(Event.objects.latest('id')),cost,state)
                updateCapacityEvent(str(Event.objects.latest('id')),quantity) 
            return redirect('tickets/generateTicket.html')
        else:
            form = TicketForm()
        return render(request, 'tickets/generateTicket.html',{'form':form},context)
    

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

def updateCapacityEvent(event,newCapacity):
    conn = connect()
    cursor = conn.cursor()
    instruction = "UPDATE events_event SET capacity=capacity+"+newCapacity+" WHERE id="+event+";"
    print (instruction)
    cursor.execute(instruction)
    conn.commit()
    conn.close()

