from django.shortcuts import render,redirect
from django.http import HttpResponse
from apps.aplicaciones.event_form import EventForm
from apps.aplicaciones.upload_form import UploadForm
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from apps.aplicaciones.models import *
from django.urls import reverse_lazy
from django.contrib import messages
import json
import psycopg2
# Create your views here.

def connect(): #CONEXION ALTERNATIVA PARA DAR INSTRUCCIONES A LA BD SIN NECESIDAD DE UN FORM
    conn = psycopg2.connect(" \
        dbname=sport_db \
        user=andres \
        password=12345")
    return conn

def index(request):
    return render(request, 'base/base.html')

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
                save_data(dato['name'],dato['initial_dale'],dato['initial_time'],dato['place'],dato['url'],dato['state'],dato['capacity'],dato['visitor'],dato['local'],dato['event_type'])
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

def generateTicket(request,id):
    event = Event.objects.get(id=id)
    print(event.capacity)
    numberTicket=event.capacity
    numberTicket=numberTicket/3

    if request.method =='GET':
        form= EventForm(instance=event)
    else:
        for x in xrange(numberTicket):
            createTicket()
        return redirect('events/listEvents.html')
    return render(request,'events/insertEvents.html',{'form':form})

def deleteEvent(request,id):
    event = Event.objects.get(id=id)
    print (event.id)
    if request.method=='POST':
        cancelEvent(id)
        print ('Se Cancelo el evento')
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

def save_data(name,initial_date,initial_time,place,url,state,capacity,visitor,local,event_type):
    conn = connect()
    cursor = conn.cursor()
    instruction = "INSERT INTO aplicaciones_event VALUES (nextval(\'aplicaciones_event_id_seq\'),\'"+name+"\',\'"+initial_date+"\',\'"+initial_time+"\',\'"+place+"\',\'"+url+"\',\'"+state+"\',"+str(capacity)+",\'"+visitor+"\',\'"+local+"\',\'"+event_type+"\');"
    cursor.execute(instruction)
    conn.commit()
    conn.close()

def createTicket(cost,ubication,event):
    conn = connect()
    cursor = conn.cursor()
    instruction = "INSERT INTO aplicaciones_ticket VALUES (nextval(\'aplicaciones_ticket_id_seq\'),"+cost+",\'"+ubication+"\',"+event+");"
    print (instruction)
    cursor.execute(instruction)
    conn.commit()
    conn.close()

def cancelEvent(id):
    conn = connect()
    cursor = conn.cursor()
    instruction = "UPDATE aplicaciones_event SET state=\'CANCELADO\' WHERE id="+id+";"
    cursor.execute(instruction)
    conn.commit()
    conn.close()
