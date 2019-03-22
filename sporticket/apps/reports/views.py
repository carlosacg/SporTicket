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
    return render(request, 'reports/dailySales.html',context)#A donde debo ir si gano 

def sellerReport(request):

    totalUsers = User.objects.all().count()
    if totalUsers >= 5:
                
        users = User.objects.annotate(total_sales=Count('my_bills')).order_by('-total_sales')   

        firstSallerN = users[0].first_name
        firstSallerL = users[0].last_name
        total_salesOne =  users[0].total_sales
        fullDataOne = firstSallerN + " "+firstSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesOne)
        secondSallerN = users[1].first_name
        secondSallerL = users[1].last_name
        total_salesTwo =  users[1].total_sales
        fullDataTwo = secondSallerN + " " +secondSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesTwo)
        threeSallerN = users[2].first_name
        threeSallerL = users[2].last_name
        total_salesThree =  users[2].total_sales
        fullDataThree = threeSallerN + " " + threeSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesThree)
        fourSallerN = users[3].first_name
        fourSallerL = users[3].last_name
        total_salesFour =  users[3].total_sales
        fullDataFour = fourSallerN + " " + fourSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesFour)
        fiveSallerN = users[4].first_name
        fiveSallerL = users[4].last_name
        total_salesFive =  users[4].total_sales
        fullDataFive = fiveSallerN +  " " + fiveSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesFive)

        context = {'fullDataOne':fullDataOne, 'fullDataTwo':fullDataTwo, 'fullDataThree':fullDataThree,  'fullDataFour':fullDataFour, 'fullDataFive':fullDataFive}
        return render(request, 'reports/sellerReport.html', context)
    
    else:
        if totalUsers == 4:

            users = User.objects.annotate(total_sales=Count('my_bills')).order_by('-total_sales')   
            firstSallerN = users[0].first_name
            firstSallerL = users[0].last_name
            total_salesOne =  users[0].total_sales
            fullDataOne = firstSallerN + " "+firstSallerL +" CON UN TOTAL DE VENTAS: " +  str(total_salesOne)
            secondSallerN = users[1].first_name
            secondSallerL = users[1].last_name
            total_salesTwo =  users[1].total_sales
            fullDataTwo = secondSallerN + " " +secondSallerL +" CON UN TOTAL DE VENTAS: " +str(total_salesTwo)
            threeSallerN = users[2].first_name
            threeSallerL = users[2].last_name
            total_salesThree =  users[2].total_sales
            fullDataThree = threeSallerN + " " + threeSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesThree)
            fourSallerN = users[3].first_name
            fourSallerL = users[3].last_name
            total_salesFour =  users[3].total_sales
            fullDataFour = fourSallerN + " " + fourSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesFour)
            context = {'fullDataOne':fullDataOne, 'fullDataTwo':fullDataTwo, 'fullDataThree':fullDataThree,  'fullDataFour':fullDataFour, 'fullDataFive':fullDataFive}
            return render(request, 'reports/sellerReport.html', context)

        else:
            if totalUsers == 3:
                
                users = User.objects.annotate(total_sales=Count('my_bills')).order_by('-total_sales')   
                firstSallerN = users[0].first_name
                firstSallerL = users[0].last_name
                total_salesOne =  users[0].total_sales
                fullDataOne = firstSallerN + " "+firstSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesOne)
                secondSallerN = users[1].first_name
                secondSallerL = users[1].last_name
                total_salesTwo =  users[1].total_sales
                fullDataTwo = secondSallerN + " " +secondSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesTwo)
                threeSallerN = users[2].first_name
                threeSallerL = users[2].last_name
                total_salesThree =  users[2].total_sales
                fullDataThree = threeSallerN + " " + threeSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesThree)
                fullDataFour = "No contamos con un cuarto vendedor"
                fullDataFive = "No contamos con un cuarto vendedor"
                context = {'fullDataOne':fullDataOne, 'fullDataTwo':fullDataTwo, 'fullDataThree':fullDataThree,  'fullDataFour':fullDataFour, 'fullDataFive':fullDataFive}
                return render(request, 'reports/sellerReport.html', context)

            else:
                if totalUsers == 2:
                    
                    users = User.objects.annotate(total_sales=Count('my_bills')).order_by('-total_sales')   
                    firstSallerN = users[0].first_name
                    firstSallerL = users[0].last_name
                    total_salesOne =  users[0].total_sales
                    fullDataOne = firstSallerN + " "+firstSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesOne)
                    secondSallerN = users[1].first_name
                    secondSallerL = users[1].last_name
                    total_salesTwo =  users[1].total_sales
                    fullDataTwo = secondSallerN + " " +secondSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesTwo)
                    fullDataThree = "No contamos con un tercero vendedor"
                    fullDataFour = "No contamos con un cuarto vendedor"
                    fullDataFive = "No contamos con un quinto vendedor"
                    context = {'fullDataOne':fullDataOne, 'fullDataTwo':fullDataTwo, 'fullDataThree':fullDataThree,  'fullDataFour':fullDataFour, 'fullDataFive':fullDataFive}
                    return render(request, 'reports/sellerReport.html', context)
                
                else:
                    if totalUsers == 1:
                        
                        users = User.objects.annotate(total_sales=Count('my_bills')).order_by('-total_sales')   
                        firstSallerN = users[0].first_name
                        firstSallerL = users[0].last_name
                        total_salesOne =  users[0].total_sales
                        fullDataOne = firstSallerN + " "+firstSallerL +" CON UN TOTAL DE VENTAS: " + str(total_salesOne)
                        fullDataTwo = "No contamos con un segundo vendedor"
                        fullDataThree = "No contamos con un tercero vendedor"
                        fullDataFour = "No contamos con un cuarto vendedor"
                        fullDataFive = "No contamos con un quinto vendedor"
                        context = {'fullDataOne':fullDataOne, 'fullDataTwo':fullDataTwo, 'fullDataThree':fullDataThree,  'fullDataFour':fullDataFour, 'fullDataFive':fullDataFive}
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
        return render(request, 'reports/dateRange.html', context)
    else:
        return render(request, 'reports/dateRange.html',{'form': form}) 