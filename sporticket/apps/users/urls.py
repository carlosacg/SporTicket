from django.urls import path
from django.conf.urls import url,include

from apps.users.views import *

urlpatterns = [

    url(r'^$', index),
    url(r'users/insertUsers.html', ProfileCreate.as_view() , name='crateUser'),
    url(r'users/listUsers.html', ProfileList.as_view() , name='listUser'),
    url(r'users/editUser/(?P<pk>\d+)/$', ProfileUpdate.as_view() , name='editUser'),
	url(r'users/deleteUsers/(?P<id>\d+)/$', deleteUsers , name='deleteUser'),

]