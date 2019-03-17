from django.urls import path
from django.conf.urls import url,include
from django.contrib.auth.decorators import login_required

from apps.users.views import *

urlpatterns = [

    url(r'^$', index, name='indexUser'),
    url(r'users/insertUsers.html', ProfileCreate.as_view() , name='crateUser'),
    url(r'users/listUsers.html',ProfileList.as_view() , name='listUser'),
    url(r'users/editUser/(?P<pk>\d+)/$', ProfileUpdate.as_view() , name='editUser'),
    url(r'users/viewUser/(?P<pk>\d+)/$', ViewUpdate.as_view() , name='viewUser'),
	url(r'users/deleteUsers/(?P<id>\d+)/$', login_required(deleteUsers) , name='deleteUser'),
    url(r'users/createUser.html', CreateUser.as_view() , name='createUser'),

]