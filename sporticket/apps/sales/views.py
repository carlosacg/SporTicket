from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from django.dispatch import receiver
from apps.events.models import *
from .models import Bill
from apps.tickets.models import Ticket
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.db import connection 
from .forms import BillForm, AddTicketsForm, BuyTicketsFormBaseball, BuyTicketsForm


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
		create_bill()
		event = Event.objects.all()
		context = {'events':event}
		return render(request,'sales/viewsEvent.html',context)

def createShopping(request,id):
		event = Event.objects.get(id=id)
		bill_id=str(Bill.objects.latest('id').id)
		bill=Bill.objects.get(id=bill_id)
		if event.event_type=='Beisbol':
			if request.method=='POST':
				form = BuyTicketsFormBaseball(request.POST)
				ubication=form['ubication'].value()
				quantity=form['quantity'].value()
				avalible_tickets=get_avalible_tickets(id,ubication)
				add_shopping(bill_id,avalible_tickets,quantity,len(avalible_tickets))
			else:
				form = BuyTicketsFormBaseball()
			tickets=getListTicketsSolds(bill_id)
			tickets_avalibles=getListTicketsAvalibles(event)
			print (tickets_avalibles)
			context = {'event':event,'form':form,'arrayTicket':tickets,'bill':bill_id,'avalibleTicket':tickets_avalibles}
			return render(request,'sales/createShopping.html',context)
		else:
			if request.method=='POST':
				form = BuyTicketsForm(request.POST)
				ubication=form['ubication'].value()
				quantity=form['quantity'].value()
				avalible_tickets=get_avalible_tickets(id,ubication)
				add_shopping(bill_id,avalible_tickets,quantity,len(avalible_tickets))
				tickets=getListTicketsSolds(bill_id)
			else:
				form = BuyTicketsForm()
			tickets=getListTicketsSolds(bill_id)
			tickets_avalibles=getListTicketsAvalibles(event)
			print (tickets_avalibles)
			context = {'event':event,'form':form,'arrayTicket':tickets,'bill':bill_id,'avalibleTicket':tickets_avalibles}
			return render(request,'sales/createShopping.html',context)

def get_event_type(event):
    cursor = connection.cursor()
    instruction = "SELECT event_type FROM events_event WHERE id="+event+";"
    cursor.execute(instruction)
    row = cursor.fetchone()
    connection.commit()
    connection.close()
    return str(row[0])

def getListTicketsSolds(bill):
    cursor = connection.cursor()
    instruction = "SELECT count(*),ubication from tickets_ticket WHERE id_bill_id="+bill+" GROUP BY ubication;"
    cursor.execute(instruction)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows

def getListTicketsAvalibles(event):
    cursor = connection.cursor()
    instruction = "SELECT count(*),ubication from tickets_ticket WHERE state='Disponible' AND event_id="+str(event.id)+" GROUP BY ubication;"
    cursor.execute(instruction)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows

def get_avalible_tickets(event,ubication):
		cursor = connection.cursor()
		instruction = "SELECT id FROM tickets_ticket WHERE event_id="+event+" AND ubication=\'"+ubication+"\' AND state='Disponible';"
		cursor.execute(instruction)
		row = cursor.fetchall()
		connection.commit()
		connection.close()
		return (list(row))

def add_ticket_to_bill(bill,ticket):
		cursor = connection.cursor()
		instruction = "UPDATE tickets_ticket SET id_bill_id="+bill +", state='Vendido' WHERE id="+ticket+";"
		cursor.execute(instruction)
		connection.commit()
		connection.close()

def create_bill():
		cursor = connection.cursor()
		instruction = "INSERT INTO sales_bill VALUES(nextval('sales_bill_id_seq'),now());"
		cursor.execute(instruction)
		connection.commit()
		connection.close()
		
def add_shopping(bill,ticket,quantity,avalibles):
		print("Factura: "+str(bill)+" TICKETS DISPONIBLES: "+str(ticket)+" CANTIDAD SOLICITADA: "+str(quantity)+" DISPONIBLES: "+str(avalibles))
		x=0
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
