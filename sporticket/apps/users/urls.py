from django.urls import path
from django.conf.urls import url,include

from apps.users.views import index, insertUser, users_list, user_edit, user_delete

urlpatterns = [
    url(r'users/insertUsers.html', insertUser , name='user_crear'),
    url(r'^listar$', users_list , name='user_list'),
    url(r'^editar/(?P<identificacion>\d+)/$', user_edit , name='user_editar'),
    url(r'^eliminar/(?P<identificacion>\d+)/$', user_delete , name='user_eliminar'),


]
