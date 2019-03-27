from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView, View, TemplateView
from django.urls import reverse_lazy,reverse
from django.dispatch import receiver
from apps.events.models import *
from apps.location.models import *
from .models import Bill, DetailsBill
from apps.tickets.models import Ticket
from django.contrib.auth.models import User
from django.db import connection 
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt,csrf_protect 
from .forms import BillForm, AddTicketsForm, BuyTicketsLocationForm
import time
import json
from django.contrib.auth.decorators import permission_required
from apps.event_type.models import EventType
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.core.serializers import serialize
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
		context = {'events':event}
		return render(request,'sales/saleEvent.html',context)

@permission_required('users.Vendedor' ,reverse_lazy('evento_listar_compras'))
def viewSales(request):	
	return render(request, 'sales/viewSales.html')

def getDailySales(request):
	if request.is_ajax:
		if request.method == 'GET':
			user = User.objects.get(id=request.user.id)
			date = request.GET.get('dateO')
			bills = Bill.objects.all().filter(id_profile=request.user.id, date_bill=date)
			bills = [ bill_serializer(bill) for bill in bills]
			return HttpResponse(json.dumps(bills,cls=DjangoJSONEncoder), content_type = "application/json")

def bill_serializer(bill):
	return {'id': bill.id, 'metodo_pago': bill.payment_method, 'total': bill.total_bill}

def getIdBillLast():
	bill=Bill.objects.all().last()
	if bill == None:
		return 1
	else:
		return int(bill.id)+1

@permission_required('users.Vendedor' ,reverse_lazy('evento_listar_compras'))
@csrf_exempt
def createSale(request,id):
	user=User.objects.get(id=request.user.id)
	userFullName = user.first_name + " " + user.last_name
	bill_id = getIdBillLast()
	hora = time.strftime("%c")
	event = Event.objects.get(id=id)
	tickets_avalibles=getListTicketsAvalibles(event)
	list_events_type=getListTypeEvents()
	if request.is_ajax:
		if request.method == "POST":
			sale = eval(request.POST.get('post_venta_envio'))
			newBill = Bill(total_bill= sale['total'], id_profile= user, payment_method= sale['metodo_pago'], type_bill='Venta') 
			newBill.save()
			tickets = sale['tickets']
			for ticket in tickets:
				addTicketBill(ticket, newBill)
				addDetailsBill(ticket, newBill)
			return HttpResponse(json.dumps({'status':'success'}), content_type="application/json")
	context = {'event':event,'hora':hora,'avalibleTicket':tickets_avalibles, 'eventType':list_events_type, 'bill':bill_id , 'userFullName':userFullName}
	return render(request,'sales/createSale.html',context)


def getListTypeEvents():
	allTypeEvents = EventType.objects.all()
	return allTypeEvents

def getIdEventType(eventTypeName):
	idEventType = EventType.objects.values('id').filter(name=eventTypeName)
	return idEventType

def getIdEventForName(eventName):
	idEvent = Event.objects.values('id').filter(name=eventName)
	return idEvent

@permission_required('users.Vendedor' ,reverse_lazy('evento_listar_compras'))
def getEventsForTypes(request):
	eventTypeName = request.GET.get('select_buscar')
	idEventType = getIdEventType(eventTypeName)[0]
	eventsForTypes = Event.objects.all().filter(event_type=str(idEventType['id']))
	eventsForTypes = [ event_serializer(eventForType) for eventForType in eventsForTypes]	
	return HttpResponse(json.dumps(eventsForTypes,cls=DjangoJSONEncoder), content_type = "application/json")

def event_serializer(event):
	return {'id':event.id, 'name':event.name, 'initial_date':event.initial_date, 'capacity':event.capacity}

def new_tickets_avalibles(tickets_avalibles):
	return {'count':tickets_avalibles[0], 'name':tickets_avalibles[1], 'cost':tickets_avalibles[2], 'id':tickets_avalibles[3]}

@permission_required('users.Vendedor' ,reverse_lazy('evento_listar_compras'))
def getNewEvent(request):
	eventName = request.GET.get('get_event_selec')
	idEvent = getIdEventForName(eventName)[0]
	event = event_serializer(Event.objects.get(id=str(idEvent['id'])))
	tickets_avalibles=getListTicketsAvalibles(Event.objects.get(id=str(idEvent['id'])))
	tickets_avalibles=[ new_tickets_avalibles(tickets_avalible) for tickets_avalible in tickets_avalibles ]
	contexto = {'event':event,'avalibleTicket':tickets_avalibles}	
	return HttpResponse(json.dumps(contexto,cls=DjangoJSONEncoder), content_type = "application/json")

def addTicketBill(ticketIn, Bill):
	contador = int(ticketIn['cant'])
	for i in range(contador):
		ticket = Ticket.objects.filter(location_id=ticketIn['id_location'], state__exact="Disponible")[0]
		ticket.id_bill = Bill
		ticket.state = "Vendido"
		ticket.save()

