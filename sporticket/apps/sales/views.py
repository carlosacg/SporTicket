from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import CreateView, View, TemplateView
from django.urls import reverse_lazy,reverse
from django.dispatch import receiver
from apps.events.models import *
from apps.location.models import *
from .models import Bill
from apps.tickets.models import Ticket
from django.contrib.auth.models import User
from django.db import connection 
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt,csrf_protect 
from .forms import BillForm, AddTicketsForm, BuyTicketsLocationForm
import time
import json
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
		event = Event.objects.filter(state="Activo")
		context = {'events':event}
		return render(request,'sales/viewsEvent.html',context)

@permission_required('users.Vendedor' ,reverse_lazy('evento_listar_compras'))
def listEvent1(request):
		event = Event.objects.filter(state="Activo")
		print (event)
		context = {'events':event}
		return render(request,'sales/saleEvent.html',context)

@permission_required('users.Vendedor' ,reverse_lazy('evento_listar_compras'))
def createSale(request,id):
	hora = time.strftime("%c")
	event = Event.objects.get(id=id)
	if request.method=='POST':
		#form = BuyTicketsForm(request.POST)
		ubication=form['ubication'].value()
		quantity=form['quantity'].value()
		avalible_tickets = get_avalible_tickets(id,ubication)
	#else:
		#form = BuyTicketsForm()
	#tickets=getListTicketsSolds(bill_id)
	tickets_avalibles=getListTicketsAvalibles(event)
	print (tickets_avalibles)
	context = {'event':event,'hora':hora,'avalibleTicket':tickets_avalibles}
	return render(request,'sales/createSale.html',context)

def createShopAjax(request,id):
	bill=Bill.objects.all().last()
	if bill == None:
		bill_id=1
	else:
		bill_id=int(bill.id)+1
		
	hora = time.strftime("%c")
	event = Event.objects.get(id=id)
	tickets_avalibles=getListTicketsAvalibles(event)
	context = {'event':event,'hora':hora,'avalibleTicket':tickets_avalibles,'bill':bill_id}
	return render(request,'sales/createShop.html',context)

class GetDataAjaxView(TemplateView):

	def get(self,request, *args, **kwargs):
		quantitys = json.loads(request.GET['jsonQuantitys'])
		ubications = json.loads(request.GET['jsonUbications'])
		event_id =request.GET['event_id']
		pago =request.GET['pago']
		x=0
		bill=createBillAjax(request,pago)
		while x < int(len(ubications)):        
			location=Location.objects.get(name=str(ubications[x]))
			avalible_tickets=get_avalible_tickets(event_id,str(location.id))
			add_shopping(bill,avalible_tickets,quantitys[x],len(avalible_tickets))
			x+=1
		return HttpResponse("data")


def createBillAjax(request,payment_method):
	create_bill(request)
	bill_id=Bill.objects.all().last()
	bill_id.payment_method=payment_method
	bill_id.save()
	print('CREO FACTURA')
	return bill_id

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
