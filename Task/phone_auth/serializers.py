from rest_framework import serializers
from .models import Profile, InviteCode


class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user', read_only=True)
    phone_number = serializers.IntegerField(read_only=True)
    authorization_code = serializers.IntegerField(read_only=True)
    invite_code = serializers.CharField(read_only=True)
    is_authenticated = serializers.BooleanField(read_only=True)

    class Meta:
        model = Profile
#       fields = '__all__'  # в принципе можно вроде было и так


class InviteCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InviteCode
        fields = '__all__'
