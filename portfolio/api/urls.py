from django.urls import path
from .views import UserRegistrationView, LoginAPIView, UserLogoutView, MyProjectListCreateAPIView, MyProjectDetailAPIView



urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('projects/', MyProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', MyProjectDetailAPIView.as_view(), name='project-detail'),
]
