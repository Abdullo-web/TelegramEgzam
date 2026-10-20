
from django.db import models
from django.conf import settings


class Channel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    type = models.CharField(max_length=10,
        choices=[
            ('public', 'Public'),
            ('private', 'Private'),
        ]
    )
    cr_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200,unique=True,blank=True,null=True)

    def save(self, *args, **kwargs):
        if self.type == 'public' and not self.link:
            super().save(*args, **kwargs)
            self.link = f'channel-{self.id}'
            super().save(update_fields=['link'])
            return

        if self.type == 'private':
            self.link = None

        super().save(*args, **kwargs)

    

class ChannelMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='channel_memberships')
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE,related_name='members')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'channel'],
                name='unique_channel_member'
            )
        ]



class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE,related_name='posts')
    content = models.TextField()
    cr_at = models.DateTimeField(auto_now_add=True)

