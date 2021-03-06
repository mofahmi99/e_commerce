from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'user_name', 'password', 'token')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """

        override the create method to store a hashed password in database and create token for each user
        """
        password = validated_data.pop("password")
        hashed_password = make_password(password)
        user = User.objects.create(password=hashed_password, **validated_data)
        user_created_token = User.objects.create_token(user)
        return user_created_token


class UserLoginSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('id', 'user_name', 'password', 'token')
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        """
        authenticate user data to log to the system
        """
        user_name = data.get("user_name")
        password = data.get("password")
        user = authenticate(user_name=user_name, password=password)
        if user is None:
            raise serializers.ValidationError(
                'user not found'
            )
        return user
