from django.shortcuts import render,redirect
from apps.reports.forms import ByEventsForms, ByDateRangeForms
from apps.tickets.models import Ticket
from apps.sales.models import Bill
import datetime

def index(request):
    return render(request, 'reports/reports.html')

def reportByEvents(request):

    print("entre")
    form = ByEventsForms()
    print("ey") 
    if request.method == 'POST':
        form = ByEventsForms(request.POST)
        selected_event = form['events'].value()
        print(selected_event)
        avalibles =reportByEventAvalibles(int(selected_event))
        sales = reportByEventSale(int(selected_event))
        dailySales =  reportByDailySales()
        context = {'sales':sales,'avalibles':avalibles,'dailySales':dailySales,'form':form}
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
    # print(sales)
    # context = {'sales': str(sales)}
    # return render(request, 'reports/reports.html',context)
    return str(sales)

def graphicsReport(request):
    return render(request, 'reports/graphicsReports.html')

def dailyReport(request):
    return render(request, 'reports/dailySales.html')

def sellerReport(request):
    return render(request, 'reports/sellerReport.html')

def reportByDateRange(request):

    form = ByDateRangeForms()

    if request.method == 'POST':
        form = ByDateRangeForms(request.POST)
        dateInitial = form['dateInitial'].value()
        dateFinal = form['dateFinal'].value()
        print(dateInitial)
        # avalibles =reportByEventAvalibles(int(selected_event))
        # sales = reportByEventSale(int(selected_event))
        # dailySales =  reportByDailySales()
        # context = {'sales':sales,'avalibles':avalibles,'dailySales':dailySales,'form':form}
        return render(request, 'reports/dateRange.html')#A donde debo ir si gano 

    else:
        return render(request, 'reports/dateRange.html',{'form': form})#El mismo lugar donde hice la peticion 
