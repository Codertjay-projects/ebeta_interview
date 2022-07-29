from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(ModelSerializer):
    """
    This serializer is used only to get the detail of the user but not all details
    """
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'email',
        ]


# This serializer is used only when users login or register to get information
class UserTokenDetailSerializer(serializers.ModelSerializer):
    """
    This returns more detail about a user and it is only used when the user
    logs in or register
    """

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'last_login',
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}, 'otp': {'write_only': True}}


class TokenSerializer(serializers.ModelSerializer):
    """
    In here i am checking if the user email has been verified before
    sending him his details
    """
    user = SerializerMethodField(read_only=True)
    access = SerializerMethodField(read_only=True)
    refresh = SerializerMethodField(read_only=True)

    class Meta:
        model = Token
        fields = ('access', 'refresh', 'user',)

    def get_access(self, obj):
        """
        This access token is a jwt token that get expired after a particular time given which could either be 24 hour
        """
        refresh = RefreshToken.for_user(obj.user)
        return str(refresh.access_token)

    def get_refresh(self, obj):
        refresh = RefreshToken.for_user(obj.user)
        return str(refresh)

    def get_user(self, obj):
        """The user serializer"""
        return UserTokenDetailSerializer(obj.user, read_only=True).data
