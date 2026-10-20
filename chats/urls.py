from django.urls import path
from .views import *

urlpatterns = [
    path('', ChatListCreateView.as_view(), name='chat-list-create'),
    path('<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('<int:chat_id>/messages/',ChatMessageListCreateView.as_view()),
    path('messages/<int:pk>/',MessageDeleteView.as_view()),
]