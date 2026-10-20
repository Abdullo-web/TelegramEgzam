from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Channel,ChannelMember
from .serializers import ChannelSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class ChannelListCreateView(generics.ListCreateAPIView):
    serializer_class = ChannelSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
    
    
    def get_queryset(self):
        return Channel.objects.filter(
            type='public'
        ).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        
class ChannelDetailView(generics.RetrieveAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Channel.objects.all()

    def get_object(self):
        channel = super().get_object()

        if channel.type == 'private':
            user = self.request.user

            if not user.is_authenticated:
                from rest_framework.exceptions import NotFound
                raise NotFound('Канал не найден.')

            is_owner = channel.owner_id == user.id

            is_member = ChannelMember.objects.filter(
                channel=channel,
                user=user
            ).exists()

            if not is_owner and not is_member:
                from rest_framework.exceptions import NotFound
                raise NotFound('Канал не найден.')

        return channel
