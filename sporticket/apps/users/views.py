from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView , UpdateView
from apps.users.models import Profile, Seller, Manager, Buyer
from django.contrib.auth.models import User
from apps.users.models import Profile
from apps.users.forms import ProfileForm, UserForm, UserUpdateForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms  import UserCreationForm
import psycopg2
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,permission_required
from django.db import connection 
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.models import Group 

# Create your views here.

def index(request):
	return HttpResponse("soy la pagina principal de la app")

class ProfileCreate(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
		
		permission_required = 'users.Gerente'	
		login_url = '/login/'
		redirect_field_name = '/login/'
		raise_exception = False
		model = Profile
		template_name = 'users/insertUsers.html'
		form_class = ProfileForm
		second_form_class = UserForm
		success_url = reverse_lazy('listUser')

		def get_context_data(self, **kwargs):
			context = super(ProfileCreate, self).get_context_data(**kwargs)
			if 'form'  not in context:
				context['form'] = self.form_class(self.request.GET)
			if 'form2' not in context:
				context['form2'] = self.second_form_class(self.request.GET)
			return context

		def post(self, request, *args , **kwargs):
			self.object = self.get_object
			form = self.form_class(request.POST)
			form2 =  self.second_form_class(request.POST)
			if form.is_valid() and form2.is_valid():
				profile = form.save(commit=False)
				profile.user = form2.save()
				typeUser = form.cleaned_data['userType']
				print(typeUser)
				profile.save()
				if str(typeUser) == "Vendedor":
					Seller.objects.create(profile=Profile.objects.all().last())
					my_group = Group.objects.get(name='Vendedores') 
					my_group.user_set.add(User.objects.all().last())
					return HttpResponseRedirect(self.get_success_url())
					messages.success(request,'Usuario Vendedor creado exitosamente!')
				if str(typeUser) == "Gerente":
					Manager.objects.create(profile=Profile.objects.all().last())
					my_group = Group.objects.get(name='Vendedores') 
					my_group.user_set.add(User.objects.all().last())
					my_group = Group.objects.get(name='Gerentes') 
					my_group.user_set.add(User.objects.all().last())
					messages.success(request,'Usuario Gerente creado exitosamente!')
					return HttpResponseRedirect(self.get_success_url())
				if str(typeUser) == "Externo":
					Manager.objects.create(profile=Profile.objects.all().last())
					my_group = Group.objects.get(name='Externo') 
					my_group.user_set.add(User.objects.all().last())
					messages.success(request,'Usuario comprador creado exitosamente!')
					return HttpResponseRedirect(self.get_success_url())
			else:
				return self.render_to_response(self.get_context_data(form=form, form2=form2))

class ProfileList(LoginRequiredMixin,PermissionRequiredMixin, ListView):
		
		permission_required = 'users.Gerente'	
		login_url = '/login/'
		redirect_field_name = '/login/'
		raise_exception = False
		model2 = User
		model = Profile
		template_name = 'users/listUsers.html'

class ProfileUpdate(LoginRequiredMixin, UpdateView):

		model = Profile
		second_model = User
		template_name = 'users/editMyProfile.html'
		form_class = ProfileForm
		second_form_class = UserForm
		success_url = reverse_lazy('listUser')

		def get_context_data(self, **kwargs):
			context = super(ProfileUpdate, self).get_context_data(**kwargs)
			pk = self.kwargs.get('pk',0)
			user = self.second_model.objects.get(id=request.user.id)
			if 'form2' not in context:
				context['form2'] = self.second_form_class(instance=user)
			context['id'] = pk
			return context

		def post(self, request, *args, **kwargs):
			self.object = self.get_object
			id_profile = kwargs['pk']
			profile = self.model.objects.get(id=id_profile)
			user = self.second_model.objects.get(id=profile.user_id)
			form = self.form_class(request.POST, instance=profile)
			form2 = self.second_form_class(request.POST, instance=user)
			if form.is_valid() and form2.is_valid():
				form.save()
				form2.save()
				return HttpResponseRedirect(self.get_success_url())
			else:
				return HttpResponseRedirect(self.get_success_url())


class ViewUpdate(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):

		permission_required = 'users.Gerente'	
		login_url = '/login/'
		redirect_field_name = '/login/'
		raise_exception = False

		model = Profile
		second_model = User
		template_name = 'users/viewUsers.html'
		form_class = ProfileForm
		second_form_class = UserForm
		success_url = reverse_lazy('listUser')

		def get_context_data(self, **kwargs):
			context = super(ViewUpdate, self).get_context_data(**kwargs)
			pk = self.kwargs.get('pk',0)
			profile = self.model.objects.get(id=pk)
			user = self.second_model.objects.get(id=profile.user_id)
			if 'form' not in context:
				context['form'] = self.form_class()
			if 'form2' not in context:
				context['form2'] = self.second_form_class(instance=user)
			context['id'] = pk
			return context

		def post(self, request, *args, **kwargs):
			self.object = self.get_object
			id_profile = kwargs['pk']
			profile = self.model.objects.get(id=id_profile)
			user = self.second_model.objects.get(id=profile.user_id)
			form = self.form_class(request.POST, instance=profile)
			form2 = self.second_form_class(request.POST, instance=user)
			if form.is_valid() and form2.is_valid():
				form.save()
				form2.save()
				return HttpResponseRedirect(self.get_success_url())
			else:
				return HttpResponseRedirect(self.get_success_url())		


@permission_required('users.Gerente' ,reverse_lazy('listUser'))
def deleteUsers(request ,id):

		user = User.objects.get(id=id)
		if request.method=='POST':
			changeState(id)
			messages.success(request,'Usuario deshabilitado exitosamente!')
			return HttpResponseRedirect(reverse('listUser'))
		return render(request,'users/deleteUsers.html',{'users':user})

def changeState(id):
	user = User.objects.get(id=id)
	user.is_active = False
	user.save()

def userLogin(request):
	
		context = {}
		if request.method == "POST":
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request, username=username, password=password)
			if user:
				login(request, user)
				if request.GET.get('next', None):
					messages.success(request,'Bienvenido a SporTicket!')	
					return HttpResponseRedirect(request.GET['next'])
					messages.success(request,'Bienvenido a SporTicket!')							
				return HttpResponseRedirect(reverse('indexUser'))
			else:
				context["error"] = "Provide valid credentials !!"
				return render(request, "auth/login.html", context)
		else:
			return render(request, "auth/login.html", context)


