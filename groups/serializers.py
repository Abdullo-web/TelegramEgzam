from rest_framework import serializers

from .models import Group, GroupMember, GroupMessage


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'owner', 'title', 'avatar']
        read_only_fields = ['id', 'owner']

    def create(self, validated_data):
        request = self.context['request']

        group = Group.objects.create(owner=request.user,**validated_data)

        GroupMember.objects.create(
            user=request.user,
            group=group,
            role='owner'
        )

        return group


class GroupMessageSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username',read_only=True)

    class Meta:
        model = GroupMessage
        fields = ['id', 'user', 'group', 'content', 'cr_at']
        read_only_fields = ['id', 'user', 'group', 'cr_at']