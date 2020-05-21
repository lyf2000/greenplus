# chat/routing.py
from django.urls import re_path

from .consumers import NotifyConsumer

websocket_urlpatterns = [
    # re_path(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
    # re_path(r'^ws/chat/$', ChatConsumer),
    re_path(r'^ws/notify/$', NotifyConsumer),
]
