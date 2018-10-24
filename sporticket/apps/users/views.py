from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.users.forms import UserForm
from apps.users.models import *
from django.views.generic import ListView,CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import psycopg2
# Create your views here.

def connect(): #CONEXION ALTERNATIVA PARA DAR INSTRUCCIONES A LA BD SIN NECESIDAD DE UN FORM
    conn = psycopg2.connect(" \
        dbname=postgres \
        user=postgres \
        password=24603759")
    return conn

def index(request):
	return render(request, 'base/base.html')

def insertUser(request):
	if request.method == 'POST':	
		form = UserForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('users/listUsers.html')
	else:
		form = UserForm()

	return render(request, 'users/insertUsers.html', {'form': form})


def listUsers(request):
	user = Users.objects.all()
	contexto = {'users': user}
	return render(request, 'users/listUsers.html', contexto)

def editUsers(request, identification):
	user = Users.objects.get(identification=identification)
	if request.method == 'GET':	
		form = UserForm(instance=user)
	else:
		form = UserForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
		return redirect('users/listUsers.html')
	return render(request, 'users/insertUsers.html',{'form': form})


def deleteUsers(request, identification):
	user = Users.objects.get(identification=identification)
	if request.method == 'POST':
		changeStateUser(identification)
		return redirect('users/listUsers.html')
	return render(request, 'users/deleteUsers.html',{'users': user})

def viewUsers(request, identification):
    user = Users.objects.get(identification=identification)
    if request.method =='GET':
        form= UserForm(instance=user)
    else:
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return redirect('users/listUsers.html')
    return render(request,'users/viewUsers.html',{'form':form})

def first(request):
	return HttpResponse("Bienvenido a sporTicket")

class UsersList(ListView):
    model = Users
    template_name ='users/listUsers.html'

def changeStateUser(identification):
    conn = connect()
    cursor = conn.cursor()
    instruction = "UPDATE users_users SET state=\'INACTIVO\' WHERE identification='"+identification+"';"
    cursor.execute(instruction)
    conn.commit()
    conn.close()