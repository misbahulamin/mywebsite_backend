from django.urls import path
from .views import UserRegistrationView, LoginAPIView, UserLogoutView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
