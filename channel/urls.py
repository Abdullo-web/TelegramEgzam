from django.urls import path
from .views import *

urlpatterns = [
    path('', ChannelListCreateView.as_view()),
    path('<int:pk>/', ChannelDetailView.as_view()),
    path('following/',FollowingListView.as_view()),
    path('channels/<int:channel_id>/follow/',ChannelFollowView.as_view()),
    path('channels/<int:channel_id>/is-following/',IsFollowingView.as_view()),
    path('channels/<int:channel_id>/posts/',ChannelPostListCreateView.as_view()),
    path('posts/<int:pk>/',PostDetailView.as_view()), 
]