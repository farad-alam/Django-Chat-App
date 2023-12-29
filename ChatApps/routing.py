# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/single-chat/(?P<user_id>\w+)/$", consumers.SingleChatConsumer.as_asgi()),
    # path("ws/single-chat/<int:id>", consumers.SingleChatConsumer.as_asgi(), name='single_chat_page')

]