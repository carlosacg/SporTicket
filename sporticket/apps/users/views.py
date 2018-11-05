from django.shortcuts import render, redirect
from django.http import HttpResponse
from apps.users.forms import UserForm
from apps.users.models import Users

# Create your views here.

def index(request):
	return render(request, 'users/index.html')

def insertUser(request):
	if request.method == 'POST':	
		form = UserForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('users:index')
	else:
		form = UserForm()

	return render(request, 'users/insertUsers.html', {'form': form})


def users_list(request):
	user = Users.objects.all()
	contexto = {'users': user}
	return render(request, 'users/user_list.html', contexto)

def user_edit(request, identificacion):
	user = Users.objects.get(identificacion=identificacion)
	if request.method == 'GET':	
		form = UserForm(instance=user)
	else:
		form = UserForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
		return redirect('users:user_list')
	return render(request, 'users/user_form.html',{'form': form})


def user_delete(request, identificacion):
	user = Users.objects.get(identificacion=identificacion)
	if request.method == 'POST':
		user.delete()
		return redirect('users:user_list')
	return render(request, 'users/user_delete.html',{'users': user})

def first(request):
	return HttpResponse("Bienvenido a sporTicket")