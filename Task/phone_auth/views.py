import random
import time
from django.contrib.auth import login
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Profile, InviteCode
from .serializers import ProfileSerializer, InviteCodeSerializer


@api_view(['POST'])
def register(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        user_profile = serializer.save()
        authorization_code = f'{random.randint(0, 9999):04}'
        user_profile.authorization_code = authorization_code
        user_profile.is_authenticated = False
        user_profile.save()
        time.sleep(2)  # имитация отправки кода
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
    time.sleep(2)  # имитация отправки кода
    return Response({'authorization_code': user_profile.authorization_code}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def check_code(request):
    user_profile = Profile.objects.get(user=request.user)
    user_profile.is_authenticated = True
    user_profile.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def profile(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number')
        if Profile.objects.filter(phone_number=phone_number).exists():
            user = Profile.objects.get(phone_number=phone_number)
            serializer = ProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        phone_number = request.data.get('phone_number')
        invite_code = request.data.get('invite_code')
        if Profile.objects.filter(phone_number=phone_number).exists():
            user = Profile.objects.get(phone_number=phone_number)
            if InviteCode.objects.filter(code=invite_code, used_by=user).exists():
                return Response({'message': 'Invite code already used by you'}, status=status.HTTP_400_BAD_REQUEST)
            elif InviteCode.objects.filter(code=invite_code).exists():
                invite = InviteCode.objects.get(code=invite_code)
                user.invite_code = invite.code
                user.save()
                return Response({'message': 'Invite code activated'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invite code not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def inviter_list(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number')
        if Profile.objects.filter(phone_number=phone_number).exists():
            user = Profile.objects.get(phone_number=phone_number)
            inviter_list = Profile.objects.filter(used_invite_codes__used_by=user).values_list('phone_number', flat=True)
            return Response({'inviter_list': list(inviter_list)}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
