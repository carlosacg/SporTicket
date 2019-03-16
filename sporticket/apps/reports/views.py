from django.shortcuts import render,redirect
from apps.reports.forms import ByEventsForms, ByDateRangeForms
from apps.tickets.models import Ticket
from apps.sales.models import Bill
import datetime
from django.contrib.auth.decorators import login_required,permission_required
from django.urls import reverse_lazy, reverse
from django.db.models import Count
from apps.users.models import *

@permission_required('users.Gerente' ,reverse_lazy('base'))
def index(request):
    return render(request, 'reports/reports.html')

def base(request):
    return render(request, 'base/base.html')

@permission_required('users.Gerente' ,reverse_lazy('base'))
def reportByEvents(request):

    form = ByEventsForms()
    if request.method == 'POST':
        form = ByEventsForms(request.POST)
        selected_event = form['events'].value()
        avalibles =reportByEventAvalibles(int(selected_event))
        sales = reportByEventSale(int(selected_event))
        context = {'sales':sales,'avalibles':avalibles,'form':form}
        return render(request, 'reports/saleEvents.html',context)#A donde debo ir si gano 

    else:
        return render(request, 'reports/saleEvents.html',{'form': form})#El mismo lugar donde hice la peticion 


def reportByEventAvalibles(event_id):

    print(event_id)
    ticket = Ticket.objects.all().filter(state='Disponible', event_id = event_id).count()
    print(ticket)
    return ticket

def reportByEventSale(event_id):

    ticket = Ticket.objects.all().filter(state='Vendido', event_id = event_id).count()
    print(ticket)
    return ticket

def reportByDailySales():

    currentDate = datetime.datetime.now()
    currentDateFormat =  str(currentDate.year) +"-"+ str(currentDate.month)+"-"+str(currentDate.day)
    sales = Bill.objects.all().filter(date_bill__range=(currentDateFormat,currentDateFormat)).count()
    return sales

def graphicsReport(request):
    return render(request, 'reports/graphicsReports.html')

def dailyReport(request):

    dailySales =  reportByDailySales()
    context = {'dailySales':dailySales}
    return render(request, 'reports/dateRange.html',context)#A donde debo ir si gano 

def sellerReport(request):

    users = User.objects.annotate(total_sales=Count('my_bills')).order_by('-total_sales')    
    bestUser = users.first().first_name
    context = {'bestUser':bestUser}
    return render(request, 'reports/sellerReport.html', context)

@permission_required('users.Gerente' ,reverse_lazy('base'))
def reportByDateRange(request):

    form = ByDateRangeForms()

    if request.method == 'POST':
        form = ByDateRangeForms(request.POST)
        dateInitial = form['dateInitial'].value()
        dateFinal = form['dateFinal'].value()
        print(dateInitial)
        context = {'dateInitial':dateInitial}
        return render(request, 'reports/dateRange.html', context)#A donde debo ir si gano 

    else:
        return render(request, 'reports/dateRange.html',{'form': form})#El mismo lugar donde hice la peticion 
