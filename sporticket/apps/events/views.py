from django.shortcuts import render,redirect
from django.http import HttpResponse
from apps.events.forms import EventForm
from apps.events.view_event import ViewEvent
from apps.events.forms import UploadForm
from apps.events.forms import ImageForm
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from apps.events.models import *
from django.urls import reverse_lazy
import json
from apps.tickets.models import Ticket
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

def index(request):
    return render(request, 'base/base.html')

def insertEvent(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            object = Event()
            event = Event.objects.get(id=str(object.lastEventId()))
            event.image="./images/porDefecto.jpg"
            event.save()
        return redirect('uploadImage.html'+str(object.lastEventId()))
    else:
        form = EventForm()
    return render(request, 'events/insertEvents.html',{'form':form})

def listEvent(request):
    event = Event.objects.all()
    context = {'events':event}
    return render(request,'events/listEvents.html',context)

def uploadFile(request):
    if request.method == 'POST':
        formulario = UploadForm(request.POST, request.FILES)
        if formulario.is_valid():
            newdoc = Document(filename = request.POST['filename'],docfile = request.FILES['docfile'])
            newdoc.save(formulario)
            ruta=request.FILES.get('docfile').name
            with open('./documents/'+ruta) as file:
                datos = json.load(file)
            for dato in datos:
                print (dato['event_type'])
                object = Event()
                print(dato['name'],dato['initial_dale'],dato['initial_time'],dato['place'],dato['url'],dato['state'],dato['capacity'],dato['visitor'],dato['local'],dato['event_type'])
                object.save_data(dato['name'],dato['initial_dale'],dato['initial_time'],dato['place'],dato['url'],dato['state'],dato['capacity'],dato['visitor'],dato['local'],dato['event_type'])
                print('GUARDO EL EVENTO')
                if dato['event_type'] == 'Beisbol':
                    object.insertTickets(dato['zAlta'],"Zona alta",Event.objects.all().last(),dato['pAlta'])
                    object.insertTickets(dato['zMedia'],"Zona media",Event.objects.all().last(),dato['pMedia'])
                    object.insertTickets(dato['zBaja'],"Zona baja",Event.objects.all().last(),dato['pBaja'])

                else:
                    object.insertTickets(dato['tNorte'],"Tribuna norte",Event.objects.all().last(),dato['pNorte'])
                    object.insertTickets(dato['tSur'],"Tribuna sur",Event.objects.all().last(),dato['pSur'])
                    object.insertTickets(dato['tOriente'],"Tribuna oriente",Event.objects.all().last(),dato['pOriente'])
                    object.insertTickets(dato['tOccidente'],"Tribuna occidente",Event.objects.all().last(),dato['pOccidente'])
                
            return redirect('evento_listar')
    else:
        formulario = UploadForm()
    return render(request, "events/jsonEvents.html",{'form': formulario})


def updateEvent(request,id):
    event = Event.objects.get(id=id)
    if request.method =='GET':
        form= EventForm(instance=event)
    else:
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
        return redirect('evento_listar')
    return render(request,'events/insertEvents.html',{'form':form})

def viewEvent(request,id):
    event = Event.objects.get(id=id)
    if request.method =='GET':
        form= ViewEvent(instance=event)
    else:
        form = ViewEvent(request.POST, instance=event)
        if form.is_valid():
            form.save()
        return redirect('evento_listar')
    context = {'event':event,'form':form}
    return render(request,'events/viewEvents.html',context)

def deleteEvent(request,id):
    event = Event.objects.get(id=id)
    print (event.id)
    if event.state == 'Cancelado':
        state = 'activar'
        context = {'state':state,'event':event}
    else:
        state = 'cancelar'
        context = {'state':state,'event':event}

    if request.method=='POST':
        if event.state == 'Activo':
            object = Event()
            object.cancelEvent(id)

        if event.state == 'Cancelado':
            object = Event()
            object.activateEvent(id)
        return redirect('events/listEvents.html')
    return render(request,'events/deleteEvents.html',context)

def uploadImage(request,id):
    if request.method == 'POST':
            formulario = ImageForm(request.POST, request.FILES)
            if formulario.is_valid():
                newdoc = Image(filename = request.POST['filename'],docfile = request.FILES['docfile'])
                newdoc.save(formulario)
                ruta=request.FILES.get('docfile').name
                print (ruta)
                object = Event()
                event = Event.objects.get(id=id)
                event.image="./images/"+ruta
                event.save()
            return redirect('tickets/generateTicket.html')
    else:
            formulario = UploadForm()
    return render(request, "events/imageEvents.html",{'form': formulario})

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


