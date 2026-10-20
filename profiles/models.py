from django.db import models
from account.models import Account


class Profile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(blank=True,null=True)




class Avatar(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='avatars')
    image = models.ImageField(upload_to='avatars/')
    created_at = models.DateTimeField(auto_now_add=True)

    