def addDetailsBill(ticketIn, Bill):
	detailsBill = DetailsBill(id_location=getLocation(ticketIn['id_location']), eventName=ticketIn['event_name'], cant=ticketIn['cant'], subtotal=ticketIn['subtotal'])
	detailsBill.id_bill = Bill
	detailsBill.save()

@permission_required('users.Vendedor' ,reverse_lazy('evento_listar_compras'))
def getBill(request):
	fullName = request.user.first_name + request.user.last_name
	idBill = request.GET.get('get_bill')
	bill = Bill.objects.get(id=idBill)
	detailsBills = DetailsBill.objects.filter(id_bill=idBill)
	detailsBills=[ detailsBill_serializer(detailsBill) for detailsBill in detailsBills ]
	return HttpResponse(json.dumps({'id':bill.id, 'date':bill.date_bill, 'name':fullName, 'total':bill.total_bill,'detailsBills':detailsBills},cls=DjangoJSONEncoder), content_type = "application/json")

def detailsBill_serializer(detailsBill):
	costo = (detailsBill.subtotal/detailsBill.cant)
	return {'eventName': detailsBill.eventName, 'cant': detailsBill.cant, 'locationName': str(detailsBill.id_location), 'costo': costo, 'subtotal': detailsBill.subtotal}

def getLocationName(idLocation):
	name = Location.objects.values('name').filter(id=idLocation)
	return name[0]['name']

def getLocation(idLocation):
	location = Location.objects.get(id=idLocation)
	return location

#-----------------------------------------
def createShop(request,id):
	hora = time.strftime("%c")
	event = Event.objects.get(id=id)
	tickets_avalibles=getListTicketsAvalibles(event)
	list_events_type=getListTypeEvents()
	bill_id = 0
	bill=Bill.objects.all().last()
	if bill == None:
		bill_id=1
	else:
		bill_id=int(bill.id)+1
	context = {'event':event,'hora':hora,'avalibleTicket':tickets_avalibles, 'eventType':list_events_type,'bill':bill_id}
	if event.url == "http://localhost:8000":
		context = {'event':event,'hora':hora,'avalibleTicket':tickets_avalibles, 'eventType':list_events_type,'bill':bill_id}
		return render(request,'sales/createShopping.html',context)
	else:
		context = {'event':event}
		return render(request,'sales/eventRefer.html',context)

class GetDataAjaxView(TemplateView):

	def get(self,request, *args, **kwargs):
		quantitys = json.loads(request.GET['jsonQuantitys'])
		ubications = json.loads(request.GET['jsonUbications'])
		pago =request.GET['pago']
		total =request.GET['total']
		x=0
		bill=createBillAjax(request,pago,'Compra',total)
		while x < int(len(ubications)):    
			location=Location.objects.get(id=ubications[x])
			addShopping(location.id,quantitys[x],bill)    
			x+=1
		return JsonResponse({'status':'success'})

def addShopping(id_location,cantidad, Bill):
	contador = int(cantidad)
	for i in range(contador):
		ticket = Ticket.objects.filter(location_id=id_location, state__exact="Disponible")[0]
		ticket.id_bill = Bill
		ticket.state = "Vendido"
		ticket.save()

def createBillAjax(request,payment_method,type_bill,total):
	create_bill(request)
	bill_id=Bill.objects.all().last()
	bill_id.payment_method=payment_method
	bill_id.type_bill=type_bill
	bill_id.total_bill=total
	bill_id.save()
	return bill_id

def listShops(request):
	user=User.objects.get(id=request.user.id)
	print(user.id)
	listShops=getMyShops(user.id)
	print('LISTA COMPRAS')
	print(listShops)
	context = {'listShops':listShops}
	return render(request,'sales/myShops.html',context)

def getMyShops(user):
	cursor = connection.cursor()
	instruction="SELECT count(*),sales_bill.id,sales_bill.total_bill,sales_bill.date_bill FROM events_event,tickets_ticket,sales_bill WHERE tickets_ticket.event_id=events_event.id AND tickets_ticket.id_bill_id=sales_bill.id AND sales_bill.type_bill='Compra' AND sales_bill.id_profile_id="+str(user)+" GROUP BY sales_bill.id,sales_bill.total_bill,sales_bill.date_bill;"
	print(instruction)
	cursor.execute(instruction)
	rows = cursor.fetchall()
	connection.commit()
	connection.close()
	print(rows)
	return rows


def getListTicketsAvalibles(event):
    cursor = connection.cursor()
    instruction = "SELECT count(*),location_location.name,location_location.cost, location_location.id FROM tickets_ticket,location_location WHERE location_location.id=tickets_ticket.location_id AND state='Disponible' AND tickets_ticket.event_id="+str(event.id)+" GROUP BY location_location.name,location_location.cost, location_location.id;"
    cursor.execute(instruction)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows


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

def calculate(ubications, event, quantity):	
	if str(quantity) != '':
		ticket = Ticket.objects.all().filter(event_id=event, ubication=ubications).first()	
		quantityTickets =  int(quantity)
		cost = ticket.cost * quantityTickets

def newSales(request):
	return render(request,'sales/listEventsSale.html')