from django.shortcuts import render,redirect
from django.http import HttpResponse
from apps.aplicaciones.event_form import EventForm
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from apps.aplicaciones.models import Event
from django.urls import reverse_lazy
# Create your views here.

def index(request):
    return render(request, 'events/insertEvents.html')

def insertEvent(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('events/insertEvents.html')
    else:
        form = EventForm()

    return render(request, 'events/insertEvents.html',{'form':form})

def listEvent(request):
    event = Event.objects.all()
    context = {'events':event}
    return render(request,'events/listEvents.html',context)

def updateEvent(request,id):
    event = Event.objects.get(id=id)
    if request.method =='GET':
        form= EventForm(instance=event)
    else:
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
        return redirect('events/listEvents.html')
    return render(request,'events/insertEvents.html',{'form':form})

def deleteEvent(request,id):
    event = Event.objects.get(id=id)
    print (event.id)
    if request.method=='POST':
        event.delete()
        print ('Se elimino el evento')
        return redirect('evento_listar')
    return render(request,'events/deleteEvents.html',{'event':event})

class EventDelete(DeleteView):
    model = Event
    template_name = 'events/deleteEvents.html'
    success_url = reverse_lazy('evento_listar')

class EventList(ListView):
    model = Event
    template_name ='events/listEvents.html'

class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    template_name ='events/insertEvents.html'
    success_url = reverse_lazy('evento_listar')

class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/insertEvents.html'
    success_url = reverse_lazy('evento_listar')
