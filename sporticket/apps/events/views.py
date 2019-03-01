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
from apps.events.forms import UploadImageForm

# Create your views here.

def index(request):
    return render(request, 'base/base.html')

def insertEvent(request):
    try:
        form = EventForm()
        imageForm = ImageForm()
        context = {'form':form,'imageForm':imageForm}
        if request.method == 'POST':
            form = EventForm(request.POST)
            imageForm = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                print ('SE CREO UN EVENTO')
                object = Event()
                object.lastEventId()
                if imageForm.is_valid():
                    newdoc = Image(filename = request.POST['filename'],docfile = request.FILES['docfile'])
                    print ('creo el newdoc')
                    newdoc.save(imageForm)
                    print ('guardo el newdoc')
                    ruta=request.FILES.get('docfile',false).name
                    print (ruta)
                    object = Event()
                    event = Event.objects.get(id=id)
                    event.image="./images/"+ruta
                    event.save()
                else:
                    print('Error al subir imagen')
            return redirect('tickets/generateTicket.html')
        else:
            return render(request, 'events/insertEvents.html',context)
    except MultiValueDictKeyError:
        newdoc = False
    return render(request, 'events/insertEvents.html',context)

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
                    insertTickets(dato['zAlta'],"Zona alta",Event.objects.all().last(),dato['pAlta'])
                    insertTickets(dato['zMedia'],"Zona media",Event.objects.all().last(),dato['pMedia'])
                    insertTickets(dato['zBaja'],"Zona baja",Event.objects.all().last(),dato['pBaja'])

                else:
                    insertTickets(dato['tNorte'],"Tribuna norte",Event.objects.all().last(),dato['pNorte'])
                    insertTickets(dato['tSur'],"Tribuna sur",Event.objects.all().last(),dato['pSur'])
                    insertTickets(dato['tOriente'],"Tribuna oriente",Event.objects.all().last(),dato['pOriente'])
                    insertTickets(dato['tOccidente'],"Tribuna occidente",Event.objects.all().last(),dato['pOccidente'])
                
            return redirect('events/listEvents.html')
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
        return redirect('events/listEvents.html')
    return render(request,'events/insertEvents.html',{'form':form})

def viewEvent(request,id):
    event = Event.objects.get(id=id)
    if request.method =='GET':
        form= ViewEvent(instance=event)
    else:
        form = ViewEvent(request.POST, instance=event)
        if form.is_valid():
            form.save()
        return redirect('events/listEvents.html')
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
            return redirect('events/listEvents.html')
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

def insertTickets(quantity,ubication,event,cost):
        x=0
        while x < int(quantity):        
            save_ticket(ubication,event,cost) 
            x+=1    

def save_ticket(ubication,event,cost):
        newTicket = Ticket(cost=cost,ubication=ubication,event=event,state='Disponible')
        newTicket.save()

