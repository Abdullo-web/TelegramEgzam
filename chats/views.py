from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Chat
from .serializers import ChatSerializer


class ChatListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Chat.objects.filter(
            models.Q(user_1=user) | models.Q(user_2=user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()


class ChatDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Chat.objects.filter(
            models.Q(user_1=user) | models.Q(user_2=user)
        )