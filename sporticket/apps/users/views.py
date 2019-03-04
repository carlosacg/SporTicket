from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView , UpdateView
from apps.users.models import Profile
from django.contrib.auth.models import User
from apps.users.forms import ProfileForm, UserForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms  import UserCreationForm
import psycopg2
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection 
from django.contrib import messages

# Create your views here.

def index(request):
	return HttpResponse("soy la pagina principal de la app")

class ProfileCreate(CreateView):
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
			profile.save()
			messages.success(request, "Paciente registrado exitosamente.")
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

class ProfileList(ListView):
	model = Profile
	template_name = 'users/listUsers.html'

class ProfileUpdate(UpdateView):
	model = Profile
	second_model = User
	template_name = 'users/insertUsers.html'
	form_class = ProfileForm
	second_form_class = UserForm
	success_url = reverse_lazy('listUser')

	def get_context_data(self, **kwargs):
		context = super(ProfileUpdate, self).get_context_data(**kwargs)
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


def changeState(id):
    cursor = connection.cursor()
    instruction = "UPDATE auth_user SET is_active=\'FALSE\' WHERE id="+id+";"
    cursor.execute(instruction)
    connection.commit()
    connection.close()

def deleteUsers(request,id):
    user = User.objects.get(id=id)
    print (user.id)
    if request.method=='POST':
        changeState(id)
        print ('Se inhabilito un usuario')
        return redirect('listUser')
    return render(request,'users/deleteUsers.html',{'users':user})


def userLogin(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('listUser'))
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

class CreateUser(CreateView):
		model = Profile
		template_name = 'users/createUser.html'
		form_class = ProfileForm
		second_form_class = UserForm
		success_url = reverse_lazy('userLogin')

