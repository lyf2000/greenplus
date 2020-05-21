from django_filters import rest_framework as filters
from rest_framework import viewsets

from chat.api.filters import MessageFilter
from chat.api.serializers import MessageSerializer, ChatSerializer
from chat.models import Message, Chat


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ('author', 'title')
    filterset_class = MessageFilter


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    # filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ('author', 'title')
    # filterset_class = MessageFilter
