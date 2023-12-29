from django.urls import path

from . import views


urlpatterns = [
    path("index/", views.index, name="index"),
    path("", views.home, name="home"),
    path("<str:room_name>/", views.room, name="room"),
    path("single-chat/<int:user_id>/", views.single_chat, name="single_chat_page")
]
