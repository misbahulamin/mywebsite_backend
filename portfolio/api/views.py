from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLogInSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token
from ..models import MyProject
from .serializers import MyProjectSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user first
            user = serializer.save()  # Now `user` is defined and valid

            # Generate a token for the created user
            token = default_token_generator.make_token(user)

            return Response({
                "message": "User created successfully!",
                "token": token
            }, status=status.HTTP_201_CREATED)

        # Return errors if validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLogInSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user:
                # Generate or retrieve an authentication token
                token, _ = Token.objects.get_or_create(user=user)

                # Log the user in
                login(request, user)

                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'message': 'Logged in successfully.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    def get(self, request):
        # Delete the user's auth token if it exists
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()

        # Log the user out
        logout(request)

        # Return a success message
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    

class MyProjectListCreateAPIView(ListCreateAPIView):
    """
    Handles listing all projects (accessible to anyone)
    and creating a new project (restricted to authenticated users).
    """
    queryset = MyProject.objects.all()
    serializer_class = MyProjectSerializer

    def get_permissions(self):
        # Allow anyone to list projects, but restrict creation to authenticated users
        if self.request.method == "POST":
            return [IsAuthenticatedOrReadOnly()]
        return [AllowAny()]


class MyProjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving (accessible to anyone),
    updating, and deleting a single project (restricted to authenticated users).
    """
    queryset = MyProject.objects.all()
    serializer_class = MyProjectSerializer

    def get_permissions(self):
        # Allow anyone to retrieve a project
        if self.request.method in ["GET"]:
            return [AllowAny()]
        # Restrict update and delete operations to authenticated users
        return [IsAuthenticatedOrReadOnly()]