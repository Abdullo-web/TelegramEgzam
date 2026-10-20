from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import AccountRegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PhoneTokenSerializer,AccountMeSerializer
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChangePasswordSerializer
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi






class AccountRegisterView(CreateAPIView):
    serializer_class = AccountRegisterSerializer
    permission_classes = [AllowAny]


class PhoneTokenView(TokenObtainPairView):
    serializer_class = PhoneTokenSerializer
    
    
class AccountMeView(RetrieveAPIView):
    serializer_class = AccountMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['old_password', 'new_password'],
            properties={
                'old_password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Текущий пароль'
                ),
                'new_password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Новый пароль'
                ),
            },
        ),
        responses={200: 'Пароль успешно изменён.'}
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'detail': 'Пароль успешно изменён.'},
            status=status.HTTP_200_OK
        )