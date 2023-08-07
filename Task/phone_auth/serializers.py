from rest_framework import serializers
from .models import User, InviteCode


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class InviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteCode
        fields = '__all__'
