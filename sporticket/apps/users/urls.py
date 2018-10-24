from django.urls import path
from django.conf.urls import url,include

from apps.users.views import *

urlpatterns = [

    url(r'^$', index),
    url(r'users/insertUsers.html', insertUser , name='crateUser'),
    url(r'users/listUsers.html', UsersList.as_view(), name='listUsers' ),
    url(r'users/editUsers/(?P<identification>\w+)/$', editUsers , name='editUser'),
    url(r'users/deleteUsers/(?P<identification>\w+)/$', deleteUsers , name='deleteUser'),
    url(r'users/viewUsers/(?P<identification>\w+)/$', viewUsers, name='viewUser' ),

]