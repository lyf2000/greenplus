from rest_framework import routers

from chat.api.views import MessageViewSet, ChatViewSet

app_name = 'api-chat'


router = routers.DefaultRouter()
router.register('messages', MessageViewSet, basename='messages-api')
router.register('chats', ChatViewSet, basename='chat-api')

urlpatterns = [
    # path('users/<int:pk>', UserRetrieveView.as_view(), name='user'),
] + router.urls
