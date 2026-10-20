from django.urls import path
from .views import AccountRegisterView,PhoneTokenView,AccountMeView,ChangePasswordView
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register/',AccountRegisterView.as_view()),
    path('token/', PhoneTokenView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('me/', AccountMeView.as_view()),
    path('change-password/',ChangePasswordView.as_view()),
]
