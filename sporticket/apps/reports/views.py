from django.shortcuts import render,redirect
from apps.reports.forms import ByEventsForms
from apps.tickets.models import Ticket

    
def report_f(request, ):
    print("entre")
    form = ByEventsForms()
    print("ey") 
    if request.method == 'POST':
        form = ByEventsForms(request.POST)
        selected_event = form['events'].value()
        print(selected_event)
        avalibles =reportByEventAvalibles(int(selected_event))
        sales = reportByEventSale(int(selected_event))
        context = {'sales':sales,'avalibles':avalibles,'form':form}
        return render(request, 'reports/reports.html',context)

    else:
        return render(request, 'reports/reports.html',{'form': form})


def reportByEventAvalibles(event_id):
    print(event_id)
    ticket = Ticket.objects.all().filter(state='Disponible', event_id = event_id).count()
    print(ticket)
    return ticket

def reportByEventSale(event_id):
    ticket = Ticket.objects.all().filter(state='Vendido', event_id = event_id).count()
    return ticket
