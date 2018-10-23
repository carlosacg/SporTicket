from django.shortcuts import render
from apps.tickets.ticket_form import TicketForm
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import RequestContext
import psycopg2
from apps.events.models import Event

# Create your views here.
def connect(): #CONEXION ALTERNATIVA PARA DAR INSTRUCCIONES A LA BD SIN NECESIDAD DE UN FORM
    conn = psycopg2.connect(" \
        dbname=sport_db \
        user=andres \
        password=123456")
    return conn

def generateTickets(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cost=form['cost'].value()
            ubication=form['ubication'].value()
            quantity=form['quantity'].value()
            state=form['state'].value()
            print (Event.objects.latest('id'))
            print(cost+"-"+ubication+"-"+quantity+"-"+str(Event.objects.latest('id'))+"-"+state)
            insertTickets(quantity,ubication,str(Event.objects.latest('id')),cost,state) 
        return redirect('events/listEvents.html')
    else:
        form = TicketForm()
    return render(request, 'tickets/generateTicket.html',{'form':form})



def insertTickets(quantity,ubication,event,cost,state):
    x=0
    while x < int(quantity):        
        save_data(ubication,event,cost,state) 
        x+=1




def save_data(ubication,event,cost,state):
    conn = connect()
    cursor = conn.cursor()
    instruction = "INSERT INTO tickets_ticket VALUES (nextval(\'tickets_ticket_id_seq\'),"+cost+",\'"+ubication+"\',"+event+",\'"+state+"\');"
    print (instruction)
    cursor.execute(instruction)
    conn.commit()
    print ("GENERO TICKET")
    conn.close()