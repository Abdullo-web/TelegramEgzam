from rest_framework import serializers
from .models import Group, GroupMember, GroupMessage


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'owner', 'title', 'avatar']
        read_only_fields = ['id', 'owner']


class GroupMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = GroupMember
        fields = ['id', 'user', 'username', 'group', 'role', 'joining_time']
        read_only_fields = ['id', 'group', 'role', 'joining_time']


class GroupMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = GroupMessage
        fields = ['id', 'user', 'username', 'group', 'content', 'cr_at']
        read_only_fields = ['id', 'user', 'group', 'cr_at']