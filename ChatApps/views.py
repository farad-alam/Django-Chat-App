from django.shortcuts import render
from CustomUser.models import CustomUser
from . models import ChatRoom, TextMessages
from django.db.models import Q

# Create your views here.


def retrive_chat_room(first_user,second_user):
    # Check if a ChatRoom already exists where these two users are present
    existing_chat_room = ChatRoom.objects.filter(
        Q(first_user=first_user, second_user=second_user) |
        Q(first_user=second_user, second_user=first_user)
    )
    return existing_chat_room.first()

def retrive_text_messages(chat_room):
    last_message = TextMessages.objects.filter(users_room=chat_room).order_by('-send_time_str').first()

    return last_message




def home(request):
    user_list = CustomUser.objects.all().exclude(id=request.user.id)

    context={
        "user_list":user_list,
    }

    return render(request,'chattemp/landing_page.html',context)

def index(request):
    # "chatapps/index.html"
    return render(request, )


def room(request, room_name):
    # "chatapps/room.html",
    return render(request,  {"room_name": room_name})


def single_chat(request, user_id):
    chat_with_user = CustomUser.objects.get(id=user_id)
    user_list = CustomUser.objects.all().exclude(id=request.user.id)

    # last_messages_list = []

    # for firends in user_list:
    #     chat_room = retrive_chat_room(firends, request.user)
    #     last_message = retrive_text_messages(chat_room)
    #     last_messages_list.append(last_message)
    
    # print(last_messages_list)

    context= {
        "user_id": user_id,
        "chat_with_user":chat_with_user,
        "user_list":user_list,
        # "last_messages_list":last_messages_list
        }
    return render(request, "chattemp/chat_with_friend.html", context)