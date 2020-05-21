from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(max_length=55)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message({self.pk}) from {self.author.username}'



class Chat(models.Model):
    members = models.ManyToManyField(User, related_name='chats')
    # created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat({self.pk})'

    def get_last_10_msg(self):
        return self.messages.all().order_by('-created')[:10]

