from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ..models import MyProject

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password_confirmation']

    def validate(self, data):
        # Check that password and password_confirmation match
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords must match.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error' : "Email Already exists"})
        return data

    def create(self, validated_data):
        # Remove password_confirmation from the data
        validated_data.pop('password_confirmation')

        # Create user and set password
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # user.is_active = False
        # user.save()
        return user


class UserLogInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class MyProjectSerializer(serializers.ModelSerializer):
    # Custom logic for live and code_link to handle null cases
    live = serializers.SerializerMethodField()
    code_link = serializers.SerializerMethodField()

    class Meta:
        model = MyProject
        fields = '__all__'

    def get_live(self, obj):
        return obj.live if obj.live else None

    def get_code_link(self, obj):
        return obj.code_link if obj.code_link else None