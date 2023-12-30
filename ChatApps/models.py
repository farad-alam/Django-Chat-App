from django.db import models
from django.utils import timezone

# Create your models here.

class ChatRoom(models.Model):
    first_user = models.ForeignKey("CustomUser.CustomUser", on_delete=models.DO_NOTHING, related_name="first_user")
    second_user = models.ForeignKey("CustomUser.CustomUser", on_delete=models.DO_NOTHING, related_name="second_user")
    room_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.room_name = f"single_chat{self.first_user.id}-{self.second_user.id}"
        super(ChatRoom, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_user}-{self.second_user}"


class TextMessages(models.Model):
    users_room = models.ForeignKey("ChatApps.ChatRoom", related_name='users_chat_room', on_delete=models.DO_NOTHING)
    send_by = models.ForeignKey("CustomUser.CustomUser", on_delete=models.DO_NOTHING, related_name="user_who_message_send_to_room")
    message_text = models.CharField(max_length=500)
    send_time_str = models.CharField(max_length=30, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.send_time_str is None:
            # Set send_time_str when it's not provided
            self.send_time_str = timezone.now().isoformat()

        super(TextMessages, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.users_room.room_name}--{self.send_by}--{self.message_text[:20]}"
    






