import random
import time
from django.contrib.auth import login
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile, InviteCode, InviterList
from .serializers import ProfileSerializer, InviteCodeSerializer, InviterList


@api_view(['POST'])
def register(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        user_profile = serializer.save()
        authorization_code = f'{random.randint(0, 9999):04}'
        user_profile.authorization_code = authorization_code
        user_profile.is_authenticated = False
        user_profile.save()
        time.sleep(2)  # имитация отправки кода т.к. у меня нет службы отправки смс-ок
        login(request, user_profile.user)
        return Response({'authorization_code': authorization_code}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def new_code(request):
    user_profile = Profile.objects.get(user=request.user)
    user_profile.authorization_code = f'{random.randint(0, 9999):04}'
    user_profile.save()
    time.sleep(2)  # имитация отправки кода т.к. у меня нет службы отправки смс-ок
    return Response({'authorization_code': user_profile.authorization_code}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def check_code(request):
    user_profile = Profile.objects.get(user=request.user)
    user_profile.is_authenticated = True
    user_profile.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
        return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Profile.DoesNotExist:
        return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def inviter_list(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number')
        if Profile.objects.filter(phone_number=phone_number).exists():
            user = Profile.objects.get(user=request.user)
            inviter_list= Profile.objects.filter(used_invite_codes__used_by=user).values_list('phone_number', flat=True)
            return Response({'inviter_list': list(inviter_list)}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
