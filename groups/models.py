from django.db import models
from django.conf import settings


class Group(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='owned_groups')
    title = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='groups/',blank=True,null=True)




class GroupMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='group_memberships')
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='members')
    role = models.CharField(max_length=10,
        choices=[
            ('owner', 'Owner'),
            ('admin', 'Admin'),
            ('member', 'Member'),
        ],default='member'
    )
    joining_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'group'],
                name='unique_group_member'
            )
        ]



class GroupMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='group_messages')
    group = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='messages')
    content = models.TextField()
    cr_at = models.DateTimeField(auto_now_add=True)

