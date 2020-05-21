from django.contrib import admin

# Register your models here.
from chat.models import Message, Chat


@admin.register(Message)
class MessageAdminModel(admin.ModelAdmin):
    pass


@admin.register(Chat)
class ChatAdminModel(admin.ModelAdmin):
    pass
