from rest_framework import serializers
from account.models import Account
from .models import Profile, Avatar


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username',
        required=False
    )

    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'bio']
        read_only_fields = ['id', 'user']

    def validate_username(self, value):
        user = self.instance.user

        if Account.objects.filter(username=value).exclude(
            id=user.id
        ).exists():
            raise serializers.ValidationError(
                'Этот username уже занят.'
            )

        return value

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        if 'username' in user_data:
            instance.user.username = user_data['username']
            instance.user.save()

        if 'bio' in validated_data:
            instance.bio = validated_data['bio']

        instance.save()
        return instance


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id', 'profile', 'image', 'created_at']
        read_only_fields = ['id', 'profile', 'created_at']