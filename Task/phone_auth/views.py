from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, InviteCode
from .serializers import UserSerializer, InviteCodeSerializer
import time
import random


@api_view(['GET', 'POST'])
def phone_auth(request):
    if request.method == 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif request.method == 'POST':
        phone_number = request.data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
            authorization_code = random.randint(1000, 9999)
            user.authorization_code = authorization_code
            user.is_authenticated = False
            user.save()
            time.sleep(2) # имитация отправки кода
            return Response({'authorization_code': authorization_code}, status=status.HTTP_200_OK)
        else:
            user = User(phone_number=phone_number)
            authorization_code = random.randint(1000, 9999)
            user.authorization_code = authorization_code
            user.is_authenticated = False
            user.save()
            time.sleep(2) # имитация отправки кода
            return Response({'authorization_code': authorization_code}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def profile(request):
    if request.method == 'GET':
        phone_number = request.GET.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        phone_number = request.data.get('phone_number')
        invite_code = request.data.get('invite_code')
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
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
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
            inviter_list = User.objects.filter(used_invite_codes__used_by=user).values_list('phone_number', flat=True)
            return Response({'inviter_list': list(inviter_list)}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
