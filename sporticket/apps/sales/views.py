from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.dispatch import receiver
from apps.events.models import *
from .models import Bill
from apps.tickets.models import Ticket
from django.views.generic import ListView,CreateView, UpdateView, DeleteView

from .forms import BillForm, AddTicketsForm, BuyTicketsFormBaseball, BuyTicketsForm

def connect(): #CONEXION ALTERNATIVA PARA DAR INSTRUCCIONES A LA BD SIN NECESIDAD DE UN FORM
    conn = psycopg2.connect(" \
        dbname=sport_db \
        user=andres \
        password=1625606")
    return conn

def index_sale(request):
    return render(request, 'sales/createSale.html')

class BillCreate(CreateView):
	model = Bill
	template_name = 'sales/base.html'
	form_class = BillForm
	s_form_class = AddTicketsForm
	success_url = reverse_lazy('sales:index')

	def get_context_data(self, **kwargs):
		context = super(BillCreate, self).get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.s_form_class(self.request.GET)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.s_form_class(request.POST)
		if form.is_valid() and form2.is_valid():
			bill = form.save()
			ticket = tickets.objects.get(pk=form2.id)
			ticket.id_bill = bill
			ticket.state = 'Vendido'
			ticket.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

class EventList(ListView):
    model = Event
    template_name ='sales/viewsEvent.html'

def createShopping(request,id):
		event = Event.objects.get(id=id)
		print (event.event_type+"-"+id)
		if event.event_type=='Beisbol':
			if request.method=='POST':
				form = BuyTicketsFormBaseball(request.POST)
				ubication=form['ubication'].value()
				quantity=form['quantity'].value()
				print(ubication+"-"+quantity)
				avalible_tickets=get_avalible_tickets(id,ubication)
				print(len(avalible_tickets))
				create_bill()
				#OBTENIDO EL ID DE LA FACTURA CREADA LLAMAMOS A LA FUNCION add_shopping
				#
			else:
				form = BuyTicketsFormBaseball()
			context = {'event':event,'form':form}
			return render(request,'sales/createShopping.html',context)
		else:
			if request.method=='POST':
				form = BuyTicketsForm(request.POST)
				ubication=form['ubication'].value()
				quantity=form['quantity'].value()
				avalible_tickets=get_avalible_tickets(id,ubication)
			else:
				form = BuyTicketsForm()
			
			context = {'event':event,'form':form}
			return render(request,'sales/createShopping.html',context)

def get_event_type(event):
    conn = connect()
    cursor = conn.cursor()
    instruction = "SELECT event_type FROM events_event WHERE id="+event+";"
    cursor.execute(instruction)
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return str(row[0])

def get_avalible_tickets(event,ubication):
		conn = connect()
		cursor = conn.cursor()
		instruction = "SELECT id FROM tickets_ticket WHERE event_id="+event+" AND ubication=\'"+ubication+"\' AND state='Disponible';"
		cursor.execute(instruction)
		row = cursor.fetchall()
		print(len(list(row)))#CANTIDAD DATOS
		print(str(row[0])[1:2])#ID 
		conn.commit()
		conn.close()
		return (list(row))

def add_ticket_to_bill(bill,ticket):
		conn = connect()
		cursor = conn.cursor()
		instruction = "UPDATE tickets_ticket SET id_bill="+bill +"WHERE id="+ticket+";"
		cursor.execute(instruction)
		row = cursor.fetchall()
		conn.commit()
		conn.close()

def create_bill():
		conn = connect()
		cursor = conn.cursor()
		instruction = "INSERT INTO sales_bill VALUES(nextval('sales_bill_id_seq'),now());"
		cursor.execute(instruction)
		conn.commit()
		conn.close()

def add_shopping(bill,ticket,quantity,avalibles):
		x=0
		if int(quantity) < int(avalibles): 
			while x < int(quantity):        
				add_ticket_to_bill(bill,str(ticket[x])[1:2]) 
				x+=1
		else:
			while x < int(avalibles):        
				add_ticket_to_bill(bill,str(ticket[x])[1:2])
				x+=1
