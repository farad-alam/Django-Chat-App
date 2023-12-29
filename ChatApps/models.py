from django.db import models

# Create your models here.

class ChatRoom(models.Model):
    first_user = models.ForeignKey("CustomUser.CustomUser", on_delete=models.DO_NOTHING, related_name="first_user")
    second_user = models.ForeignKey("CustomUser.CustomUser", on_delete=models.DO_NOTHING, related_name="second_user")
    room_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.room_name = f"single_chat{self.first_user.id}-{self.second_user.id}"
        super(ChatRoom, self).save(*args, **kwargs)




class TextMessage(models.Model):
    sent_by = models.ForeignKey("CustomUser.CustomUser", on_delete=models.DO_NOTHING, related_name="message_get_from")
    sent_to = models.ForeignKey("CustomUser.CustomUser", on_delete=models.DO_NOTHING, related_name="message_sent_to")
    message_text = models.CharField(max_length=500)
    time_stamp = models.DateTimeField(auto_now_add=True)