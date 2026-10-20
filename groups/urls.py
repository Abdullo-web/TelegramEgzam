from django.urls import path
from .views import *
urlpatterns = [
    path('', GroupListCreateView.as_view()),
    path('<int:pk>/', GroupDetailView.as_view()),
    path('<int:group_id>/members/',GroupMemberListCreateView.as_view()),
    path('<int:group_id>/members/me/',LeaveGroupView.as_view()),
    path('<int:group_id>/members/<int:pk>/',GroupMemberDetailView.as_view()),
    path('<int:group_id>/messages/',GroupMessageListCreateView.as_view()),
    path('messages/<int:pk>/',GroupMessageDeleteView.as_view()),
]