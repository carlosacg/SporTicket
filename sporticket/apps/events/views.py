from django.shortcuts import render,redirect
from django.http import HttpResponse
from apps.events.forms import EventForm
from apps.events.forms import ViewEvent
from apps.event_type.forms import EventTypeForm
from apps.events.forms import UploadForm
from apps.events.forms import ImageForm
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from apps.events.models import *
from django.urls import reverse_lazy,reverse
import json
from apps.tickets.models import Ticket
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponseRedirect
from apps.events.serializers import EventSerializers
from rest_framework import generics
from django.views.generic.list import ListView
import requests
import json
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.

def index(request):
    return render(request, 'base/base.html')

@permission_required('users.Gerente' ,reverse_lazy('indexEvents'))
def insertEventType(request):
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('insertEvents.html')
    else:
        form = EventTypeForm()
    return render(request, 'events/insertEvenType.html',{'form':form}) 

@permission_required('users.Gerente' ,reverse_lazy('indexEvents'))
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

@permission_required('users.Gerente' ,reverse_lazy('indexEvents'))
def listEvent(request):
    event = Event.objects.all()
    context = {'events':event}
    return render(request,'events/listEvents.html',context)

@permission_required('users.Gerente' ,reverse_lazy('index'))
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
                    print('Entro a beisbol')
                    insertTickets(dato['zAlta'],"Zona alta",Event.objects.all().last(),dato['pAlta'])
                    insertTickets(dato['zMedia'],"Zona media",Event.objects.all().last(),dato['pMedia'])
                    insertTickets(dato['zBaja'],"Zona baja",Event.objects.all().last(),dato['pBaja'])

                else:
                    print('Entro a futTenis')
                    print(dato['tNorte'],"Tribuna norte",Event.objects.all().last(),dato['pNorte'])
                    insertTickets(dato['tNorte'],"Tribuna norte",Event.objects.all().last(),dato['pNorte'])
                    insertTickets(dato['tSur'],"Tribuna sur",Event.objects.all().last(),dato['pSur'])
                    insertTickets(dato['tOriente'],"Tribuna oriente",Event.objects.all().last(),dato['pOriente'])
                    insertTickets(dato['tOccidente'],"Tribuna occidente",Event.objects.all().last(),dato['pOccidente'])
                
            return redirect('events/listEvents.html')
    else:
        formulario = UploadForm()
    return render(request, "events/jsonEvents.html",{'form': formulario})

@permission_required('users.Gerente' ,reverse_lazy('indexEvents'))
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

@permission_required('users.Gerente' ,reverse_lazy('indexEvents'))
def viewEvent(request,id):
    event = Event.objects.get(id=id)
    if request.method =='GET':
        getEventsJSON('GET')
        form= ViewEvent(instance=event)
    else:
        form = ViewEvent(request.POST, instance=event)
        if form.is_valid():
            form.save()
        return redirect('evento_listar')
    context = {'event':event,'form':form}
    return render(request,'events/viewEvents.html',context)

@permission_required('users.Gerente' ,reverse_lazy('indexEvents'))
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

@permission_required('users.Gerente' ,reverse_lazy('indexEvents'))
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
            return HttpResponseRedirect(reverse('location_crear', args=[id]))
    else:
            formulario = UploadForm()
    return render(request, "events/imageEvents.html",{'form': formulario})
    
def insertTickets(quantity,ubication,event,cost):
        print(quantity,ubication,event,cost)
        x=0
        while x < int(quantity):        
            save_ticket(ubication,event,cost) 
            x+=1    
    
def save_ticket(ubication,event,cost):
    print(ubication,event,cost)
    newTicket = Ticket(cost=cost,ubication=ubication,event=event,state='Disponible')
    newTicket.save()

class EventDelete(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    		
        permission_required = 'users.Gerente'	
        login_url = '/login/'
        redirect_field_name = '/login/'
        raise_exception = False
        model = Event
        template_name = 'events/deleteEvents.html'
        success_url = reverse_lazy('evento_listar')

class EventList(LoginRequiredMixin,ListView):
		
        login_url = '/login/'
        redirect_field_name = '/login/'
        raise_exception = False
        model = Event
        template_name ='events/listEvents.html'

class EventCreate(LoginRequiredMixin,CreateView):
    	
        permission_required = 'users.Gerente'	
        login_url = '/login/'
        redirect_field_name = '/login/'
        raise_exception = False
        model = Event
        form_class = EventForm
        template_name ='events/insertEvents.html'
        success_url = reverse_lazy('evento_listar')

class EventUpdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
		
        permission_required = 'users.Gerente'	
        login_url = '/login/'
        redirect_field_name = '/login/'
        raise_exception = False
        model = Event
        form_class = EventForm
        template_name = 'events/insertEvents.html'
        success_url = reverse_lazy('evento_listar')

class EventsSerialList(LoginRequiredMixin, generics.ListCreateAPIView):

        login_url = '/login/'
        redirect_field_name = '/login/'
        raise_exception = False
        queryset = Event.objects.all()
        serializer_class = EventSerializers

class EventsSerialDetail(LoginRequiredMixin, generics.RetrieveUpdateDestroyAPIView):

        login_url = '/login/'
        redirect_field_name = '/login/'
        raise_exception = False
        queryset = Event.objects.all()
        serializer_class = EventSerializers

def getEventsJSON(request):
    response = requests.get('http://localhost:8001/events/?format=json') 
    if response.status_code == 200:
        payload = response.json()
        for i in payload:
            name = i['name']
            date = i['initial_date']
            hour = i['initial_time']
            place = i['place']
            state = i['state']
            url = i['url']
            capacity = i['capacity']
            visitor = i['visitor']
            local = i['local']
            image = i['image']
            event_type = i['event_type']
            print(event_type)
            object = Event()
            newEvent = Event(name=name,initial_date=date,initial_time=hour,place=place,url=url,state=state,capacity=capacity,visitor=visitor,local=local,event_type_id=event_type)
            newEvent.save()
            print("Interopere")
        
