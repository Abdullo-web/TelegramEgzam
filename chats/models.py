from django.db import models
from django.conf import settings


class Chat(models.Model):
    user_1 = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='chats_as_user_1')

    user_2 = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='chats_as_user_2')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_1', 'user_2'],
                name='unique_private_chat_pair'
            )
        ]
