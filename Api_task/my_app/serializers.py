from rest_framework import serializers
# from authentication.models import User
from .models import *
# from authentication.serializers import UserSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"