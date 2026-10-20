from django.urls import path
from .views import *

urlpatterns = [
    path('', GroupListCreateView.as_view()),
    path('<int:pk>/', GroupDetailView.as_view()),
    path('<int:group_id>/messages/',GroupMessageListCreateView.as_view()),
]