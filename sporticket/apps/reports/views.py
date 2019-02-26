from django.shortcuts import render
from apps.reports.forms import ByEventsForms

def index_sale(request):
    if request.method == 'POST':
        form = ByEventsForms(request.POST)
        return redirect('home')
    else:
        form = ByEventsForms()  
    return render(request, 'reports/reports.html',{'form': form})
    
def dasd(request):
    form = ByMovementReportForm()
    selected_evebt = None
    if request.method == 'POST':
        form = ByEventsForms(request.POST)
        if form.is_valid():
            selected_event = form.events
            print(select_event)
            return redirect('home')
        else:
            form = ByEventsForms()  
        return render(request, 'reports/reports.html',{'form': form})

def reportByEvent(event_id):
    ticket = Ticket.objects.all().filter(state='Disponible', event_id = event_id) 
    return ticket.count()

def reportByEvent(event_id):
    ticket = Ticket.objects.all().filter(state='Vendido', event_id = event_id) 
    return ticket.count()
