from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Channel
from .serializers import ChannelSerializer


class ChannelListCreateView(generics.ListCreateAPIView):
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Channel.objects.filter(
            type='public'
        ).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)