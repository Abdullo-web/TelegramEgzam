from rest_framework import serializers
from account.models import Account
from .models import Chat,Message


class ChatSerializer(serializers.ModelSerializer):
    user_2 = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        required=True
    )

    class Meta:
        model = Chat
        fields = ['id', 'user_1', 'user_2', 'created_at']
        read_only_fields = ['id', 'user_1', 'created_at']

    def validate_user_2(self, value):
        request = self.context['request']

        if value == request.user:
            raise serializers.ValidationError(
                'Нельзя создать чат с самим собой.'
            )

        return value

    def create(self, validated_data):
        request = self.context['request']
        other_user = validated_data['user_2']
        current_user = request.user


        user_1, user_2 = sorted(
            [current_user, other_user],
            key=lambda user: user.pk
        )

        chat, created = Chat.objects.get_or_create(
            user_1=user_1,
            user_2=user_2
        )

        return chat
    
    


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'created_at']
        read_only_fields = ['id', 'chat', 'sender', 'created_at']