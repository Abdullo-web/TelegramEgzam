from rest_framework import serializers
from .models import Account
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password




class AccountRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = Account
        fields = ['id', 'phone_number', 'password']
        read_only_fields = ['id']

    def validate_phone_number(self, value):
        if not value.startswith('+992') or len(value) != 13:
            raise serializers.ValidationError('vvedite pravilny nomer telefona')

        if Account.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('Etot nomer uje zaregistrirovan')

        return value

    def create(self, validated_data):
        return Account.objects.create_user(
            username=validated_data['phone_number'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        
        
        

class PhoneTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['phone_number'],
            password=attrs['password']
        )

        if user is None:
            raise serializers.ValidationError(
                'Неправильный номер телефона или пароль.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Аккаунт отключён.'
            )

        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        
        
class AccountMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','username','phone_number','first_name','last_name','email',]
        



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                'Старый пароль указан неправильно.'
            )

        return value

    def validate_new_password(self, value):
        user = self.context['request'].user
        validate_password(value, user=user)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
        return user