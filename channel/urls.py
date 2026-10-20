from django.urls import path
from .views import *

urlpatterns = [
    path('', ChannelListCreateView.as_view()),
     path('<int:pk>/', ChannelDetailView.as_view()),
]