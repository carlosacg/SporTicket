from django.urls import path
from django.conf.urls import url,include
from django.contrib.auth.decorators import login_required

from apps.users.views import *

urlpatterns = [

    url(r'^$', login_required(index), name='indexUser'),
    url(r'^$', login_required(createProfileSocial), name='indexProfile'),
    url(r'users/insertUsers.html', ProfileCreate.as_view() , name='crateUser'),
    url(r'users/listUsers.html',ProfileList.as_view() , name='listUser'),
    url(r'users/editProfile/(?P<id>\d+)/$', login_required(updateProfile) , name='editUser'),
    url(r'users/createProfile.html', login_required(createProfileSocial) , name='editUser'),
    url(r'users/viewUser/(?P<pk>\d+)/$', ViewUpdate.as_view() , name='viewUser'),
	url(r'users/deleteUsers/(?P<id>\d+)/$', login_required(deleteUsers) , name='deleteUser'),
    url(r'users/editUsersAdmin/(?P<id>\d+)/$', login_required(updateUser) , name='editUsers'),
    url(r'users/createUser.html', CreateUser.as_view() , name='createUser'),
	 

]
