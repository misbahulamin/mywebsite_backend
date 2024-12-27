from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLogInSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token


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
