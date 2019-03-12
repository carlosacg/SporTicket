from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.dispatch import receiver
from apps.events.models import *
from apps.location.models import *
from .models import Bill
from apps.tickets.models import Ticket
from django.contrib.auth.models import User
from django.db import connection 
from .forms import BillForm, AddTicketsForm, BuyTicketsLocationForm
import time
from django.contrib.auth.decorators import permission_required

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

def listEvent(request):
		create_bill(request)
		event = Event.objects.filter(state="Activo")
		print (event)
		context = {'events':event}
		return render(request,'sales/viewsEvent.html',context)

@permission_required('users.Vendedor' ,reverse_lazy('evento_listar_compras'))
def listEvent1(request):
		event = Event.objects.filter(state="Activo")
		print (event)
		context = {'events':event}
		return render(request,'sales/saleEvent.html',context)

def createSale(request,id):
	hora = time.strftime("%c")
	event = Event.objects.get(id=id)
	if request.method=='POST':
		form = BuyTicketsForm(request.POST)
		ubication=form['ubication'].value()
		quantity=form['quantity'].value()
		avalible_tickets = get_avalible_tickets(id,ubication)
	else:
		form = BuyTicketsForm()
	#tickets=getListTicketsSolds(bill_id)
	tickets_avalibles=getListTicketsAvalibles(event)
	print (tickets_avalibles)
	context = {'event':event,'form':form,'hora':hora,'avalibleTicket':tickets_avalibles}
	return render(request,'sales/createSale.html',context)

def createShop(request,id):
	event = Event.objects.get(id=id)
	bill_id=Bill.objects.all().last()
	if request.method=='POST':
		form=BuyTicketsLocationForm(request.POST)
		if form.is_valid:
			location=form['location'].value()
			quantity=form['quantity'].value()
			payment_method=form['payment'].value()
			print(location)
			bill_id=Bill.objects.all().last()
			bill_id.payment_method=payment_method
			bill_id.save()
			avalible_tickets=get_avalible_tickets(id,location)
			add_shopping(bill_id,avalible_tickets,quantity,len(avalible_tickets))

	else:
		form=BuyTicketsLocationForm(request.POST)
		form.query(event)
	tickets=getListTicketsSolds(bill_id)
	tickets_avalibles=getListTicketsAvalibles(event)
	context = {'event':event,'form':form,'arrayTicket':tickets,'bill':bill_id,'avalibleTicket':tickets_avalibles}
	return render(request,'sales/createShopping.html',context)


def getListTicketsSolds(bill):
    cursor = connection.cursor()
    instruction = "SELECT count(*),location_location.name,location_location.cost FROM tickets_ticket,location_location WHERE location_location.id=tickets_ticket.location_id AND id_bill_id="+str(bill.id)+" GROUP BY location_location.name,location_location.cost;"
    cursor.execute(instruction)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows

def getListTicketsAvalibles(event):
    cursor = connection.cursor()
    instruction = "SELECT count(*),location_location.name,location_location.cost FROM tickets_ticket,location_location WHERE location_location.id=tickets_ticket.location_id AND state='Disponible' AND tickets_ticket.event_id="+str(event.id)+" GROUP BY location_location.name,location_location.cost;"
    cursor.execute(instruction)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows

def get_avalible_tickets(event,location):
	cursor = connection.cursor()
	instruction = "SELECT id FROM tickets_ticket WHERE event_id="+event+" AND location_id="+location+" AND state='Disponible';"
	print(instruction)
	cursor.execute(instruction)
	row = cursor.fetchall()
	connection.commit()
	connection.close()
	return (list(row))

def add_ticket_to_bill(bill,ticket):
	ticket = Ticket.objects.get(id=ticket)
	ticket.id_bill=bill
	ticket.state='Vendido'
	ticket.save()


def create_bill(request):
	user=User.objects.get(id=request.user.id)
	print(user.id)
	bill = Bill(id_profile=user)
	bill.save()
		
def add_shopping(bill,ticket,quantity,avalibles):
		print("Factura: "+str(bill)+" TICKETS DISPONIBLES: "+str(ticket)+" CANTIDAD SOLICITADA: "+str(quantity)+" DISPONIBLES: "+str(avalibles))
		x=0
		if str(quantity) != '':
			if int(quantity) < int(avalibles): 
				while x < int(quantity):
					if int(len(str(ticket[x])))==4:
						add_ticket_to_bill(bill,str(ticket[x])[1:2])
					if int(len(str(ticket[x])))==5:
						add_ticket_to_bill(bill,str(ticket[x])[1:3])
					if int(len(str(ticket[x])))==6:
						add_ticket_to_bill(bill,str(ticket[x])[1:4])
					if int(len(str(ticket[x])))==7:
						add_ticket_to_bill(bill,str(ticket[x])[1:5])
					if int(len(str(ticket[x])))==8:
						add_ticket_to_bill(bill,str(ticket[x])[1:6])
					if int(len(str(ticket[x])))==9:
						add_ticket_to_bill(bill,str(ticket[x])[1:7])
					if int(len(str(ticket[x])))==10:
						add_ticket_to_bill(bill,str(ticket[x])[1:8])
					if int(len(str(ticket[x])))==11:
						add_ticket_to_bill(bill,str(ticket[x])[1:9])
					x+=1
			else:
				while x < int(avalibles):
					if int(len(str(ticket[x])))==4:
						add_ticket_to_bill(bill,str(ticket[x])[1:2])
					if int(len(str(ticket[x])))==5:
						add_ticket_to_bill(bill,str(ticket[x])[1:3])
					if int(len(str(ticket[x])))==6:
						add_ticket_to_bill(bill,str(ticket[x])[1:4])
					if int(len(str(ticket[x])))==7:
						add_ticket_to_bill(bill,str(ticket[x])[1:5])
					if int(len(str(ticket[x])))==8:
						add_ticket_to_bill(bill,str(ticket[x])[1:6])
					if int(len(str(ticket[x])))==9:
						add_ticket_to_bill(bill,str(ticket[x])[1:7])
					if int(len(str(ticket[x])))==10:
						add_ticket_to_bill(bill,str(ticket[x])[1:8])
					if int(len(str(ticket[x])))==11:
						add_ticket_to_bill(bill,str(ticket[x])[1:9])
					x+=1

def calculate(ubications, event, quantity):	
	if str(quantity) != '':
		ticket = Ticket.objects.all().filter(event_id=event, ubication=ubications).first()	
		quantityTickets =  int(quantity)
		cost = ticket.cost * quantityTickets
