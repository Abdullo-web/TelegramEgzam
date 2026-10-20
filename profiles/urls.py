from django.urls import path
from .views import *

urlpatterns = [
    path('', ProfileSearchView.as_view()),
    path('me/', ProfileUpdateMeView.as_view()),
    path('<int:pk>/', ProfileDetailView.as_view()),
    path('avatars/', AvatarCreateView.as_view()),
    path('avatars/<int:pk>/', AvatarDetailView.as_view()),
]