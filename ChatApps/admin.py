from django.contrib import admin
from .models import ChatRoom, TextMessages
# Register your models here.

admin.site.register(ChatRoom)
admin.site.register(TextMessages)