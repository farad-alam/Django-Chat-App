from django.shortcuts import render
from CustomUser.models import CustomUser

# Create your views here.

def home(request):
    user_list = CustomUser.objects.all()
    context={
        "user_list":user_list
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
    user_list = CustomUser.objects.all()
    context= {"user_id": user_id,"chat_with_user":chat_with_user,"user_list":user_list}
    return render(request, "chattemp/chat_with_friend.html", context)