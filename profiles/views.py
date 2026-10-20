from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Profile, Avatar
from .serializers import ProfileSerializer, AvatarSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator



class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]



class ProfileUpdateMeView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description='Поиск по username',
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
    ),
)
class ProfileSearchView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search = self.request.query_params.get('search', '')
        return Profile.objects.filter(
            user__username__icontains=search
        )



from rest_framework.parsers import MultiPartParser, FormParser

class AvatarCreateView(generics.CreateAPIView):
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        serializer.save(profile=profile)


class AvatarDetailView(generics.RetrieveDestroyAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.profile.user != self.request.user:
            raise PermissionDenied('Нельзя удалить чужой аватар.')

        instance.delete()
