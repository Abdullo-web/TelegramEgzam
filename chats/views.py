from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import Chat,Message
from .serializers import ChatSerializer,MessageSerializer
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


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
        
        
        
    
class ChatMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_chat(self):
        chat = get_object_or_404(
            Chat,
            pk=self.kwargs['chat_id']
        )

        if self.request.user.pk not in [
            chat.user_1_id,
            chat.user_2_id
        ]:
            raise PermissionDenied(
                'Ты не являешься участником этого чата.'
            )

        return chat

    def get_queryset(self):
        chat = self.get_chat()
        return Message.objects.filter(chat=chat).select_related(
            'sender', 'chat'
        ).order_by('created_at', 'id')

    def perform_create(self, serializer):
        chat = self.get_chat()
        serializer.save(
            chat=chat,
            sender=self.request.user
        )


class MessageDeleteView(generics.DestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)