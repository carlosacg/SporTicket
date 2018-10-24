from django.urls import path
from django.conf.urls import url,include

from apps.login.views import login

urlpatterns = [
    url(r'login/login.html', login , name='login'),
]