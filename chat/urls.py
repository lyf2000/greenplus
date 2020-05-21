from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import chat, page, user

app_name = 'chat'

urlpatterns = [
    path('', chat, name='chat'),
    path('user/', user, name='user'),
    path('page/', page, name='page'),
    path('api/', include('chat.api.urls'))

]