def success(request):
    context = {}
    context['user'] = request.user
    return render(request, "auth/success.html", context)

def userLogout(request):
		logout(request)
		return HttpResponseRedirect(reverse('userLogin'))

@permission_required('users.Gerente' ,reverse_lazy('listUser'))
def updateUser(request,id):
	
		user = User.objects.get(id=id)
		profile = Profile.objects.get(user_id=id)
		form = UserUpdateForm()
		if request.method == 'POST':

			form = UserUpdateForm(request.POST)

			first_name = form['first_name'].value()
			last_name = form['last_name'].value()
			username = form['username'].value()
			userType = form['userType'].value()
			email = form['email'].value()
			phone = form['phone'].value()
			numAccount = form['numAccount'].value()	

			user.first_name = first_name
			user.last_name = last_name
			user.username = username
			user.email = email
			profile.userType = userType
			profile.phone = phone
			profile.numAccount = numAccount

			profile.save()
			user.save()
			messages.success(request,'Usuario actualizado exitosamente!')
			return render(request, 'users/listUsers.html')
		else:
			return render(request, 'users/editUsers.html',{'form': form})


def updateProfile(request,id):
	
		user = User.objects.get(id=id)
		form = UserUpdateForm()
		if request.method == 'POST':

			form = UserUpdateForm(request.POST)

			first_name = form['first_name'].value()
			last_name = form['last_name'].value()
			username = form['username'].value()
			email = form['email'].value()

			user.first_name = first_name
			user.last_name = last_name
			user.username = username
			user.email = email

			user.save()
			messages.success(request,'Usuario actualizado exitosamente!')
			return render(request, 'users/listUsers.html')
		else:
			return render(request, 'users/editMyProfile.html',{'form': form})

def createProfileSocial(request):

		person = Profile.objects.all().filter(user_id=request.user.id).exists()
		print(person)
		form = UserUpdateForm()
		if person == False:
			if request.method == 'POST':
				form = UserUpdateForm(request.POST)
				identification =  form['identification'].value()
				phone = form['phone'].value()
				userType = 'Externo'
				numAccount = form['numAccount'].value()	
				lastProfile = Profile.objects.all().filter().last()
				if lastProfile == None:
					object = Profile()
					newProfile = Profile(1, request.user.id,identification,userType,phone,numAccount)
					newProfile.save()
					messages.success(request,'Su perfil ha sido creado exitosamente!')
					return render(request, 'users/listUsers.html')
				else:			
					object = Profile()
					idUser = lastProfile.id + 1
					print (idUser)
					newProfile = Profile(idUser, request.user.id,identification,userType,phone,numAccount)
					newProfile.save()
					messages.success(request,'Su perfil ha sido creado exitosamente!')
					return render(request, 'users/listUsers.html')
			else:
				return render(request, 'users/createMyProfile.html',{'form': form})
		else:
				return render(request, 'sales/viewsEvent.html')
class CreateUser(CreateView):
		model = Profile
		template_name = 'users/createUser.html'
		form_class = ProfileForm
		second_form_class = UserForm
		success_url = reverse_lazy('userLogin')

